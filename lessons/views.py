from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from lessons.task import mailing_about_updates
from lessons.models import Course, Lesson, Subscriptions
from lessons.pagination import CourseAndLessonPagination
from lessons.permissions import IsModerator, IsOwner
from lessons.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer
from lessons.services import create_payment, check_payment
from users.models import Payment


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = CourseAndLessonPagination

    def get_queryset(self):
        if self.action in ['list', 'retrieve', 'update', 'destroy']:
            return Course.objects.filter(owner=self.request.user)
        return Course.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [~IsModerator, IsAuthenticated]
        elif self.action in ['retrieve', 'update']:
            permission_classes = [IsModerator | IsOwner, IsAuthenticated]
        elif self.action == 'destroy':
            permission_classes = [IsOwner, IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        course = serializer.save()
        mailing_about_updates.delay(course.pk)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        course = serializer.save()
        mailing_about_updates.delay(course.pk)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    pagination_class = CourseAndLessonPagination

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Lesson.objects.all().order_by('name')
        return Lesson.objects.filter(owner=self.request.user)

    permission_classes = [IsAuthenticated]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsOwner, IsAuthenticated]

    def get_queryset(self):
        return Lesson.objects.filter(owner=self.request.user)


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson']
    ordering_fields = ['pay_date']


class PayLessonAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        lesson = get_object_or_404(Lesson, pk=self.kwargs.get('pk'))
        user = self.request.user

        with transaction.atomic():
            new_payment = serializer.save(user=user, paid_lesson=lesson)
            try:
                create_payment(lesson, user)
            except Exception as e:
                raise ValidationError({"detail": str(e)})
            new_payment.save()


class PayCourseAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs.get('pk'))
        user = self.request.user

        with transaction.atomic():
            new_payment = serializer.save(user=user, paid_course=course)

            try:
                session = create_payment(new_payment.paid_course, new_payment.user)
                new_payment.session_id = session.id
                new_payment.payment_url = session.url
            except Exception as e:
                raise ValidationError({"detail": str(e)})

            new_payment.save()


class CheckPaymentAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def get_object(self):
        obj = super().get_object()
        session_id = obj.session_id

        try:
            session = check_payment(session_id)
            if session and session.payment_status in {'paid', 'complete'}:
                obj.is_paid = True
                obj.save()
        except Exception as e:
            raise ValidationError({"detail": str(e)})

        return obj


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        course_pk = self.kwargs.get('pk')
        course = get_object_or_404(Course, pk=course_pk)

        new_sub = serializer.save(user=self.request.user, course=course)


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    queryset = Subscriptions.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("Вы не можете удалить подписку, которая не принадлежит вам.")
        super().perform_destroy(instance)

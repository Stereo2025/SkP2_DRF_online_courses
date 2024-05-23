from django.urls import path
from rest_framework.routers import DefaultRouter

from lessons.apps import LessonsConfig
from lessons.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentListAPIView, SubscriptionCreateAPIView, \
    SubscriptionDestroyAPIView, PayLessonAPIView, PayCourseAPIView, CheckPaymentAPIView

app_name = LessonsConfig.name
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')


urlpatterns = [
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lessons/', LessonListAPIView.as_view(), name='lessons_list'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson'),
    path('lessons/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lessons/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),

    path('payments/', PaymentListAPIView.as_view(), name='payment_list'),
    path('pay_lesson/<int:pk>/', PayLessonAPIView.as_view(), name='pay_lesson'),
    path('pay_course/<int:pk>/', PayCourseAPIView.as_view(), name='pay_course'),
    path('check_pay/<int:pk>/', CheckPaymentAPIView.as_view(), name='check_pay'),

    path('courses/create_sub/<int:pk>/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
    path('courses/delete_sub/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='subscription_delete'),
] + router.urls

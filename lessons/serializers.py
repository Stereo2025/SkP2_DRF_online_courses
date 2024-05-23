from rest_framework import serializers
from lessons.models import Course, Lesson, Subscriptions
from lessons.validators import VideoUrlValidator
from users.models import Payment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class MinimalLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['name', 'description']
        validators = [VideoUrlValidator(field='video_url')]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = MinimalLessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_lessons_count(self, course):
        return course.lessons.count()

    def get_is_subscribed(self, course):
        user = self.context['request'].user
        if user and user.is_authenticated:
            subscription_exists = Subscriptions.objects.filter(course=course, user=user).exists()
            return subscription_exists
        return False

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'lessons_count', 'lessons', 'is_subscribed']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = '__all__'

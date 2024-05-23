from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from lessons.models import Lesson, Course, Subscriptions
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='test@mail.ru', password='qwe123')
        self.client.force_authenticate(user=self.user)

        self.lesson = Lesson.objects.create(
            name="test",
            description="test description",
            video_url="https://www.youtube.com/watch",
            owner=self.user,
        )

    def test_create_lesson(self):
        """Тестирование создание урока"""
        data = {
            "name": "test",
            "description": "test description",
            "video_url": "https://www.youtube.com/watch",
        }
        response = self.client.post(
            reverse('lessons:lesson_create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json(),
            {'id': 2, 'name': 'test', 'image': None, 'description': 'test description',
             'video_url': 'https://www.youtube.com/watch', 'course': None, 'owner': self.user.pk}
        )

    def test_list_lessons(self):
        """Тестирование списка уроков"""
        response = self.client.get(
            reverse('lessons:lessons_list'),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {'count': 1, 'next': None, 'previous': None, 'results': [
                {'id': self.lesson.pk, 'name': self.lesson.name, 'image': self.lesson.image,
                 'description': self.lesson.description,
                 'video_url': self.lesson.video_url, 'course': self.lesson.course, 'owner': self.user.pk}]}
        )

    def test_retrieve_lesson(self):
        """Тестирование экземпляра урока"""
        response = self.client.get(
            reverse('lessons:lesson', kwargs={'pk': self.lesson.pk}),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.lesson.pk, 'name': self.lesson.name, 'image': self.lesson.image,
             'description': self.lesson.description,
             'video_url': self.lesson.video_url, 'course': self.lesson.course, 'owner': self.user.pk}

        )

    def test_update_lesson(self):
        """Тестирование редактирования урока"""
        data = {
            "name": "test_update",
            "description": "update description",
            "video_url": "https://www.youtube.com/watch",
        }
        response = self.client.patch(
            reverse('lessons:lesson_update', kwargs={'pk': self.lesson.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {'id': self.lesson.pk, 'name': 'test_update', 'image': None, 'description': 'update description',
             'video_url': 'https://www.youtube.com/watch', 'course': None, 'owner': self.user.pk}
        )

    def test_delete_lesson(self):
        """Тестирование удаления урока"""

        response = self.client.delete(
            reverse('lessons:lesson_delete', kwargs={'pk': self.lesson.pk}),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class SubscriptionTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='test@mail.ru', password='test1234')
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            name="test course",
            description="test description",
            owner=self.user,
        )

        self.subscription = Subscriptions.objects.create(
            course=self.course,
            user=self.user
        )

    def test_create_subscription(self):
        """Тестирование создание подписки"""
        data = {
            "course": self.course.pk,
            "user": self.user.pk,
        }
        response = self.client.post(
            reverse('lessons:subscription_create', kwargs={'pk': self.course.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {'id': 2, 'course': self.course.pk, 'user': self.user.pk}
        )

    def test_delete_subscription(self):
        """Тестирование удаления подписки"""

        response = self.client.delete(
            reverse('lessons:subscription_delete', kwargs={'pk': self.subscription.pk}),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from lessons.models import Course
from lessons.services import send_mailing
from users.models import User


@shared_task
def mailing_about_updates(course_id):
    """Отправляет сообщения об обновлении курса всем подписанным пользователям."""
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return

    if now() - course.date_modified <= timedelta(hours=4):
        subscription_list = course.subscriptions.select_related('user')
        users = [subscription.user for subscription in subscription_list]

        subject = 'Обновление курса'
        body = f'Вышло обновление по курсу {course}'
        send_mailing(users, subject, body)

        course.date_modified = now()
        course.save()


@shared_task
def check_user():
    """Отключает неактивных пользователей, не входивших в систему последний месяц."""
    month_ago = now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=month_ago)
    inactive_users.update(is_active=False)

import logging

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from lms.models import Course, Subscription

from datetime import timedelta

from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task
def send_course_upd_notification(course_id):
    """Рассылка уведомлений о обновлени курса"""
    course = Course.objects.get(pk=course_id)
    subscriptions = Subscription.objects.filter(course=course)

    for subscription in subscriptions:
        logger.info(f'Отправка уведомления о обновлении курса: {subscription.user.email}')
        send_mail(
            f"Обновление курса {course.course_name}",
            "Курс на который вы подписаны обновлён!",
            from_email=EMAIL_HOST_USER,
            recipient_list=[subscription.user.email],
            fail_silently=True
        )


@shared_task
def block_inactive_users():
    """Блокировка неактивных пользователей"""
    inactive_days = 30
    all_users = get_user_model()
    month_ago = timezone.now() - timedelta(days=inactive_days)

    inactive_users = all_users.objects.filter(
        last_login__lte=month_ago,
        is_active=True
    ).only('id', 'is_active')

    for user in inactive_users:
        user.is_active = False
        user.save()
        logger.info(f'Пользователь {user.email} заблокирован в связи с неактивностью {inactive_days} дней')

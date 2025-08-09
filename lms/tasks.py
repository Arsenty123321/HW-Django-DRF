from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from lms.models import Course, Subscription


@shared_task
def send_course_upd_notification(course_id):
    """Рассылка уведомлений о обновлени курса"""
    course = Course.objects.get(pk=course_id)
    subscriptions = Subscription.objects.filter(course=course)

    for subscription in subscriptions:
        send_mail(
            f"Обновление курса {course.course_name}",
            "Курс на который вы подписаны обновлён!",
            from_email=EMAIL_HOST_USER,
            recipient_list=[subscription.user.email],
            fail_silently=True
        )

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from users.models import CustomsUser


@shared_task
def newsletter_about_updating_course_materials(email):
    """Отправка рассылки подписчику курса при обновлении материалов курса"""
    send_mail(
        subject="Обновление курса",
        message="Материалы курса были обновлены. Ознакомиться с обновлениями Вы можете на сайте курса",
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
    )


@shared_task
def checking_user_activity():
    """Блокировка пользователя, если он не заходил более 30 дней"""
    one_month_ago = timezone.now() - timezone.timedelta(days=30)
    inactive_users = CustomsUser.objects.filter(
        last_login__lt=one_month_ago, is_active=True
    )

    for user in inactive_users:
        user.is_active = False
        user.save()

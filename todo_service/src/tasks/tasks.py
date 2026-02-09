from celery import shared_task
from django.utils import timezone
from django.conf import settings
import requests

from .models import Task


@shared_task
def check_overdue_tasks():
    """Проверяет просроченные задачи и отправляет уведомления."""
    now = timezone.now()

    overdue_tasks = Task.objects.filter(
        due_date__lt=now, status__in=["pending", "in_progress"]
    ).select_related("user")

    for task in overdue_tasks:
        try:
            send_telegram_notification.delay(
                telegram_id=task.user.telegram_id,
                task_title=task.title,
                message=f"⚠️ Задача просрочена: {task.title}",
            )
        except Exception:
            pass
    return f"Проверено {overdue_tasks.count()} просроченных задач"


@shared_task
def send_telegram_notification(telegram_id, task_title, message):
    """Отправляет уведомление в Telegram."""
    bot_token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": telegram_id, "text": message, "parse_mode": "HTML"}
    requests.post(url, json=data)

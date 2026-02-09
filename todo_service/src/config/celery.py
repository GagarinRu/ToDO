import os
from datetime import timedelta

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("todo_service")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "check-overdue-tasks-every-hour": {
        "task": "tasks.tasks.check_overdue_tasks",
        "schedule": timedelta(seconds=30),
    },
}

from django.db import models
from django.conf import settings

from base.models import NULLABLE, BaseModel
from base.utils import dt_now
from tasks.choices import Priority, Status
from tasks.constants import (
    DEFAULT_COLOR,
    MAX_LENGHT,
    MAX_LENGHT_NAME,
    MAX_LENGHT_CHOICE,
    MAX_LENGHT_TITLE,
)


class Category(BaseModel):
    """Модель категории (тега) для задач."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name="Пользователь",
    )
    name = models.CharField("Название категории", max_length=MAX_LENGHT_NAME)
    color = models.CharField(
        "Цвет (HEX)",
        max_length=MAX_LENGHT,
        default=DEFAULT_COLOR,
        help_text="Цвет в формате HEX (#RRGGBB)",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]
        unique_together = ["user", "name"]

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    @property
    def hashid(self):
        return str(self.id)


class Task(BaseModel):
    """Модель задачи ToDo."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Пользователь",
    )
    title = models.CharField("Заголовок", max_length=MAX_LENGHT_TITLE)
    description = models.TextField("Описание", **NULLABLE)
    status = models.CharField(
        "Статус",
        max_length=MAX_LENGHT_CHOICE,
        choices=Status.choices,
        default=Status.PENDING,
    )
    priority = models.CharField(
        "Приоритет",
        max_length=MAX_LENGHT_CHOICE,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    due_date = models.DateTimeField("Срок выполнения", **NULLABLE)
    completed_at = models.DateTimeField("Дата завершения", **NULLABLE)
    categories = models.ManyToManyField(
        Category, related_name="tasks", blank=True, verbose_name="Категории"
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["due_date"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.user.username})"

    @property
    def hashid(self):
        return str(self.id)

    @property
    def is_overdue(self):
        """Просрочена ли задача."""
        if self.due_date and self.status not in [
            self.Status.COMPLETED,
            self.Status.CANCELLED,
        ]:
            return self.due_date < dt_now
        return False

    def save(self, *args, **kwargs):
        """Автоматически устанавливаем completed_at при завершении задачи."""
        if self.status == Status.COMPLETED and not self.completed_at:
            self.completed_at = dt_now
        elif self.status != Status.COMPLETED and self.completed_at:
            self.completed_at = None
        super().save(*args, **kwargs)

from django.contrib.auth.models import AbstractUser
from django.db import models

from base.models import NULLABLE, BaseModel


class User(AbstractUser, BaseModel):
    """Кастомная модель пользователя с ручной генерацией HashID."""

    telegram_id = models.BigIntegerField(
        "Telegram ID", unique=True, help_text="ID пользователя в Telegram", **NULLABLE
    )
    telegram_username = models.CharField("Telegram username", max_length=32, **NULLABLE)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-date_joined"]

    def __str__(self):
        return f"{self.username} ({self.get_full_name() or 'Без имени'})"

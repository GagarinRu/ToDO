from typing import ClassVar, Tuple

from django.db import models


class BaseTextChoice(models.TextChoices):
    """Base Text Choice."""

    choices: ClassVar[Tuple[Tuple[str, str], ...]]

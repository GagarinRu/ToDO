from datetime import datetime

from django.utils import timezone


def dt_now() -> datetime:
    """Get datetime now."""
    return timezone.now()

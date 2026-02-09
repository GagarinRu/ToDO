from base.choices import BaseTextChoice


class Status(BaseTextChoice):
    """Выбор типа статуса."""

    PENDING = "pending", "В ожидании"
    IN_PROGRESS = "in_progress", "В работе"
    COMPLETED = "completed", "Завершена"
    CANCELLED = "cancelled", "Отменена"


class Priority(BaseTextChoice):
    """Выбор типа приоритета."""

    LOW = "low", "Низкий"
    MEDIUM = "medium", "Средний"
    HIGH = "high", "Высокий"
    CRITICAL = "critical", "Критический"

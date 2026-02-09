from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from hashids import Hashids
import redis

NULLABLE = {"blank": True, "null": True}


class BaseModel(models.Model):
    """Base model с автоматической генерацией HashID."""

    objects: models.Manager

    id = models.CharField(
        primary_key=True, max_length=50, editable=False, verbose_name="HashID"
    )
    created = models.DateTimeField(_("created"), auto_now_add=True)
    updated = models.DateTimeField(_("updated"), auto_now=True)

    class Meta:
        abstract = True

    @classmethod
    def get_model_name(cls):
        """Возвращает имя модели для префикса."""
        return cls.__name__.lower()

    @classmethod
    def get_prefix(cls):
        """Возвращает префикс для hashid на основе имени модели."""
        model_name = cls.get_model_name()
        prefixes = {"user": "user_", "task": "task_", "category": "cat_"}
        return prefixes.get(model_name, f"{model_name}_")

    @classmethod
    def get_redis_client(cls):
        """Возвращает Redis клиент."""
        return redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
            decode_responses=True,
        )

    @classmethod
    def get_redis_counter_key(cls):
        """Возвращает ключ для счетчика в Redis."""
        return f"{cls.get_model_name()}:id:counter"

    @classmethod
    def generate_hashid(cls):
        """Генерирует HashID используя Redis для счетчика."""
        redis_client = cls.get_redis_client()
        counter_key = cls.get_redis_counter_key()
        next_id = redis_client.incr(counter_key)
        hashids = Hashids(
            salt=settings.HASHID_FIELD_SALT,
            alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890",
            min_length=7,
        )
        hashid = hashids.encode(next_id)
        return f"{cls.get_prefix()}{hashid}"

    def save(self, *args, **kwargs):
        """Генерируем HashID при создании."""
        if not self.id:
            self.id = self.generate_hashid()
            print(f"Generated {self.__class__.__name__} ID: {self.id}")
            kwargs["force_insert"] = True
            kwargs["force_update"] = False
        super().save(*args, **kwargs)

    @property
    def hashid(self):
        return str(self.id)

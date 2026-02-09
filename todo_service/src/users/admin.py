from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "telegram_id",
        "telegram_username",
        "is_staff",
        "is_active",
    )
    list_filter = ("is_staff", "is_active", "groups")
    search_fields = ("username", "email", "telegram_id", "telegram_username")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Персональная информация",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "telegram_id",
                    "telegram_username",
                )
            },
        ),
        (
            "Права доступа",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "telegram_id",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    ordering = ("-date_joined",)

from django.contrib import admin
from .models import Task, Category


class CategoryInline(admin.TabularInline):
    model = Task.categories.through
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "color", "created")
    list_filter = ("user", "created")
    search_fields = ("name", "user__username")
    raw_id_fields = ("user",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "status",
        "priority",
        "due_date",
        "created",
        "is_overdue",
    )
    list_filter = ("status", "priority", "created", "due_date", "user")
    search_fields = ("title", "description", "user__username")
    raw_id_fields = ("user",)
    readonly_fields = ("created", "updated", "completed_at")
    fieldsets = (
        ("Основная информация", {"fields": ("title", "description", "user")}),
        ("Детали задачи", {"fields": ("status", "priority", "due_date", "categories")}),
        ("Даты", {"fields": ("created", "updated", "completed_at")}),
    )
    filter_horizontal = ("categories",)

    def is_overdue(self, obj):
        return obj.is_overdue

    is_overdue.boolean = True
    is_overdue.short_description = "Просрочена"

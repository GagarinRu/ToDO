from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    """Command to create a superuser."""

    def handle(self, *args, **options):
        # Импортируем внутри функции чтобы избежать циклических импортов
        from users.models import User

        admin_email = getattr(settings, "ADMIN_EMAIL", "admin@example.com")
        admin_username = getattr(settings, "ADMIN_USERNAME", "admin")
        admin_password = getattr(settings, "ADMIN_PASSWORD", "admin123")

        # Пропускаем если уже существует
        if User.objects.filter(username=admin_username).exists():
            self.stdout.write(f"Admin user '{admin_username}' already exists")
            return

        # Создаем через стандартный create_user (должен работать с вашим менеджером)
        try:
            user = User.objects.create_user(
                username=admin_username,
                email=admin_email,
                password=admin_password,
                is_staff=True,
                is_superuser=True,
                is_active=True,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Admin user '{admin_username}' created successfully"
                )
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error creating admin user: {e}"))

            # Альтернативный метод
            try:
                user = User(
                    username=admin_username,
                    email=admin_email,
                    is_staff=True,
                    is_superuser=True,
                    is_active=True,
                )
                user.set_password(admin_password)
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Admin user '{admin_username}' created (alternative method)"
                    )
                )
            except Exception as e2:
                self.stdout.write(
                    self.style.ERROR(f"Alternative method also failed: {e2}")
                )

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "telegram_id",
            "telegram_username",
            "first_name",
            "last_name",
            "email",
            "date_joined",
        )
        read_only_fields = ("id", "date_joined")


class TelegramAuthSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField(required=True)
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        telegram_id = attrs.get("telegram_id")

        try:
            user = User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            username = attrs.get("username")
            first_name = attrs.get("first_name", "")
            base_username = f"tg_{telegram_id}"
            username = base_username
            user = User.objects.create_user(
                username=username,
                telegram_id=telegram_id,
                telegram_username=attrs.get("username", ""),
                first_name=first_name,
                password=f"telegram_{telegram_id}",
            )
        attrs["user"] = user
        return attrs

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

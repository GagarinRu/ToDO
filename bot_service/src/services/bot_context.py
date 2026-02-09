import logging
from cachetools import TTLCache
from services.auth_service import AuthService
from services.api_client import ApiClient

logger = logging.getLogger(__name__)


class BotContext:
    """Контекст бота для хранения состояния и сервисов."""

    def __init__(self):
        self.user_cache = TTLCache(maxsize=1000, ttl=300)
        self.auth_service = AuthService()
        self.api_client = ApiClient(self.auth_service)

    async def authenticate_user(self, telegram_user, chat_id):
        """Аутентифицирует пользователя и возвращает данные."""
        cache_key = f"{telegram_user.id}_{chat_id}"
        cached_user = self.user_cache.get(cache_key)
        if cached_user:
            return cached_user
        authenticated = await self.auth_service.authenticate(
            telegram_id=telegram_user.id,
            username=telegram_user.username or "",
            first_name=telegram_user.first_name or "",
        )

        if authenticated:
            django_user = await self.api_client.get_or_create_user(
                telegram_id=telegram_user.id,
                username=telegram_user.username or "",
                first_name=telegram_user.first_name or "",
            )
            if django_user:
                user_data = {
                    "telegram_user": telegram_user,
                    "django_user": django_user,
                    "chat_id": chat_id,
                    "is_authenticated": True,
                }
                self.user_cache[cache_key] = user_data
                return user_data
            else:
                logger.error(f"Failed to get/create Django user for {telegram_user.id}")
        else:
            logger.error(f"Authentication failed for user {telegram_user.id}")
        user_data = {
            "telegram_user": telegram_user,
            "django_user": None,
            "chat_id": chat_id,
            "is_authenticated": False,
        }
        self.user_cache[cache_key] = user_data
        logger.warning(f"Created unauthenticated user data for {telegram_user.id}")
        return user_data

    def get_user_from_cache(self, telegram_user, chat_id):
        """Получает пользователя из кэша."""
        cache_key = f"{telegram_user.id}_{chat_id}"
        return self.user_cache.get(cache_key)


bot_context = BotContext()

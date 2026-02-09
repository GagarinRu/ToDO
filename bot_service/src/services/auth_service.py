import aiohttp
import logging
from typing import Optional

from config.config import settings

logger = logging.getLogger(__name__)


class AuthService:
    """Сервис для аутентификации."""

    def __init__(self):
        self.token: Optional[str] = None

    async def authenticate(
        self, telegram_id: int, username: str, first_name: str
    ) -> bool:
        """Аутентификация через Telegram."""
        url = f"{settings.api_base_url}/api/v1/users/telegram_auth/"
        data = {
            "telegram_id": telegram_id,
            "username": username,
            "first_name": first_name or "",
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data) as response:
                    logger.info(f"📡 Ответ от API: {response.status}")

                    if response.status == 200:
                        token_data = await response.json()
                        self.token = token_data.get("access")
                        logger.info(f"✅ Токен получен: {self.token[:20]}...")
                        return True
                    else:
                        error_text = await response.text()
                        logger.error(
                            f"❌ Ошибка аутентификации: {response.status} - {error_text}"
                        )
                        return False
        except Exception as e:
            logger.error(f"🔥 Ошибка подключения: {e}")
            return False

    async def get_token(self) -> Optional[str]:
        """Получить токен."""
        return self.token

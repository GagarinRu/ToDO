import aiohttp
import logging
from typing import Optional, Dict, List
from config.config import settings
from services.auth_service import AuthService

logger = logging.getLogger(__name__)


class ApiClient:
    """Клиент для работы с Django REST API."""

    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
        self.base_url = settings.api_base_url

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> Optional[Dict]:
        """Выполняет HTTP запрос к API."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {"Content-Type": "application/json"}
        token = await self.auth_service.get_token()
        if token:
            headers["Authorization"] = f"Bearer {token}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params,
                    headers=headers,
                    timeout=settings.DJANGO_API_TIMEOUT,
                ) as response:
                    if response.status == 204:
                        return None

                    response_data = await response.json()

                    if response.status >= 400:
                        logger.error(f"API error {response.status}: {response_data}")
                        return None

                    return response_data
        except Exception as e:
            logger.error(f"Request error to {url}: {e}")
            return None

    async def get_or_create_user(
        self, telegram_id: int, username: str, first_name: str
    ) -> Optional[Dict]:
        """Получает или создает пользователя."""
        authenticated = await self.auth_service.authenticate(
            telegram_id, username, first_name
        )
        if authenticated:
            return await self._make_request(
                "GET", f"api/v1/users/telegram/{telegram_id}/"
            )
        return None

    async def get_tasks(self) -> Optional[List[Dict]]:
        """Получает список задач пользователя."""
        data = await self._make_request("GET", "api/v1/tasks/")
        if data:
            if isinstance(data, dict) and "results" in data:
                return data["results"]
            elif isinstance(data, list):
                return data
        return []

    async def create_task(
        self, title: str, description: str = "", category_ids: List[str] = None
    ) -> Optional[Dict]:
        """Создает новую задачу."""
        task_data = {
            "title": title,
            "description": description,
            "status": "pending",
            "priority": "medium",
            "category_ids": category_ids or [],
        }
        return await self._make_request("POST", "api/v1/tasks/", data=task_data)

    async def get_categories(self) -> Optional[List[Dict]]:
        """Получает список категорий."""
        logger.info("Getting categories from API...")
        data = await self._make_request("GET", "api/v1/categories/")

        if data:
            logger.info(f"Categories API returned: {data}")
            if isinstance(data, dict) and "results" in data:
                return data["results"]
            elif isinstance(data, list):
                return data
        logger.warning("No categories data returned")
        return []

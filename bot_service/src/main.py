import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from config.config import settings
from dialogs.task_dialog import task_dialog
from handlers import categories, commands, tasks

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    """Основная функция запуска бота."""
    logger.info("Starting bot...")

    # Инициализация бота
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

    # Хранилище состояний
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Регистрируем роутеры
    dp.include_router(commands.router)
    dp.include_router(tasks.router)
    dp.include_router(categories.router)
    dp.include_router(task_dialog)

    setup_dialogs(dp)
    # Запускаем бота
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Bot started successfully")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

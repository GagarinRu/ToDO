from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command


from utils.formatters import format_welcome_message
from services.bot_context import bot_context


router = Router()


@router.message(CommandStart())
async def command_start(message: Message):
    """Обработчик команды /start."""
    user_data = await bot_context.authenticate_user(message.from_user, message.chat.id)

    if user_data.get("is_authenticated", False):
        welcome_text = format_welcome_message(user_data.get("django_user", {}))
        await message.answer(welcome_text)
    else:
        await message.answer("❌ Ошибка аутентификации. Пожалуйста, попробуйте позже.")


@router.message(Command("help"))
async def command_help(message: Message):
    """Обработчик команды /help."""
    help_text = """
        📋 *Доступные команды:*

    /start - Начать работу с ботом
    /tasks - Показать мои задачи
    /new_task - Создать новую задачу (диалог)
    /categories - Показать категории
    /help - Показать это сообщение
    /cancel - Отмена действия

    🎯 *Создание задач:*
    • Используйте /new_task для пошагового создания
    • Или просто напишите текст для быстрого создания

    🎯 *Просмотр задач:*
    • Все задачи показываются с датой создания
    • Задачи отображаются с категориями
    • Используйте кнопки для управления

    ⏰ *Напоминания:*
    Бот автоматически напомнит о просроченных задачах!
    """
    await message.answer(help_text)


@router.message(Command("cancel"))
async def command_cancel(message: Message):
    """Обработчик команды /cancel."""
    await message.answer("❌ Текущее действие отменено.")

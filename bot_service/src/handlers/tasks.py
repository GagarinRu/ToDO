from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
import logging
from aiogram.filters import Command

from aiogram_dialog import DialogManager, StartMode
from utils.formatters import format_task_list
from dialogs.task_dialog import TaskDialogStates
from services.bot_context import bot_context


logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("tasks"))
async def command_tasks(message: Message):
    """Показать список задач."""
    user_data = bot_context.get_user_from_cache(message.from_user, message.chat.id)
    if not user_data:
        user_data = await bot_context.authenticate_user(
            message.from_user, message.chat.id
        )
    if not user_data or not user_data.get("is_authenticated", False):
        await message.answer("❌ Сначала нужно авторизоваться. Используйте /start")
        return
    try:
        tasks_data = await bot_context.api_client.get_tasks()
        if not tasks_data:
            await message.answer(
                "📭 У вас пока нет задач.\n\n"
                "Чтобы создать задачу:\n"
                "• Используйте команду /new_task для пошагового создания\n"
                "• Или просто напишите текст для быстрого создания"
            )
            return
        if isinstance(tasks_data, list):
            tasks = tasks_data
        elif isinstance(tasks_data, dict) and "results" in tasks_data:
            tasks = tasks_data["results"]
        else:
            tasks = []
        if not tasks:
            await message.answer(
                "📭 У вас пока нет задач. Используйте /new_task чтобы создать первую!"
            )
            return
        text = format_task_list(tasks)
        await message.answer(text, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error getting tasks: {e}")
        await message.answer("❌ Не удалось получить задачи. Попробуйте позже.")


@router.message(Command("new_task"))
async def command_new_task(message: Message, dialog_manager: DialogManager):
    """Запуск диалога создания задачи."""
    # Упрощаем - сразу аутентифицируем
    user_data = await bot_context.authenticate_user(message.from_user, message.chat.id)

    if not user_data or not user_data.get("is_authenticated", False):
        await message.answer("❌ Сначала нужно авторизоваться. Используйте /start")
        return

    await dialog_manager.start(TaskDialogStates.enter_title, mode=StartMode.RESET_STACK)


@router.callback_query(F.data.startswith("task:"))
async def task_callback_handler(callback: CallbackQuery, dialog_manager: DialogManager):
    """Обработчик callback'ов для задач."""
    chat_id = callback.message.chat.id if callback.message else None
    user_data = bot_context.get_user_from_cache(callback.from_user, chat_id)
    if not user_data or not user_data.get("is_authenticated", False):
        await callback.answer("❌ Сначала нужно авторизоваться. Используйте /start")
        return
    action = callback.data.split(":")[1]
    if action == "create":
        if dialog_manager:
            await dialog_manager.start(
                TaskDialogStates.enter_title, mode=StartMode.RESET_STACK
            )
        else:
            await callback.message.answer(
                "Для создания задачи используйте команду /new_task\n"
                "Или просто напишите текст задачи."
            )
        await callback.answer()

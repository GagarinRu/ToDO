from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Row, Back
from aiogram_dialog import DialogManager
from aiogram.types import Message, CallbackQuery
import logging

from aiogram.fsm.state import State, StatesGroup
from services.bot_context import bot_context

logger = logging.getLogger(__name__)


class TaskDialogStates(StatesGroup):
    """Состояния диалога."""

    enter_title = State()
    enter_description = State()
    confirm = State()


async def process_title(message: Message, widget, manager: DialogManager, text: str):
    """Обработчик ввода названия задачи."""
    if len(text.strip()) < 3:
        await message.answer("❌ Название должно быть не менее 3 символов")
        return

    manager.dialog_data["title"] = text.strip()
    await manager.next()


async def process_description(
    message: Message, widget, manager: DialogManager, text: str
):
    """Обработчик ввода описания задачи."""
    manager.dialog_data["description"] = text.strip()
    await manager.next()


async def skip_description(callback: CallbackQuery, button, manager: DialogManager):
    """Пропустить ввод описания."""
    manager.dialog_data["description"] = ""
    await manager.next()


async def confirm_task(callback: CallbackQuery, button, manager: DialogManager):
    """Подтверждение создания задачи."""
    title = manager.dialog_data.get("title", "")
    description = manager.dialog_data.get("description", "")
    try:
        user_data = await bot_context.authenticate_user(
            callback.from_user, callback.message.chat.id
        )
        if not user_data.get("is_authenticated", False):
            await callback.message.answer("❌ Ошибка аутентификации.")
            await manager.done()
            return
        task = await bot_context.api_client.create_task(title, description)
        if task:
            await callback.message.answer(
                f"✅ Задача создана!\n\n"
                f"📝 *{title}*\n"
                f"{description or 'Без описания'}\n\n"
                f"📅 Дата создания: {task.get('created_at', 'сегодня')}",
                parse_mode="Markdown",
            )
        else:
            await callback.message.answer("❌ Не удалось создать задачу.")
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        await callback.message.answer("❌ Ошибка при создании задачи.")
    await manager.done()


async def get_confirm_data(dialog_manager: DialogManager, **kwargs):
    """Получаем данные для окна подтверждения."""
    title = dialog_manager.dialog_data.get("title", "")
    description = dialog_manager.dialog_data.get("description", "Без описания")

    return {
        "title": title,
        "description": description,
    }


task_dialog = Dialog(
    Window(
        Const("📝 *Введите название задачи:*"),
        TextInput(
            id="title_input",
            on_success=process_title,
        ),
        Cancel(Const("❌ Отмена")),
        state=TaskDialogStates.enter_title,
        parse_mode="Markdown",
    ),
    Window(
        Const("✏️ *Введите описание задачи (или пропустите):*"),
        TextInput(
            id="description_input",
            on_success=process_description,
        ),
        Row(
            Button(Const("⏭️ Пропустить"), id="skip", on_click=skip_description),
            Back(Const("◀️ Назад")),
            Cancel(Const("❌ Отмена")),
        ),
        state=TaskDialogStates.enter_description,
        parse_mode="Markdown",
    ),
    Window(
        Format(
            "📋 *Проверьте данные:*\n\n"
            "📝 *Название:* {title}\n"
            "✏️ *Описание:* {description}\n\n"
            "Создать задачу?"
        ),
        Row(
            Button(Const("✅ Создать"), id="confirm", on_click=confirm_task),
            Back(Const("◀️ Назад")),
            Cancel(Const("❌ Отмена")),
        ),
        state=TaskDialogStates.confirm,
        parse_mode="Markdown",
        getter=get_confirm_data,
    ),
)

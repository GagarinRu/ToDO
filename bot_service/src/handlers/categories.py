from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.filters import Command
import logging

from services.bot_context import bot_context


logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("categories"))
async def command_categories(message: Message):
    """Обработчик команды /categories."""
    user_data = bot_context.get_user_from_cache(message.from_user, message.chat.id)
    if not user_data:
        user_data = await bot_context.authenticate_user(
            message.from_user, message.chat.id
        )
    if not user_data or not user_data.get("is_authenticated", False):
        await message.answer("❌ Сначала нужно авторизоваться. Используйте /start")
        return
    try:
        categories_list = await bot_context.api_client.get_categories()

        if not categories_list:
            await message.answer(
                "📂 У вас пока нет категорий.\n\n"
                "Категории можно создать через админ-панель Django.\n"
                "После создания они будут отображаться здесь."
            )
            return
        text = "📂 *Ваши категории:*\n\n"
        for i, category in enumerate(categories_list, 1):
            name = category.get("name", "Без названия")
            text += f"{i}. 🏷️ {name}\n"
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="➕ Создать в админке",
                        url="http://localhost:8000/admin/tasks/category/",
                    ),
                ]
            ]
        )
        await message.answer(text, parse_mode="Markdown", reply_markup=keyboard)
    except Exception as e:
        logger.error(f"Error loading categories: {e}")
        await message.answer("❌ Не удалось загрузить категории. Попробуйте позже.")


@router.callback_query(F.data.startswith("category:"))
async def category_callback_handler(callback: CallbackQuery):
    """Обработчик callback'ов для категорий."""
    chat_id = callback.message.chat.id if callback.message else None
    user_data = bot_context.get_user_from_cache(callback.from_user, chat_id)

    if not user_data or not user_data.get("is_authenticated", False):
        await callback.answer("❌ Сначала нужно авторизоваться. Используйте /start")
        return

    action = callback.data.split(":")[1]
    if action == "add":
        await callback.message.answer(
            "Чтобы добавить категорию, используйте админ-панель Django.\n\n"
            "Категории созданные через админку будут доступны для прикрепления к задачам."
        )
        await callback.answer()
    elif action == "edit":
        await callback.answer("Редактирование категорий через админ-панель Django.")
    elif action == "show":
        await command_categories(callback.message)
        await callback.answer()
    else:
        await callback.answer("Функция в разработке")

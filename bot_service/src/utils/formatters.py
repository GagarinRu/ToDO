from datetime import datetime


def format_task_list(tasks: list) -> str:
    """Форматирует список задач."""
    if not tasks:
        return "📭 Задачи не найдены"
    text = "📋 *Ваши задачи:*\n\n"
    for i, task in enumerate(tasks, 1):
        status_emoji = {
            "pending": "⏳",
            "in_progress": "🔄",
            "completed": "✅",
            "cancelled": "❌",
        }.get(task.get("status", "pending"), "📝")
        priority_emoji = {
            "low": "🟢",
            "medium": "🟡",
            "high": "🟠",
            "critical": "🔴",
        }.get(task.get("priority", "medium"), "⚪")
        title = task.get("title", "Без названия")
        created_at = task.get("created_at", "")
        created_str = "неизвестно"
        if created_at:
            try:
                if "Z" in created_at:
                    created_dt = datetime.fromisoformat(
                        created_at.replace("Z", "+00:00")
                    )
                elif "+" in created_at:
                    created_dt = datetime.fromisoformat(created_at)
                else:
                    created_dt = datetime.fromisoformat(created_at)
                created_str = created_dt.strftime("%d.%m.%Y %H:%M")
            except (ValueError, TypeError) as e:
                created_str = str(created_at)
                print(f"Error parsing date {created_at}: {e}")
        text += f"{i}. {status_emoji} {priority_emoji} *{title}*\n"
        text += f"   📅 Создано: {created_str}\n"
        if task.get("categories"):
            categories = task.get("categories", [])
            if categories:
                category_names = []
                for cat in categories:
                    if isinstance(cat, dict) and cat.get("name"):
                        category_names.append(cat.get("name"))
                    elif isinstance(cat, str):
                        category_names.append(cat)

                if category_names:
                    text += f"   🏷️ Категории: {', '.join(category_names)}\n"
        due_date = task.get("due_date")
        if due_date:
            try:
                if "Z" in str(due_date):
                    due_dt = datetime.fromisoformat(
                        str(due_date).replace("Z", "+00:00")
                    )
                elif "+" in str(due_date):
                    due_dt = datetime.fromisoformat(str(due_date))
                else:
                    due_dt = datetime.fromisoformat(str(due_date))

                due_str = due_dt.strftime("%d.%m.%Y %H:%M")
                text += f"   ⏰ Срок: {due_str}\n"
            except (ValueError, TypeError):
                text += f"   ⏰ Срок: {due_date}\n"

        text += "\n"
    return text


def format_welcome_message(user_data: dict) -> str:
    """Форматирует приветственное сообщение."""
    first_name = user_data.get("first_name", "Пользователь")
    username = user_data.get("username", "")

    return f"""
    👋 Привет, {first_name or username}!

    🎯 Добро пожаловать в ToDo бот!

    С помощью этого бота вы можете:
    • 📝 Создавать задачи (команда /new_task)
    • 🏷️ Просматривать категории (/categories)
    • 📋 Смотреть список задач (/tasks)
    • 🔔 Получать уведомления о просроченных задачах

    📅 *Все задачи показываются с датой создания*
    🏷️ *Категории помогают организовать задачи*

    Используйте /help для полного списка команд.
    """

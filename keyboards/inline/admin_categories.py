from aiogram.utils.keyboard import InlineKeyboardBuilder

def admin_categories_kb(categories):
    kb = InlineKeyboardBuilder()

    for c in categories:
        kb.button(
            text=f"❌ {c['title']}",
            callback_data=f"admin:cat:delete:{c['id']}"
        )

    kb.button(text="➕ Добавить категорию", callback_data="admin:cat:add")
    kb.button(text="⬅️ Назад", callback_data="menu:menu")

    kb.adjust(1)
    return kb.as_markup()

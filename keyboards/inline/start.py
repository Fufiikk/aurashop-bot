from aiogram.utils.keyboard import InlineKeyboardBuilder

def start_menu(is_admin: bool):
    kb = InlineKeyboardBuilder()

    kb.button(text="🛍 Товары", callback_data="menu:catalog")
    kb.button(text="🛒 Корзина", callback_data="menu:cart")
    kb.button(text="👤 Личный кабинет", callback_data="menu:profile")

    if is_admin:
        kb.button(text="🛠 Админка", callback_data="menu:admin")

    kb.adjust(1)
    return kb.as_markup()


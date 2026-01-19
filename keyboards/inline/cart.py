from aiogram.utils.keyboard import InlineKeyboardBuilder


def cart_kb(has_items: bool):
    kb = InlineKeyboardBuilder()

    if has_items:
        kb.button(text="💳 Оплатить", callback_data="cart:pay")
        kb.button(text="🗑 Очистить корзину", callback_data="cart:clear")

    kb.button(text="⬅️ В меню", callback_data="menu:menu")
    kb.adjust(1)
    return kb.as_markup()

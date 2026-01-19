from aiogram.utils.keyboard import InlineKeyboardBuilder


def profile_kb():
    kb = InlineKeyboardBuilder()

    kb.button(text="💳 Пополнить баланс", callback_data="profile:topup")
    kb.button(text="🎟 Ввести промокод", callback_data="profile:promo")
    kb.button(text="👥 Реферальная система", callback_data="profile:ref")
    kb.button(text="⬅️ В меню", callback_data="menu:menu")

    kb.adjust(1)
    return kb.as_markup()

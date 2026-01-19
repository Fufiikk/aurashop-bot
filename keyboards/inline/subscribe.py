from aiogram.utils.keyboard import InlineKeyboardBuilder


def subscribe_kb(channel_link: str):
    kb = InlineKeyboardBuilder()

    kb.button(text="📢 Подписаться", url=channel_link)
    kb.button(text="✅ Я подписался", callback_data="check_sub")

    kb.adjust(1)
    return kb.as_markup()

from aiogram.utils.keyboard import InlineKeyboardBuilder

def back_to_menu_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ В меню", callback_data="menu:menu")
    return kb.as_markup()

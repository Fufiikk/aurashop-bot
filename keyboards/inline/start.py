from aiogram.utils.keyboard import InlineKeyboardBuilder

def start_menu(is_admin: bool):
    kb = InlineKeyboardBuilder()

    kb.button(text="🛍 Товары", callback_data="menu:catalog")
    kb.button(text="🛒 Корзина", callback_data="menu:cart")
    kb.button(text="👤 Личный кабинет", callback_data="menu:profile")
    kb.button(text="☎️ Поддержка", url="http://t.me/AuraAdminOfficial")
    kb.button(text="📜 Пользовательское соглашение", url="https://telegra.ph/POLZOVATELSKOE-SOGLASHENIE-01-20-32")
    kb.button(text="📝 Политика конфиденциальности", url="https://telegra.ph/Politika-konfidencialnosti-01-20-59")

    if is_admin:
        kb.button(text="🛠 Админка", callback_data="menu:admin")

    kb.adjust(1,1,1,1,2)
    return kb.as_markup()


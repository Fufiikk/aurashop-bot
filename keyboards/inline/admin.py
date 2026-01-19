from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


# ─────────────────────────────
# CALLBACK DATA
# ─────────────────────────────
class AdminCB(CallbackData, prefix="admin"):
    action: str
    product_id: int | None = None
    category_id: int | None = None


# ─────────────────────────────
# ГЛАВНОЕ МЕНЮ АДМИНКИ
# ─────────────────────────────
def admin_menu_kb():
    kb = InlineKeyboardBuilder()

    kb.button(text="➕ Добавить товар", callback_data=AdminCB(action="add"))
    kb.button(text="📦 Товары", callback_data=AdminCB(action="products"))
    kb.button(text="📂 Категории", callback_data=AdminCB(action="categories"))
    kb.button(text="🎟 Промокоды", callback_data="admin:promos")
    kb.button(text="📢 Рассылка", callback_data="admin:mailing")
    kb.button(text="⬅️ В меню", callback_data="menu:menu")

    kb.adjust(1)
    return kb.as_markup()


# ─────────────────────────────
# СПИСОК ТОВАРОВ (АДМИН)
# ─────────────────────────────
def admin_products_kb(products):
    kb = InlineKeyboardBuilder()

    for p in products:
        status = "🟢" if p["is_active"] else "🔴"

        kb.button(
            text=f"{status} {p['title']}",
            callback_data=AdminCB(
                action="toggle",
                product_id=p["id"]
            )
        )

        kb.button(
            text="➕ Добавить выдачу",
            callback_data=AdminCB(
                action="add_item",
                product_id=p["id"]
            )
        )

    kb.button(text="⬅️ Назад", callback_data=AdminCB(action="back"))

    kb.adjust(1)
    return kb.as_markup()



# ─────────────────────────────
# ВЫБОР КАТЕГОРИИ ПРИ ДОБАВЛЕНИИ ТОВАРА
# ─────────────────────────────
def choose_category_kb(categories):
    kb = InlineKeyboardBuilder()

    for c in categories:
        kb.button(
            text=c["title"],
            callback_data=AdminCB(
                action="choose_category",
                category_id=c["id"]
            )
        )

    kb.adjust(1)
    return kb.as_markup()


# ─────────────────────────────
# ПОДТВЕРЖДЕНИЕ СОЗДАНИЯ ТОВАРА
# ─────────────────────────────
def confirm_product_kb():
    kb = InlineKeyboardBuilder()

    kb.button(text="✅ Сохранить", callback_data=AdminCB(action="confirm"))
    kb.button(text="❌ Отмена", callback_data=AdminCB(action="cancel"))

    kb.adjust(2)
    return kb.as_markup()



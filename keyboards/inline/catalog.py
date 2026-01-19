from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.callbacks import CategoryCB, ProductCB


def categories_kb(categories):
    kb = InlineKeyboardBuilder()

    for c in categories:
        kb.button(
            text=c["title"],
            callback_data=CategoryCB(action="open", category_id=c["id"])
        )

    kb.button(text="⬅️ В меню", callback_data="menu:menu")
    kb.adjust(1)
    return kb.as_markup()


def products_kb(products, category_id: int):
    kb = InlineKeyboardBuilder()

    for p in products:
        if p["qty"] > 0:
            text = f"{p['title']} ({p['qty']} шт) — {p['price']} ₽"
        else:
            text = f"{p['title']} (нет в наличии)"

        kb.button(
            text=text,
            callback_data=ProductCB(action="open", product_id=p["id"])
        )

    kb.button(
        text="⬅️ В категории",
        callback_data=CategoryCB(action="to_categories", category_id=None)
    )

    kb.adjust(1)
    return kb.as_markup()


def product_card_kb(product_id: int, category_id: int, qty: int):
    kb = InlineKeyboardBuilder()

    if qty > 0:
        kb.button(text="🛒 В корзину", callback_data=f"cart:add:{product_id}")

    kb.button(
        text="⬅️ Назад",
        callback_data=CategoryCB(action="open", category_id=category_id)
    )
    kb.button(text="🏠 В меню", callback_data="menu:menu")

    kb.adjust(1)
    return kb.as_markup()



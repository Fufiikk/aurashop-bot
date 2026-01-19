from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from keyboards.inline.catalog import (
    categories_kb,
    products_kb,
    product_card_kb
)
from utils.callbacks import CategoryCB, ProductCB

router = Router()


@router.callback_query(F.data == "menu:catalog")
async def open_catalog(callback: CallbackQuery, category_repo):
    categories = category_repo.get_all()

    await callback.message.edit_text(
        "📂 <b>Каталог</b>\n\nВыберите категорию 👇",
        reply_markup=categories_kb(categories),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(CategoryCB.filter(F.action == "open"))
async def open_category(
    callback: CallbackQuery,
    callback_data: CategoryCB,
    catalog_service,
    product_item_repo
):
    products = catalog_service.get_by_category(callback_data.category_id)

    # 🔥 добавляем количество
    products_with_qty = []
    for p in products:
        qty = product_item_repo.count_free(p["id"])
        p = dict(p)
        p["qty"] = qty
        products_with_qty.append(p)

    try:
        await callback.message.edit_text(
            "📦 <b>Товары</b>",
            reply_markup=products_kb(products_with_qty, callback_data.category_id),
            parse_mode="HTML"
        )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            await callback.answer("ℹ️ Вы уже в этой категории")
            return
        raise

    await callback.answer()


@router.callback_query(ProductCB.filter(F.action == "open"))
async def open_product(
    callback: CallbackQuery,
    callback_data: ProductCB,
    catalog_service,
    product_item_repo
):
    product = catalog_service.get_by_id(callback_data.product_id)
    qty = product_item_repo.count_free(product["id"])

    text = (
        f"✏️ Название: <b>{product['title']}</b>\n\n〰️〰️〰️〰️〰️〰️〰️\n"
        f"📝 Описание: {product['description']}\n\n〰️〰️〰️〰️〰️〰️〰️\n"
        f"💰 <b>{product['price']} ₽</b>\n〰️〰️〰️〰️〰️〰️〰️\n"
        f"📦 <b>В наличии:</b> {qty} шт"
    )

    await callback.message.edit_text(
        text,
        reply_markup=product_card_kb(
            product_id=product["id"],
            category_id=product["category_id"],
            qty=qty
        ),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(CategoryCB.filter(F.action == "to_categories"))
async def back_to_categories(
    callback: CallbackQuery,
    category_repo
):
    categories = category_repo.get_all()

    await callback.message.edit_text(
        "📂 <b>Каталог</b>\n\nВыберите категорию 👇",
        reply_markup=categories_kb(categories),
        parse_mode="HTML"
    )
    await callback.answer()


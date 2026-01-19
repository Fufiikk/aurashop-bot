from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from keyboards.inline.admin import (
    AdminCB,
    admin_products_kb,
    admin_menu_kb,
)
from states.admin import AddProductItem

router = Router()


@router.callback_query(AdminCB.filter(F.action == "products"))
async def show_products(callback: CallbackQuery, admin_product_repo, config):
    if callback.from_user.id not in config.admin_ids:
        await callback.answer("⛔ Нет доступа", show_alert=True)
        return

    products = admin_product_repo.list_all()

    try:
        await callback.message.edit_text(
            text="📦 <b>Все товары</b>",
            reply_markup=admin_products_kb(products),
            parse_mode="HTML"
        )
    except TelegramBadRequest:
        pass

    await callback.answer()


@router.callback_query(AdminCB.filter(F.action == "toggle"))
async def toggle_product(
    callback: CallbackQuery,
    callback_data: AdminCB,
    admin_product_repo,
    config
):
    if callback.from_user.id not in config.admin_ids:
        await callback.answer("⛔ Нет доступа", show_alert=True)
        return

    admin_product_repo.toggle_active(callback_data.product_id)
    products = admin_product_repo.list_all()

    await callback.message.edit_text(
        "📦 <b>Все товары</b>",
        reply_markup=admin_products_kb(products),
        parse_mode="HTML"
    )
    await callback.answer()


# ─────────────────────────────
# ➕ ДОБАВЛЕНИЕ ВЫДАЧИ
# ─────────────────────────────
@router.callback_query(AdminCB.filter(F.action == "add_item"))
async def start_add_item(
    callback: CallbackQuery,
    callback_data: AdminCB,
    state: FSMContext,
    config
):
    if callback.from_user.id not in config.admin_ids:
        await callback.answer("⛔ Нет доступа", show_alert=True)
        return

    await state.set_state(AddProductItem.content)
    await state.update_data(product_id=callback_data.product_id)

    await callback.message.edit_text(
        "📦 <b>Добавление выдачи</b>\n\n"
        "Отправьте <b>текст</b> или <b>файл</b>, который будет выдан покупателю.",
        parse_mode="HTML"
    )
    await callback.answer()


@router.message(AddProductItem.content)
async def save_product_item(
    message: Message,
    state: FSMContext,
    product_item_repo
):
    data = await state.get_data()
    product_id = data["product_id"]

    # текст
    if message.text:
        product_item_repo.add(
            product_id=product_id,
            type_="text",
            content=message.text
        )

    # файл
    elif message.document:
        product_item_repo.add(
            product_id=product_id,
            type_="file",
            content=message.document.file_id
        )

    else:
        await message.answer("❌ Отправьте текст или файл")
        return

    await state.clear()

    await message.answer(
        "✅ <b>Выдача добавлена</b>\n"
        "Вы можете добавить ещё или вернуться назад.",
        reply_markup=admin_menu_kb(),
        parse_mode="HTML"
    )


@router.callback_query(AdminCB.filter(F.action == "back"))
async def back_to_admin_menu(callback: CallbackQuery, config):
    if callback.from_user.id not in config.admin_ids:
        await callback.answer("⛔ Нет доступа", show_alert=True)
        return

    await callback.message.edit_text(
        "🛠 <b>Админ-панель</b>\n\nВыберите действие 👇",
        reply_markup=admin_menu_kb(),
        parse_mode="HTML"
    )
    await callback.answer()

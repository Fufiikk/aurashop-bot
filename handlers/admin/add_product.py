from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from states.admin import AddProduct
from keyboards.inline.admin import (
    choose_category_kb,
    confirm_product_kb,
    AdminCB,
    admin_menu_kb
)

router = Router()


# ─────────────────────────────
# СТАРТ ДОБАВЛЕНИЯ ТОВАРА
# ─────────────────────────────
@router.callback_query(AdminCB.filter(F.action == "add"))
async def start_add_product(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(AddProduct.title)

    await callback.message.edit_text(
        "➕ <b>Добавление товара</b>\n\nВведите название товара:",
        parse_mode="HTML"
    )
    await callback.answer()


# ─────────────────────────────
# НАЗВАНИЕ
# ─────────────────────────────
@router.message(StateFilter(AddProduct.title))
async def add_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await state.set_state(AddProduct.description)
    await message.answer("✏️ Введите описание товара:")


# ─────────────────────────────
# ОПИСАНИЕ
# ─────────────────────────────
@router.message(StateFilter(AddProduct.description))
async def add_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text.strip())
    await state.set_state(AddProduct.price)
    await message.answer("💰 Введите цену товара (числом):")


# ─────────────────────────────
# ЦЕНА → КАТЕГОРИЯ
# ─────────────────────────────
@router.message(StateFilter(AddProduct.price))
async def add_price(message: Message, state: FSMContext, category_repo):
    if not message.text.isdigit():
        await message.answer("❌ Цена должна быть числом")
        return

    await state.update_data(price=int(message.text))
    await state.set_state(AddProduct.category)

    categories = category_repo.get_all()

    await message.answer(
        "📂 Выберите категорию:",
        reply_markup=choose_category_kb(categories)
    )


# ─────────────────────────────
# КАТЕГОРИЯ → ПОДТВЕРЖДЕНИЕ
# ─────────────────────────────
@router.callback_query(
    StateFilter(AddProduct.category),
    AdminCB.filter(F.action == "choose_category")
)
async def choose_category(
    callback: CallbackQuery,
    callback_data: AdminCB,
    state: FSMContext
):
    await state.update_data(category_id=callback_data.category_id)
    await state.set_state(AddProduct.confirm)

    data = await state.get_data()

    await callback.message.edit_text(
        text=(
            "👀 <b>Предпросмотр товара</b>\n\n"
            f"📦 <b>{data['title']}</b>\n\n"
            f"{data['description']}\n\n"
            f"💰 <b>{data['price']} ₽</b>\n\n"
            "После сохранения вы добавите выдачу."
        ),
        reply_markup=confirm_product_kb(),
        parse_mode="HTML"
    )
    await callback.answer()


# ─────────────────────────────
# СОХРАНИТЬ ТОВАР → ВЫДАЧА
# ─────────────────────────────
@router.callback_query(
    StateFilter(AddProduct.confirm),
    AdminCB.filter(F.action == "confirm")
)
async def confirm_product(
    callback: CallbackQuery,
    state: FSMContext,
    admin_product_repo
):
    data = await state.get_data()

    product_id = admin_product_repo.create(
        title=data["title"],
        description=data["description"],
        price=data["price"],
        category_id=data["category_id"],
        is_active=True
    )

    # 🔥 ПЕРЕХОДИМ В DELIVERY STATE
    await state.clear()
    await state.set_state(AddProduct.delivery)
    await state.update_data(product_id=product_id)

    await callback.message.edit_text(
        "✅ <b>Товар создан</b>\n\n"
        "📦 Теперь отправьте <b>текст или файл</b> для выдачи товара.",
        parse_mode="HTML"
    )
    await callback.answer()


# ─────────────────────────────
# ❌ ОТМЕНА
# ─────────────────────────────
@router.callback_query(
    StateFilter(AddProduct.confirm),
    AdminCB.filter(F.action == "cancel")
)
async def cancel_add_product(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "❌ Добавление товара отменено",
        reply_markup=admin_menu_kb(),
        parse_mode="HTML"
    )
    await callback.answer()


# ─────────────────────────────
# ВЫДАЧА: ТЕКСТ
# ─────────────────────────────
@router.message(StateFilter(AddProduct.delivery), F.text)
async def add_delivery_text(
    message: Message,
    state: FSMContext,
    product_item_repo
):
    data = await state.get_data()
    product_id = data["product_id"]

    product_item_repo.add(
        product_id=product_id,
        type_="text",
        content=message.text
    )

    await state.clear()
    await message.answer(
        "📦 <b>Выдача добавлена (текст)</b>",
        reply_markup=admin_menu_kb(),
        parse_mode="HTML"
    )


# ─────────────────────────────
# ВЫДАЧА: ФАЙЛ
# ─────────────────────────────
@router.message(
    StateFilter(AddProduct.delivery),
    F.document | F.photo | F.video
)
async def add_delivery_file(
    message: Message,
    state: FSMContext,
    product_item_repo
):
    data = await state.get_data()
    product_id = data["product_id"]

    file_id = (
        message.document.file_id
        if message.document
        else message.photo[-1].file_id
        if message.photo
        else message.video.file_id
    )

    product_item_repo.add(
        product_id=product_id,
        type_="file",
        content=file_id
    )

    await state.clear()
    await message.answer(
        "📦 <b>Выдача добавлена (файл)</b>",
        reply_markup=admin_menu_kb(),
        parse_mode="HTML"
    )




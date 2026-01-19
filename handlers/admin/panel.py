from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline.admin import AdminCB
from states.admin import AddProduct

router = Router()


@router.callback_query(
    AdminCB.filter(F.action == "add")
)
async def admin_add_product(
    callback: CallbackQuery,
    callback_data: AdminCB,
    config,
    state: FSMContext
):
    if callback.from_user.id not in config.admin_ids:
        await callback.answer("⛔ Нет доступа", show_alert=True)
        return

    await state.clear()
    await state.set_state(AddProduct.title)

    await callback.message.edit_text(
        text="➕ <b>Добавление товара</b>\n\nВведите название товара:",
        parse_mode="HTML"
    )
    await callback.answer()


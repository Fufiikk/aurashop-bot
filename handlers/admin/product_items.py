from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

router = Router()


class AddItemState(StatesGroup):
    waiting_content = State()


@router.callback_query(F.data.startswith("admin:add_item:"))
async def start_add_item(callback: CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split(":")[-1])

    await state.set_state(AddItemState.waiting_content)
    await state.update_data(product_id=product_id)

    await callback.message.edit_text(
        "📦 <b>Добавление выдачи</b>\n\n"
        "Отправь:\n"
        "• текст (ключ)\n"
        "• или файл",
        parse_mode="HTML"
    )
    await callback.answer()


@router.message(AddItemState.waiting_content)
async def save_item(
    message: Message,
    state: FSMContext,
    product_item_repo
):
    data = await state.get_data()
    product_id = data["product_id"]

    # файл
    if message.document:
        product_item_repo.add_file(
            product_id,
            message.document.file_id
        )
        await message.answer("✅ Файл добавлен")

    # текст
    else:
        product_item_repo.add_text(
            product_id,
            message.text.strip()
        )
        await message.answer("✅ Текст добавлен")

    await state.clear()

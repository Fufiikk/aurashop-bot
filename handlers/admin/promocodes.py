from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.inline.common import back_to_menu_kb

router = Router()


class PromoAdminState(StatesGroup):
    code = State()
    amount = State()


# ─────────────────────────────
# ОТКРЫТЬ МЕНЮ ПРОМОКОДОВ
# ─────────────────────────────
@router.callback_query(F.data == "admin:promos")
async def promo_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.edit_text(
        "🎟 <b>Промокоды</b>\n\n"
        "Отправьте код нового промокода",
        reply_markup=back_to_menu_kb(),
        parse_mode="HTML"
    )
    await callback.answer()

    await state.set_state(PromoAdminState.code)


# ─────────────────────────────
# ВВОД КОДА
# ─────────────────────────────
@router.message(PromoAdminState.code)
async def promo_code(message: Message, state: FSMContext):
    code = message.text.strip().upper()

    if len(code) < 3:
        await message.answer("❌ Код слишком короткий")
        return

    await state.update_data(code=code)
    await state.set_state(PromoAdminState.amount)

    await message.answer("💰 Введите сумму начисления:")


# ─────────────────────────────
# ВВОД СУММЫ
# ─────────────────────────────
@router.message(PromoAdminState.amount)
async def promo_amount(message: Message, state: FSMContext, promo_repo):
    try:
        amount = int(message.text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Введите корректную сумму")
        return

    data = await state.get_data()
    code = data["code"]

    promo_repo.create(code, amount)

    await message.answer(
        f"✅ <b>Промокод создан</b>\n\n"
        f"Код: <code>{code}</code>\n"
        f"Сумма: <b>{amount} ₽</b>",
        reply_markup=back_to_menu_kb(),
        parse_mode="HTML"
    )

    # 🔥 ВОТ ЭТО РЕАЛЬНО КОНЕЦ FSM
    await state.clear()



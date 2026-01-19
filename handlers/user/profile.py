from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.inline.profile import profile_kb
from keyboards.inline.common import back_to_menu_kb

router = Router()


class PromoState(StatesGroup):
    enter_code = State()


@router.callback_query(F.data == "menu:profile")
async def open_profile(callback: CallbackQuery, user_service):
    user = user_service.get_or_create(
        callback.from_user.id,
        callback.from_user.first_name
    )

    await callback.message.edit_text(
        f"👤 <b>Личный кабинет</b>\n\n"
        f"🆔 ID: <code>{user['user_id']}</code>\n"
        f"👋 Имя: <b>{user['first_name']}</b>\n"
        f"💰 Баланс: <b>{user['balance']} ₽</b>",
        reply_markup=profile_kb(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "profile:topup")
async def topup(callback: CallbackQuery):
    await callback.answer("💳 Пополнение в разработке", show_alert=True)


@router.callback_query(F.data == "profile:promo")
async def promo_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PromoState.enter_code)
    await callback.message.edit_text(
        "🎟 <b>Введите промокод:</b>",
        reply_markup=back_to_menu_kb(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.message(PromoState.enter_code)
async def promo_apply(
    message: Message,
    state: FSMContext,
    promo_repo,
    user_repo
):
    code = message.text.strip().upper()
    user_id = message.from_user.id

    promo = promo_repo.get(code)

    if not promo:
        await message.answer("❌ Промокод не найден или неактивен")
        return

    if promo_repo.is_used(user_id, code):
        await message.answer("⚠️ Вы уже использовали этот промокод")
        return

    user_repo.add_balance(user_id, promo["amount"])
    promo_repo.mark_used(user_id, code)

    await message.answer(
        f"✅ Промокод применён!\n"
        f"💰 Начислено: {promo['amount']} ₽",
        reply_markup=back_to_menu_kb()
    )

    await state.clear()


@router.callback_query(F.data == "profile:ref")
async def profile_referrals(
    callback: CallbackQuery,
    referral_repo,
    config
):
    user_id = callback.from_user.id
    count = referral_repo.count_referrals(user_id)
    referrals = referral_repo.get_referrals(user_id)

    link = f"https://t.me/{config.bot_username}?start=ref_{user_id}"

    text = (
        "👥 <b>Реферальная система</b>\n\n"
        f"🔗 <b>Ваша ссылка:</b>\n<code>{link}</code>\n\n"
        f"📊 <b>Прогресс:</b> {count} / 5\n"
        "🎁 <b>Награда:</b> 50 ₽\n\n"
    )

    if referrals:
        text += "<b>👤 Приглашённые:</b>\n"
        for r in referrals:
            text += f"• {r['first_name']} (<code>{r['user_id']}</code>)\n"
    else:
        text += "Пока никто не перешёл по ссылке 😔"

    await callback.message.edit_text(
        text,
        reply_markup=back_to_menu_kb(),
        parse_mode="HTML"
    )
    await callback.answer()


from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from keyboards.inline.start import start_menu
from keyboards.inline.common import back_to_menu_kb
from keyboards.inline.admin import admin_menu_kb

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, config, user_repo, referral_repo):
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    # создаём пользователя
    user_repo.get_or_create(user_id, first_name)

    # реферальный старт
    if message.text.startswith("/start ref_"):
        try:
            referrer_id = int(message.text.split("ref_")[1])
        except ValueError:
            referrer_id = None

        if referrer_id and referrer_id != user_id:
            added = referral_repo.add(referrer_id, user_id)

            if added:
                count = referral_repo.count_referrals(referrer_id)

                if count >= 5 and not referral_repo.reward_received(referrer_id):
                    user_repo.add_balance(referrer_id, 50)
                    referral_repo.mark_reward_received(referrer_id)

    is_admin = user_id in config.admin_ids

    await message.answer(
        "<b>🎁 Добро пожаловать в магазин</b>\n\nПокупайте • Приглашайте • Получайте бонусы\n\nНачните с меню ниже ⬇️",
        reply_markup=start_menu(is_admin),
        parse_mode="HTML"
    )



@router.callback_query(F.data == "menu:menu")
async def back_to_menu(callback: CallbackQuery, config):
    is_admin = callback.from_user.id in config.admin_ids

    await callback.message.edit_text(
        "<b>🎁 Добро пожаловать в магазин</b>\n\nПокупайте • Приглашайте • Получайте бонусы\n\nНачните с меню ниже ⬇️",
        reply_markup=start_menu(is_admin),
        parse_mode="HTML"
    )
    await callback.answer()


# @router.callback_query(F.data == "menu:profile")
# async def profile(callback: CallbackQuery):
#     await callback.message.edit_text(
#         f"👤 <b>Личный кабинет</b>\n\nID: <code>{callback.from_user.id}</code>",
#         reply_markup=back_to_menu_kb(),
#         parse_mode="HTML"
#     )
#     await callback.answer()


@router.callback_query(F.data == "menu:admin")
async def admin(callback: CallbackQuery, config):
    if callback.from_user.id not in config.admin_ids:
        await callback.answer("⛔ Нет доступа", show_alert=True)
        return

    await callback.message.edit_text(
        "🛠 <b>Админ-панель</b>",
        reply_markup=admin_menu_kb(),
        parse_mode="HTML"
    )
    await callback.answer()




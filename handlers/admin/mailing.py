from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from states.admin import MailingState
from keyboards.inline.common import back_to_menu_kb

router = Router()


@router.callback_query(F.data == "admin:mailing")
async def start_mailing(callback: CallbackQuery, state: FSMContext, config):
    if callback.from_user.id not in config.admin_ids:
        await callback.answer("⛔ Нет доступа", show_alert=True)
        return

    await state.set_state(MailingState.text)

    await callback.message.edit_text(
        "📢 <b>Рассылка</b>\n\n"
        "Отправьте текст, который нужно разослать всем пользователям:",
        reply_markup=back_to_menu_kb(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.message(MailingState.text)
async def process_mailing(
    message: Message,
    state: FSMContext,
    bot,
    user_repo,
    config
):
    if message.from_user.id not in config.admin_ids:
        return

    text = message.text
    users = user_repo.get_all_ids()

    sent = 0
    failed = 0

    await message.answer("⏳ Начинаю рассылку...")

    for user_id in users:
        try:
            await bot.send_message(
                user_id,
                text,
                parse_mode="HTML"
            )
            sent += 1
        except Exception:
            failed += 1

    await message.answer(
        f"✅ <b>Рассылка завершена</b>\n\n"
        f"📤 Отправлено: <b>{sent}</b>\n"
        f"❌ Ошибок: <b>{failed}</b>",
        reply_markup=back_to_menu_kb(),
        parse_mode="HTML"
    )

    await state.clear()

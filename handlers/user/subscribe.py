from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.inline.start import start_menu

router = Router()


@router.callback_query(F.data == "check_sub")
async def check_sub(callback: CallbackQuery, config, bot):
    user_id = callback.from_user.id
    is_admin = user_id in config.admin_ids

    try:
        member = await bot.get_chat_member(
            chat_id=config.channel_id,
            user_id=user_id
        )

        if member.status in ("member", "administrator", "creator"):
            await callback.message.edit_text(
                "✅ <b>Подписка подтверждена</b>\n\nДобро пожаловать 👇",
                reply_markup=start_menu(is_admin),
                parse_mode="HTML"
            )
            await callback.answer()
            return

    except:
        pass

    await callback.answer("❌ Вы не подписаны", show_alert=True)

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest


ALLOWED_CALLBACKS = {
    "check_sub",
    "menu:menu",
}


class SubscribeMiddleware(BaseMiddleware):
    def __init__(self, channel_id: int, channel_link: str):
        self.channel_id = channel_id
        self.channel_link = channel_link

    async def __call__(self, handler, event, data):
        bot = data["bot"]

        # ───────────── USER ID ─────────────
        if isinstance(event, Message):
            user_id = event.from_user.id

            # ✅ /start всегда разрешён
            if event.text and event.text.startswith("/start"):
                return await handler(event, data)

        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id

            # ✅ разрешённые callback
            if event.data in ALLOWED_CALLBACKS:
                return await handler(event, data)

        else:
            return await handler(event, data)

        # ───────────── CHECK SUB ─────────────
        try:
            member = await bot.get_chat_member(
                chat_id=self.channel_id,
                user_id=user_id
            )

            if member.status in ("member", "administrator", "creator"):
                return await handler(event, data)

        except TelegramBadRequest:
            pass

        # ───────────── NOT SUBSCRIBED ─────────────
        from keyboards.inline.subscribe import subscribe_kb

        text = (
            "🚫 <b>Доступ ограничен</b>\n\n"
            "Подпишитесь на канал, чтобы пользоваться ботом 👇"
        )

        if isinstance(event, Message):
            await event.answer(
                text,
                reply_markup=subscribe_kb(self.channel_link),
                parse_mode="HTML"
            )

        elif isinstance(event, CallbackQuery):
            await event.message.edit_text(
                text,
                reply_markup=subscribe_kb(self.channel_link),
                parse_mode="HTML"
            )
            await event.answer()

        return

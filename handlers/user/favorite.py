from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()


# ❤️ добавить в избранное
@router.callback_query(F.data.startswith("fav:add:"))
async def add_to_favorite(
    callback: CallbackQuery,
    favorite_service
):
    product_id = int(callback.data.split(":")[-1])

    favorite_service.add(
        user_id=callback.from_user.id,
        product_id=product_id
    )

    await callback.answer("❤️ Добавлено в избранное")


# 💔 удалить из избранного (на будущее)
@router.callback_query(F.data.startswith("fav:remove:"))
async def remove_from_favorite(
    callback: CallbackQuery,
    favorite_service
):
    product_id = int(callback.data.split(":")[-1])

    favorite_service.remove(
        user_id=callback.from_user.id,
        product_id=product_id
    )

    await callback.answer("💔 Удалено из избранного")


from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline.cart import cart_kb

router = Router()


# ─────────────────────────────
# 🛒 ОТКРЫТЬ КОРЗИНУ
# ─────────────────────────────
@router.callback_query(F.data == "menu:cart")
async def open_cart(callback: CallbackQuery, cart_service, user_service):
    user_id = callback.from_user.id

    items = await cart_service.get_cart(user_id)
    balance = user_service.get_balance(user_id)

    if not items:
        await callback.message.edit_text(
            "🛒 <b>Корзина пуста</b>",
            reply_markup=cart_kb(has_items=False),
            parse_mode="HTML"
        )
        await callback.answer()
        return

    total = 0
    text = "🛒 <b>Ваша корзина</b>\n\n"

    for i in items:
        subtotal = i["price"] * i["quantity"]
        total += subtotal
        text += f"• {i['title']} × {i['quantity']} = {subtotal} ₽\n"

    text += f"\n💰 <b>Итого:</b> {total} ₽"
    text += f"\n💳 <b>Баланс:</b> {balance} ₽"

    await callback.message.edit_text(
        text,
        reply_markup=cart_kb(has_items=True),
        parse_mode="HTML"
    )
    await callback.answer()


# ─────────────────────────────
# ➕ ДОБАВИТЬ В КОРЗИНУ
# ─────────────────────────────
@router.callback_query(F.data.startswith("cart:add:"))
async def add_to_cart(callback: CallbackQuery, cart_service):
    product_id = int(callback.data.split(":")[-1])
    await cart_service.add(callback.from_user.id, product_id)
    await callback.answer("✅ Товар добавлен в корзину")


# ─────────────────────────────
# 💳 ОПЛАТА + ВЫДАЧА
# ─────────────────────────────
@router.callback_query(F.data == "cart:pay")
async def pay_cart(
    callback: CallbackQuery,
    cart_service,
    user_service,
    product_item_repo,
    order_repo
):
    user_id = callback.from_user.id
    items = await cart_service.get_cart(user_id)

    if not items:
        await callback.answer("🛒 Корзина пуста", show_alert=True)
        return

    total = sum(i["price"] * i["quantity"] for i in items)
    balance = user_service.get_balance(user_id)

    if balance < total:
        await callback.answer(
            f"❌ Недостаточно средств\nБаланс: {balance} ₽",
            show_alert=True
        )
        return

    # 🔒 ПРОВЕРКА НАЛИЧИЯ ВЫДАЧ
    for i in items:
        free = 0
        for _ in range(i["quantity"]):
            if product_item_repo.get_free_item(i["product_id"]):
                free += 1
        if free < i["quantity"]:
            await callback.answer(
                f"❌ Недостаточно выдачи для «{i['title']}»",
                show_alert=True
            )
            return

    # 💸 СПИСАНИЕ
    user_service.subtract_balance(user_id, total)

    # 📦 ЗАКАЗ
    order_id = order_repo.create(user_id, total)

    await callback.message.answer(
        "🎉 <b>Покупка успешна!</b>\n\n<b>Ваши товары:</b>",
        parse_mode="HTML"
    )

    # 🎁 ВЫДАЧА
    for i in items:
        for _ in range(i["quantity"]):
            item = product_item_repo.get_free_item(i["product_id"])

            if item["type"] == "text":
                await callback.message.answer(item["content"])
            else:
                await callback.message.answer_document(item["content"])

            product_item_repo.mark_used(item["id"])

            order_repo.add_item(
                order_id,
                i["product_id"],
                i["title"],
                i["price"],
                1
            )

    # 🧹 ОЧИСТКА КОРЗИНЫ
    await cart_service.clear(user_id)

    await callback.message.answer(
        "✅ <b>Покупка завершена</b>",
        reply_markup=cart_kb(has_items=False),
        parse_mode="HTML"
    )
    await callback.answer()


# ─────────────────────────────
# 🧹 ОЧИСТИТЬ КОРЗИНУ
# ─────────────────────────────
@router.callback_query(F.data == "cart:clear")
async def clear_cart(callback: CallbackQuery, cart_service):
    await cart_service.clear(callback.from_user.id)
    await callback.message.edit_text(
        "🧹 <b>Корзина очищена</b>",
        reply_markup=cart_kb(has_items=False),
        parse_mode="HTML"
    )
    await callback.answer()

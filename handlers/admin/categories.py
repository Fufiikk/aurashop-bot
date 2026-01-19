from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.inline.admin import AdminCB
from keyboards.inline.admin_categories import admin_categories_kb

router = Router()


# ─────────────────────────────
# FSM
# ─────────────────────────────
class AddCategory(StatesGroup):
    title = State()


# ─────────────────────────────
# 📂 СПИСОК КАТЕГОРИЙ
# ─────────────────────────────
@router.callback_query(AdminCB.filter(F.action == "categories"))
async def admin_categories(
    callback: CallbackQuery,
    category_repo,
    config
):
    if callback.from_user.id not in config.admin_ids:
        await callback.answer("⛔ Нет доступа", show_alert=True)
        return

    categories = category_repo.get_all()

    await callback.message.edit_text(
        "📂 <b>Категории</b>\n\n"
        "Нажмите ❌ чтобы удалить категорию",
        reply_markup=admin_categories_kb(categories),
        parse_mode="HTML"
    )
    await callback.answer()


# ─────────────────────────────
# ➕ ДОБАВИТЬ КАТЕГОРИЮ
# ─────────────────────────────
@router.callback_query(F.data == "admin:cat:add")
async def add_category_start(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.set_state(AddCategory.title)

    await callback.message.edit_text(
        "➕ <b>Добавление категории</b>\n\nВведите название:",
        parse_mode="HTML"
    )
    await callback.answer()


@router.message(AddCategory.title)
async def add_category_finish(
    message: Message,
    state: FSMContext,
    category_repo
):
    category_repo.create(message.text)
    await state.clear()

    await message.answer("✅ Категория добавлена")


# ─────────────────────────────
# ❌ УДАЛИТЬ КАТЕГОРИЮ
# ─────────────────────────────
@router.callback_query(F.data.startswith("admin:cat:delete:"))
async def delete_category(
    callback: CallbackQuery,
    category_repo
):
    category_id = int(callback.data.split(":")[-1])
    category_repo.delete(category_id)

    await callback.answer("❌ Категория удалена", show_alert=True)

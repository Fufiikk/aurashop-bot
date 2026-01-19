from aiogram.filters.callback_data import CallbackData


class CategoryCB(CallbackData, prefix="cat"):
    action: str  # open | to_categories
    category_id: int | None


class ProductCB(CallbackData, prefix="prod"):
    action: str
    product_id: int


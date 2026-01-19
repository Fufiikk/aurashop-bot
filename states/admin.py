from aiogram.fsm.state import StatesGroup, State


class AddProduct(StatesGroup):
    title = State()
    description = State()
    price = State()
    category = State()   # ← ВАЖНО: ЭТОГО НЕ ХВАТАЛО
    delivery = State()
    confirm = State()



class MailingState(StatesGroup):
    text = State()

class AddProductItem(StatesGroup):
    content = State()
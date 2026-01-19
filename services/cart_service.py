class CartService:
    def __init__(self, cart_repo):
        self.cart_repo = cart_repo

    async def is_in_cart(self, user_id: int, product_id: int) -> bool:
        return self.cart_repo.exists(user_id, product_id)

    async def toggle(self, user_id: int, product_id: int) -> bool:
        if self.cart_repo.exists(user_id, product_id):
            self.cart_repo.remove(user_id, product_id)
            return False
        self.cart_repo.add(user_id, product_id)
        return True

    async def increment(self, user_id: int, product_id: int):
        self.cart_repo.add(user_id, product_id)

    async def decrement(self, user_id: int, product_id: int):
        self.cart_repo.decrement(user_id, product_id)

    async def remove(self, user_id: int, product_id: int):
        self.cart_repo.remove(user_id, product_id)

    async def get_cart(self, user_id: int):
        return self.cart_repo.get_cart(user_id)

    async def clear(self, user_id: int):
        self.cart_repo.clear(user_id)

    async def add(self, user_id: int, product_id: int):
        self.cart_repo.add(user_id, product_id)

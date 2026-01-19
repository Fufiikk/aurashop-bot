class FavoriteService:
    def __init__(self, favorite_repo):
        self.favorite_repo = favorite_repo

    async def is_favorite(self, user_id: int, product_id: int) -> bool:
        return self.favorite_repo.exists(user_id, product_id)

    async def toggle(self, user_id: int, product_id: int) -> bool:
        if self.favorite_repo.exists(user_id, product_id):
            self.favorite_repo.remove(user_id, product_id)
            return False
        self.favorite_repo.add(user_id, product_id)
        return True

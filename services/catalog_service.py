class CatalogService:
    def __init__(self, product_repo):
        self.product_repo = product_repo

    def get_by_category(self, category_id: int):
        """
        Вернуть все активные товары в категории
        """
        return self.product_repo.get_by_category(category_id)

    def get_by_id(self, product_id: int):
        """
        Вернуть товар по ID
        """
        return self.product_repo.get_by_id(product_id)


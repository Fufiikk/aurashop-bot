class UserService:
    def __init__(self, repo):
        self.repo = repo

    def get_or_create(self, user_id: int, first_name: str):
        return self.repo.get_or_create(user_id, first_name)

    def get_balance(self, user_id: int) -> int:
        return self.repo.get_balance(user_id)

    def add_balance(self, user_id: int, amount: int):
        self.repo.add_balance(user_id, amount)

    def subtract_balance(self, user_id: int, amount: int):
        balance = self.get_balance(user_id)
        if balance < amount:
            raise ValueError("Недостаточно средств")
        self.repo.subtract_balance(user_id, amount)

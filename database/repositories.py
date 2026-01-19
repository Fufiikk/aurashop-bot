# database/repositories.py

# ─────────────────────────────
# PRODUCTS (USER)
# ─────────────────────────────
class ProductRepository:
    def __init__(self, db):
        self.db = db

    def get_by_category(self, category_id: int):
        return self.db.fetchall(
            """
            SELECT id, title, description, price, category_id
            FROM products
            WHERE category_id = ? AND is_active = 1
            ORDER BY id DESC
            """,
            (category_id,)
        )

    def get_by_id(self, product_id: int):
        return self.db.fetchone(
            """
            SELECT id, title, description, price, category_id
            FROM products
            WHERE id = ? AND is_active = 1
            """,
            (product_id,)
        )


# ─────────────────────────────
# CART
# ─────────────────────────────
class CartRepository:
    def __init__(self, db):
        self.db = db

    def add(self, user_id: int, product_id: int):
        self.db.execute(
            """
            INSERT INTO cart (user_id, product_id, quantity)
            VALUES (?, ?, 1)
            ON CONFLICT(user_id, product_id)
            DO UPDATE SET quantity = quantity + 1
            """,
            (user_id, product_id)
        )

    def get_cart(self, user_id: int):
        return self.db.fetchall(
            """
            SELECT
                c.product_id,
                c.quantity,
                p.title,
                p.price
            FROM cart c
            JOIN products p ON p.id = c.product_id
            WHERE c.user_id = ?
            """,
            (user_id,)
        )

    def clear(self, user_id: int):
        self.db.execute(
            "DELETE FROM cart WHERE user_id=?",
            (user_id,)
        )


# ─────────────────────────────
# ADMIN PRODUCTS
# ─────────────────────────────
class AdminProductRepository:
    def __init__(self, db):
        self.db = db

    def create(
        self,
        title: str,
        description: str,
        price: int,
        category_id: int,
        is_active: bool = True
    ) -> int:
        cur = self.db.execute(
            """
            INSERT INTO products (
                title,
                description,
                price,
                category_id,
                is_active
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (title, description, price, category_id, int(is_active))
        )
        return cur.lastrowid

    def list_all(self):
        return self.db.fetchall(
            """
            SELECT id, title, price, is_active
            FROM products
            ORDER BY id DESC
            """
        )

    def toggle_active(self, product_id: int):
        self.db.execute(
            """
            UPDATE products
            SET is_active = CASE is_active
                WHEN 1 THEN 0
                ELSE 1
            END
            WHERE id = ?
            """,
            (product_id,)
        )


# ─────────────────────────────
# CATEGORIES
# ─────────────────────────────
class CategoryRepository:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        return self.db.fetchall(
            "SELECT id, title FROM categories ORDER BY id"
        )

    def create(self, title: str):
        self.db.execute(
            "INSERT INTO categories (title) VALUES (?)",
            (title,)
        )

    def delete(self, category_id: int):
        self.db.execute(
            "DELETE FROM categories WHERE id = ?",
            (category_id,)
        )


# ─────────────────────────────
# PRODUCT ITEMS (ВЫДАЧА)
# ─────────────────────────────
class ProductItemRepository:
    def __init__(self, db):
        self.db = db

    def add(self, product_id: int, type_: str, content: str):
        self.db.execute(
            """
            INSERT INTO product_items (
                product_id,
                type,
                content,
                is_used
            )
            VALUES (?, ?, ?, 0)
            """,
            (product_id, type_, content)
        )

    def get_free_item(self, product_id: int):
        return self.db.fetchone(
            """
            SELECT id, type, content
            FROM product_items
            WHERE product_id = ? AND is_used = 0
            LIMIT 1
            """,
            (product_id,)
        )

    def mark_used(self, item_id: int):
        self.db.execute(
            "UPDATE product_items SET is_used = 1 WHERE id = ?",
            (item_id,)
        )

    # 🔥 ВАЖНО: КОЛИЧЕСТВО ДОСТУПНЫХ ВЫДАЧ
    def count_free(self, product_id: int) -> int:
        row = self.db.fetchone(
            """
            SELECT COUNT(*) AS cnt
            FROM product_items
            WHERE product_id = ? AND is_used = 0
            """,
            (product_id,)
        )
        return row["cnt"] if row else 0


# ─────────────────────────────
# USERS
# ─────────────────────────────
class UserRepository:
    def __init__(self, db):
        self.db = db

    def get_or_create(self, user_id: int, first_name: str):
        user = self.db.fetchone(
            "SELECT user_id, first_name, balance FROM users WHERE user_id=?",
            (user_id,)
        )
        if not user:
            self.db.execute(
                """
                INSERT INTO users (user_id, first_name, balance)
                VALUES (?, ?, 0)
                """,
                (user_id, first_name)
            )
            return {
                "user_id": user_id,
                "first_name": first_name,
                "balance": 0
            }
        return user

    def get_balance(self, user_id: int) -> int:
        row = self.db.fetchone(
            "SELECT balance FROM users WHERE user_id=?",
            (user_id,)
        )
        return row["balance"] if row else 0

    def add_balance(self, user_id: int, amount: int):
        self.db.execute(
            "UPDATE users SET balance = balance + ? WHERE user_id=?",
            (amount, user_id)
        )

    def subtract_balance(self, user_id: int, amount: int):
        self.db.execute(
            "UPDATE users SET balance = balance - ? WHERE user_id=?",
            (amount, user_id)
        )

    def get_all_ids(self):
        rows = self.db.fetchall("SELECT user_id FROM users")
        return [row["user_id"] for row in rows]


# ─────────────────────────────
# PROMOCODES
# ─────────────────────────────
class PromoRepository:
    def __init__(self, db):
        self.db = db

    def get(self, code: str):
        return self.db.fetchone(
            "SELECT code, amount FROM promocodes WHERE code=? AND is_active=1",
            (code.upper(),)
        )

    def create(self, code: str, amount: int):
        self.db.execute(
            "INSERT INTO promocodes (code, amount) VALUES (?, ?)",
            (code.upper(), amount)
        )

    def delete(self, code: str):
        self.db.execute(
            "DELETE FROM promocodes WHERE code=?",
            (code.upper(),)
        )

    def is_used(self, user_id: int, code: str) -> bool:
        row = self.db.fetchone(
            "SELECT 1 FROM promocode_uses WHERE user_id=? AND code=?",
            (user_id, code.upper())
        )
        return row is not None

    def mark_used(self, user_id: int, code: str):
        self.db.execute(
            "INSERT INTO promocode_uses (user_id, code) VALUES (?, ?)",
            (user_id, code.upper())
        )


# ─────────────────────────────
# ORDERS
# ─────────────────────────────
class OrderRepository:
    def __init__(self, db):
        self.db = db

    def create(self, user_id: int, total: int) -> int:
        cur = self.db.execute(
            "INSERT INTO orders (user_id, total) VALUES (?, ?)",
            (user_id, total)
        )
        return cur.lastrowid

    def add_item(
        self,
        order_id: int,
        product_id: int,
        title: str,
        price: int,
        quantity: int
    ):
        self.db.execute(
            """
            INSERT INTO order_items
            (order_id, product_id, title, price, quantity)
            VALUES (?, ?, ?, ?, ?)
            """,
            (order_id, product_id, title, price, quantity)
        )

# ─────────────────────────────
# REFERRALS
# ─────────────────────────────
class ReferralRepository:
    def __init__(self, db):
        self.db = db

    def add(self, referrer_id: int, referred_id: int) -> bool:
        """
        Добавляет реферала.
        Возвращает False, если пользователь уже был приглашён.
        """
        try:
            self.db.execute(
                """
                INSERT INTO referrals (referrer_id, referred_id)
                VALUES (?, ?)
                """,
                (referrer_id, referred_id)
            )
            return True
        except Exception:
            return False

    def count_referrals(self, referrer_id: int) -> int:
        row = self.db.fetchone(
            "SELECT COUNT(*) AS cnt FROM referrals WHERE referrer_id=?",
            (referrer_id,)
        )
        return row["cnt"] if row else 0

    def get_referrals(self, referrer_id: int):
        return self.db.fetchall(
            """
            SELECT u.user_id, u.first_name
            FROM referrals r
            JOIN users u ON u.user_id = r.referred_id
            WHERE r.referrer_id = ?
            ORDER BY r.created_at DESC
            """,
            (referrer_id,)
        )

    def reward_received(self, user_id: int) -> bool:
        row = self.db.fetchone(
            "SELECT reward_received FROM referral_rewards WHERE user_id=?",
            (user_id,)
        )
        return bool(row and row["reward_received"])

    def mark_reward_received(self, user_id: int):
        self.db.execute(
            """
            INSERT INTO referral_rewards (user_id, reward_received)
            VALUES (?, 1)
            ON CONFLICT(user_id)
            DO UPDATE SET reward_received = 1
            """,
            (user_id,)
        )




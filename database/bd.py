import sqlite3
from pathlib import Path


class Database:
    def __init__(self, path: str):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

    def execute(self, query: str, params: tuple = ()):
        cur = self.conn.cursor()
        cur.execute(query, params)
        self.conn.commit()
        return cur

    def fetchone(self, query: str, params: tuple = ()):
        return self.execute(query, params).fetchone()

    def fetchall(self, query: str, params: tuple = ()):
        return self.execute(query, params).fetchall()

    # 🔥 АВТО-СОЗДАНИЕ ТАБЛИЦ
    def init_schema(self):
        # ───── USERS ─────
        self.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            balance INTEGER DEFAULT 0
        );
        """)

        # ───── CATEGORIES ─────
        self.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        );
        """)

        # ───── PRODUCTS ─────
        self.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL,
            category_id INTEGER,
            is_active INTEGER DEFAULT 1,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        );
        """)

        # ───── CART ─────
        self.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            user_id INTEGER,
            product_id INTEGER,
            quantity INTEGER DEFAULT 1,
            PRIMARY KEY (user_id, product_id)
        );
        """)

        # ───── FAVORITES ─────
        self.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            user_id INTEGER,
            product_id INTEGER,
            PRIMARY KEY (user_id, product_id)
        );
        """)

        # ───── PROMOCODES ─────
        self.execute("""
        CREATE TABLE IF NOT EXISTS promocodes (
            code TEXT PRIMARY KEY,
            amount INTEGER NOT NULL,
            is_active INTEGER DEFAULT 1
        );
        """)

        self.execute("""
        CREATE TABLE IF NOT EXISTS promocode_uses (
            user_id INTEGER,
            code TEXT,
            UNIQUE(user_id, code)
        );
        """)

        # ───── PRODUCT ITEMS (выдача товара) ─────
        self.execute("""
        CREATE TABLE IF NOT EXISTS product_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            type TEXT NOT NULL,          -- text | file
            content TEXT NOT NULL,       -- текст или file_id
            is_used INTEGER DEFAULT 0,
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
        """)

        # ───── ORDERS ─────
        self.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            total INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)

        self.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            order_id INTEGER,
            product_id INTEGER,
            title TEXT,
            price INTEGER,
            quantity INTEGER
        );
        """)
        # ───── REFERRALS ─────
        self.execute("""
        CREATE TABLE IF NOT EXISTS referrals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            referrer_id INTEGER NOT NULL,
            referred_id INTEGER NOT NULL UNIQUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)

        self.execute("""
        CREATE TABLE IF NOT EXISTS referral_rewards (
            user_id INTEGER PRIMARY KEY,
            reward_received INTEGER DEFAULT 0
        );
        """)

    # ───── НАЧАЛЬНЫЕ КАТЕГОРИИ ─────
    def seed_categories(self):
        self.execute(
            "INSERT OR IGNORE INTO categories (id, title) VALUES (1, 'Игры')"
        )
        self.execute(
            "INSERT OR IGNORE INTO categories (id, title) VALUES (2, 'Софт')"
        )
        self.execute(
            "INSERT OR IGNORE INTO categories (id, title) VALUES (3, 'Подписки')"
        )




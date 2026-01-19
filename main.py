import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import load_config
from database.bd import Database
from database.repositories import (
    ProductRepository,
    CartRepository,
    AdminProductRepository,
    CategoryRepository,
)
from services.catalog_service import CatalogService
from services.cart_service import CartService
from services.favorite_service import FavoriteService

from handlers.user import start, catalog, cart, favorite
from handlers.admin import panel, add_product, products
from database.repositories import UserRepository
from services.user_service import UserService
from handlers.admin import categories
from handlers.user import profile
from handlers.admin import promocodes
from database.repositories import PromoRepository
from middlewares.subscribe import SubscribeMiddleware
from handlers.user import subscribe
from handlers.admin import mailing
from database.repositories import ProductItemRepository, OrderRepository
from database.repositories import ProductItemRepository
from database.repositories import ReferralRepository

CHANNEL_LINK = "https://t.me/anal99i"

async def main():
    logging.basicConfig(level=logging.INFO)

    # ─────────────────────────────
    # CONFIG
    # ─────────────────────────────
    config = load_config()

    bot = Bot(token=config.bot_token, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())

    # ─────────────────────────────
    # DATABASE
    # ─────────────────────────────
    db = Database("data/shop.db")
    db.init_schema()



    # router

    # ─────────────────────────────
    # REPOSITORIES
    # ─────────────────────────────
    product_repo = ProductRepository(db)
    admin_product_repo = AdminProductRepository(db)
    cart_repo = CartRepository(db)

    category_repo = CategoryRepository(db)
    promo_repo = PromoRepository(db)
    # ─────────────────────────────
    # SERVICES
    # ─────────────────────────────
    catalog_service = CatalogService(product_repo)
    cart_service = CartService(cart_repo)

    product_item_repo = ProductItemRepository(db)
    order_repo = OrderRepository(db)
    referral_repo = ReferralRepository(db)
    # ─────────────────────────────
    # DEPENDENCY INJECTION
    # ─────────────────────────────
    dp["config"] = config
    dp["category_repo"] = category_repo
    dp["catalog_service"] = catalog_service
    dp["cart_service"] = cart_service

    dp["admin_product_repo"] = admin_product_repo
    dp["user_service"] = UserService(UserRepository(db))
    dp["promo_repo"] = promo_repo
    dp["user_repo"] = UserRepository(db)
    dp["product_item_repo"] = product_item_repo
    dp["order_repo"] = order_repo
    dp["referral_repo"] = referral_repo
    # ─────────────────────────────
    # ROUTERS (ПОРЯДОК ВАЖЕН)
    # ─────────────────────────────
    # FSM / ADMIN
    # ───────────── MIDDLEWARE ─────────────
    dp.message.middleware(
        SubscribeMiddleware(
            channel_id=config.channel_id,
            channel_link=CHANNEL_LINK
        )
    )

    dp.callback_query.middleware(
        SubscribeMiddleware(
            channel_id=config.channel_id,
            channel_link=CHANNEL_LINK
        )
    )

    # ───────────── ROUTERS ─────────────
    dp.include_router(subscribe.router)

    dp.include_router(add_product.router)
    dp.include_router(panel.router)
    dp.include_router(products.router)

    dp.include_router(start.router)
    dp.include_router(catalog.router)
    dp.include_router(cart.router)
    dp.include_router(favorite.router)
    dp.include_router(categories.router)
    dp.include_router(profile.router)
    dp.include_router(promocodes.router)
    dp.include_router(mailing.router)

    # ─────────────────────────────
    # START
    # ─────────────────────────────
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


import asyncio
from handlers.start import start_router
from handlers.myinfo import myinfo_router
from handlers.random import random_router
from handlers.opros import opros_router
from handlers.review_dialog import review_router
from config import dp, bot, database
from handlers.admin_dishes import admin_dishes_router
from handlers.user_dishes import user_dishes_router



async def on_startup(bot):
    database.create_tables()



async def main():
    dp.include_router(start_router)
    dp.include_router(myinfo_router)
    dp.include_router(random_router)
    dp.include_router(opros_router)
    dp.include_router(review_router)
    dp.include_router(admin_dishes_router)
    dp.include_router(user_dishes_router)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

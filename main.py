import asyncio
import logging
from aiogram import Bot, Dispatcher
from app.handlers import router

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token='7312535077:AAGw0PIF2uwtV5gBFaucyNrdcIhf4O1iRXI')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
    

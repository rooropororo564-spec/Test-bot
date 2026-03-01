import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

BOT_TOKEN = "7886729712:AAGOhzgr1V5BFI3Hc8ImeMc4kQXU2LSXUBQ"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! че каво? 👋")

@dp.message()
async def echo(message: types.Message):
    await message.answer("Привет! че каво? 👋")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

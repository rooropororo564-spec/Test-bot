import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

BOT_TOKEN = "7886729712:AAFSUso8QEDKMsyx_1aJc09ZhsPYAKBq9dG4"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Как дела? 👋")

@dp.message()
async def echo(message: types.Message):
    await message.answer("Привет! Как дела? 👋")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

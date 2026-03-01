import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import httpx

BOT_TOKEN = "7886729712:AAGOhzgr1V5BFI3Hc8ImeMc4kQXU2LSXUBQ"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Главное меню
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🐱 Котик", callback_data="cat")],
        [InlineKeyboardButton(text="🎲 Угадай число", callback_data="game")],
        [InlineKeyboardButton(text="🎰 Удача дня", callback_data="luck")],
    ])

user_numbers = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Как дела? 👋\nВыбирай:", reply_markup=main_menu())

@dp.message()
async def echo(message: types.Message):
    await message.answer("Выбирай:", reply_markup=main_menu())

# Котик
@dp.callback_query(F.data == "cat")
async def send_cat(callback: types.CallbackQuery):
    await callback.answer()
    async with httpx.AsyncClient() as client:
        r = await client.get("https://api.thecatapi.com/v1/images/search")
        url = r.json()[0]["url"]
    await callback.message.answer_photo(url, caption="Вот твой котик! 🐱", reply_markup=main_menu())

# Игра угадай число
@dp.callback_query(F.data == "game")
async def game_start(callback: types.CallbackQuery):
    await callback.answer()
    number = random.randint(1, 10)
    user_numbers[callback.from_user.id] = number
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=str(i), callback_data=f"guess_{i}") for i in range(1, 6)],
        [InlineKeyboardButton(text=str(i), callback_data=f"guess_{i}") for i in range(6, 11)],
    ])
    await callback.message.answer("🎲 Угадай число от 1 до 10:", reply_markup=keyboard)

@dp.callback_query(F.data.startswith("guess_"))
async def check_guess(callback: types.CallbackQuery):
    await callback.answer()
    guess = int(callback.data.split("_")[1])
    correct = user_numbers.get(callback.from_user.id)
    if guess == correct:
        await callback.message.answer(f"🎉 Правильно! Число было {correct}!", reply_markup=main_menu())
    else:
        await callback.message.answer(f"❌ Неверно! Было {correct}. Попробуй ещё!", reply_markup=main_menu())

# Удача дня
@dp.callback_query(F.data == "luck")
async def luck(callback: types.CallbackQuery):
    await callback.answer()
    phrases = [
        "⭐️ Сегодня твой день — всё получится!",
        "💰 Жди неожиданных денег!",
        "😴 Лучший план на сегодня — отдохнуть.",
        "🚀 Ты на пике — действуй!",
        "🍕 Твоя удача сегодня — пицца.",
        "👀 Кто-то думает о тебе прямо сейчас.",
        "🎯 Сосредоточься — и всё выйдет.",
    ]
    await callback.message.answer(random.choice(phrases), reply_markup=main_menu())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

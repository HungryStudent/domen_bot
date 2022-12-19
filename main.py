from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import executor
from aiogram import Bot

from config import *

stor = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=stor)

main_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Добавить домен"))


class DomenState(StatesGroup):
    enter_domen = State()


async def on_startup(_):
    pass


@dp.message_handler(commands='start')
async def start_message(message: Message):
    await message.answer("Привет", reply_markup=main_kb)


@dp.message_handler(text="Добавить домен")
async def add_domen(message: Message):
    pass


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
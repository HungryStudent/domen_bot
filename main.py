from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import executor
from aiogram import Bot

from config import *
import db

stor = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=stor)

main_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Добавить домен"))
cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Отмена"))


class DomainState(StatesGroup):
    enter_domain = State()


async def on_startup(_):
    db.start()


@dp.message_handler(commands='start')
async def start_message(message: Message):
    await message.answer("Привет", reply_markup=main_kb)


@dp.message_handler(text="Добавить домен")
async def enter_domain(message: Message):
    await message.answer("Введите домен", reply_markup=cancel_kb)
    await DomainState.enter_domain.set()


@dp.message_handler(state="*", text="Отмена")
async def cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Ввод остановлен", reply_markup=main_kb)


@dp.message_handler(state=DomainState.enter_domain)
async def add_domain(message: Message, state: FSMContext):
    url = message.text
    db.add_domain(url)
    await message.answer("Домен добавлен", reply_markup=main_kb)
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

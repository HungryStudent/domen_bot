from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import executor
from aiogram import Bot

import keyboards as kb
from config import *
import db

stor = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=stor)


class ProjectStates(StatesGroup):
    enter_name = State()
    enter_offer = State()
    enter_domain = State()


class DomainState(StatesGroup):
    enter_domain = State()


async def on_startup(_):
    db.start()


@dp.message_handler(commands='start')
async def start_message(message: Message):
    await message.answer("Привет", reply_markup=kb.main)


@dp.message_handler(text="Проекты")
async def show_projects(message: Message):
    projects = db.get_projects()
    await message.answer("Список проектов", reply_markup=kb.get_projects(projects))


@dp.message_handler(state="*", text="Отмена")
async def cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Ввод остановлен", reply_markup=kb.main)


@dp.callback_query_handler(text="create_project")
async def enter_name_to_project(call: CallbackQuery):
    await ProjectStates.enter_name.set()
    await call.message.answer("Введите название проекта", reply_markup=kb.cancel)
    await call.answer()


@dp.message_handler(state=ProjectStates.enter_name)
async def enter_domain_to_project(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await ProjectStates.next()
    await message.answer("Введите offer id")


@dp.message_handler(state=ProjectStates.enter_offer)
async def enter_domain_to_project(message: Message, state: FSMContext):
    await state.update_data(offer=message.text)
    await ProjectStates.next()
    await message.answer("Введите домен")


@dp.message_handler(state=ProjectStates.enter_domain)
async def create_project(message: Message, state: FSMContext):
    data = await state.get_data()
    db.create_project(data["name"], data["offer"], message.text)
    await state.finish()
    await message.answer("Проект создан")
    await show_projects(message)


@dp.callback_query_handler(text="back_to_projects")
async def back_to_projects(call: CallbackQuery):
    projects = db.get_projects()
    await call.message.edit_text("Список проектов", reply_markup=kb.get_projects(projects))


@dp.callback_query_handler(Text(startswith="project"))
async def show_project(call: CallbackQuery):
    project_id = call.data.split(":")[1]
    project = db.get_project(project_id)
    await call.message.edit_text(f"Выбран проект {project[0]} - {project[1]}",
                                 reply_markup=kb.get_add_domain(project_id))


@dp.callback_query_handler(Text(startswith="delete"))
async def delete_project(call: CallbackQuery):
    project_id = call.data.split(":")[1]
    await call.message.edit_text("Вы уверены, что хотите удалить проект?",
                                 reply_markup=kb.get_accept_delete(project_id))


@dp.callback_query_handler(Text(startswith="accept_delete"))
async def accept_delete_project(call: CallbackQuery):
    project_id = call.data.split(":")[1]
    db.delete_project(project_id)
    await call.message.edit_text("Проект удален")


@dp.callback_query_handler(text="cancel_delete")
async def cancel_delete_project(call: CallbackQuery):
    await call.message.delete()


@dp.callback_query_handler(Text(startswith="add_domain"))
async def show_project(call: CallbackQuery, state: FSMContext):
    project_id = call.data.split(":")[1]
    await DomainState.enter_domain.set()
    await state.update_data(project_id=project_id)
    await call.message.answer("Введите домен", reply_markup=kb.cancel)
    await call.answer()


@dp.message_handler(state=DomainState.enter_domain)
async def add_domain(message: Message, state: FSMContext):
    data = await state.get_data()
    url = message.text
    domain_count = db.add_domain(url, data["project_id"])
    await message.answer(f"Домен добавлен. Всего - {domain_count}", reply_markup=kb.main)
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

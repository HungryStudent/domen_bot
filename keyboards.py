from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

main = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Проекты"))
cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Отмена"))


def get_projects(projects):
    kb = InlineKeyboardMarkup(row_width=1)
    for project in projects:
        kb.add(InlineKeyboardButton(project[1], callback_data=f"project:{project[0]}"))
    kb.add(InlineKeyboardButton("Добавить новый проект", callback_data=f"create_project"))
    return kb


def get_add_domain(project_id):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("Добавить домен", callback_data=f"add_domain:{project_id}"),
        InlineKeyboardButton("Удалить проект", callback_data=f"delete:{project_id}"),
        InlineKeyboardButton("Назад", callback_data="back_to_projects"))


def get_accept_delete(project_id):
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("Да, удалить", callback_data=f"accept_delete:{project_id}"),
        InlineKeyboardButton("Нет", callback_data="cancel_delete"))

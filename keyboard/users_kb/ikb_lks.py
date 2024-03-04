from aiogram.types import ReplyKeyboardMarkup
from utils.db_api.quck_commands import users
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton
from utils.db_api.quck_commands import questions
from aiogram.filters.callback_data import CallbackData


class Current_lks(CallbackData, prefix="my"):
    cb: str
    id: int


def ikb_lks(id):
    cb = Current_lks(cb="ikb_lks", id=id).pack()
    btn1 = InlineKeyboardButton(text=f"🙋‍♂️Личный кабинет", callback_data=cb)
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn1]])
    return builder

from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton


def ikb_save():
    btn1 = InlineKeyboardButton(text="Да", callback_data="ikb_save_event")
    btn2 = InlineKeyboardButton(text="Нет", callback_data="ikb_back")
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn1], [btn2]])
    return builder

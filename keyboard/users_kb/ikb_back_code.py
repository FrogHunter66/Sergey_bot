from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton


def ikb_back_code():
    btn1 = InlineKeyboardButton(text="↩️Назад", callback_data="ikb_back_code")
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn1]])
    return builder
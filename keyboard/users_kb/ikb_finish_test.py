from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton



def ikb_finish_test():
    btn1 = InlineKeyboardButton(text="Завершить", callback_data="ikb_finish_test")
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn1]])
    return builder

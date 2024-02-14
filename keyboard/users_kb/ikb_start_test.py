from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton



def ikb_start_test():
    btn1 = InlineKeyboardButton(text="Начать", callback_data="ikb_start_test")
    btn2 = InlineKeyboardButton(text="Назад", callback_data="ikb_back_code")
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn1], [btn2]])
    return builder

from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton



def ikb_start():
    btn1 = InlineKeyboardButton(text="🔔Зарегистрироваться!", callback_data="ikb_register_new")
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn1]])
    return builder

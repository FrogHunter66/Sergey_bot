from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton


def ikb_back():
    btn1 = InlineKeyboardButton(text="Назад", callback_data="ikb_back")
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn1]])
    return builder


def ikb_back_create_test():
    btn1 = InlineKeyboardButton(text="Назад", callback_data="ikb_back")
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn1]])
    return builder
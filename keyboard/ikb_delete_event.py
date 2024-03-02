from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton


def ikb_delete_event():
    btn1 = InlineKeyboardButton(text="✅Да", callback_data="ikb_delete_forever_event")
    btn2 = InlineKeyboardButton(text="❌Нет", callback_data="ikb_back_from_delete")
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn1], [btn2]])
    return builder

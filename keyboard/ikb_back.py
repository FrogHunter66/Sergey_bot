from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton


def ikb_back_clear(): #todo Нигде не используется
    btn1 = InlineKeyboardButton(text="🗑️Очистить", callback_data="ikb_clear_state")
    btn2 = InlineKeyboardButton(text="↩️Назад", callback_data="ikb_back")
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn1], [btn2]])
    return builder

def ikb_back():
    btn1 = InlineKeyboardButton(text="↩️Назад", callback_data="ikb_back")
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn1]])
    return builder


def ikb_back_create_test():
    btn1 = InlineKeyboardButton(text="↩️Назад", callback_data="ikb_back")
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn1]])
    return builder

def ikb_back_actions_event():
    btn1 = InlineKeyboardButton(text="↩️Назад", callback_data="ikb_back_actions_event")
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn1]])
    return builder
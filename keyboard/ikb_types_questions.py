from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton



def ikb_types_of_questions():
    btn1 = InlineKeyboardButton(text="1 Тип", callback_data="ikb_1st_type")
    btn2 = InlineKeyboardButton(text="2 Тип", callback_data="ikb_2nd_type")
    btn3 = InlineKeyboardButton(text="↩️Назад", callback_data="ikb_back_choose_questionnn") #todo потерялся калбэк
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn1], [btn2], [btn3]])
    return builder

def ikb_types_of_questions_quiz():
    btn1 = InlineKeyboardButton(text="1 Тип", callback_data="ikb_1st_type_quiz")
    btn2 = InlineKeyboardButton(text="2 Тип", callback_data="ikb_2nd_type_quiz")
    btn3 = InlineKeyboardButton(text="↩️Назад", callback_data="ikb_back_choose_quiz_quest")
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn1], [btn2], [btn3]])
    return builder

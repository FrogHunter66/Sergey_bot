from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton



def ikb_timer():
    btn1 = InlineKeyboardButton(text="15 минут",callback_data="ikb_time_15m")
    btn2 = InlineKeyboardButton(text="30 минут",callback_data="ikb_time_30m")
    btn3 = InlineKeyboardButton(text="1 час",callback_data="ikb_time_1h")
    btn4 = InlineKeyboardButton(text="2 часа",callback_data="ikb_time_2h")
    btn5 = InlineKeyboardButton(text="3 часа",callback_data="ikb_time_3h")
    btn6 = InlineKeyboardButton(text="6 часов",callback_data="ikb_time_6h")
    btn7 = InlineKeyboardButton(text="12 часов",callback_data="ikb_time_12h")
    btn8 = InlineKeyboardButton(text="1 сутки",callback_data="ikb_time_1d")
    btn9 = InlineKeyboardButton(text="2 суток",callback_data="ikb_time_2d")
    btn10 = InlineKeyboardButton(text="5 суток",callback_data="ikb_time_5d")
    btn11 = InlineKeyboardButton(text="1 неделя",callback_data="ikb_time_7d")
    btn12 = InlineKeyboardButton(text="Неограниченно", callback_data="ikb_time_without")
    btn13 = InlineKeyboardButton(text="Назад", callback_data="ikb_back")
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn1, btn2, btn3, btn4], [btn5, btn6, btn7, btn8], [btn9, btn10, btn11, btn12]])
    return builder

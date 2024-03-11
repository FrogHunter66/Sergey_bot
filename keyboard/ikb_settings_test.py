from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton



def ikb_settings_test():

    btn6 = InlineKeyboardButton(text="📝Имя теста", callback_data="ikb_name_for_test")
    btn1 = InlineKeyboardButton(text="🔓Код доступа", callback_data="access_code")
    btn2 = InlineKeyboardButton(text="🕒Время на выполнение", callback_data="time_to_answer")
    btn3 = InlineKeyboardButton(text="🕒Время существования", callback_data="time_of_test")
    btn4 = InlineKeyboardButton(text="➕Создать", callback_data="ikb_create_questions")
    btn5 = InlineKeyboardButton(text="↩️Назад", callback_data="ikb_back_actions")
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn6], [btn1], [btn2], [btn3], [btn4], [btn5]])
    return builder

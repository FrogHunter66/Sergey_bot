from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton



def ikb_settings_test():
    btn6 = InlineKeyboardButton(text="📝Название теста", callback_data="ikb_name_for_test")
    btn2 = InlineKeyboardButton(text="🕒Время на выполнение", callback_data="time_to_answer")
    btn3 = InlineKeyboardButton(text="🕒Время существования", callback_data="time_of_test")
    btn4 = InlineKeyboardButton(text="➕Создать", callback_data="ikb_create_questions")
    btn5 = InlineKeyboardButton(text="↩️Назад", callback_data="ikb_back_actions")
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn6], [btn2], [btn3], [btn4], [btn5]])
    return builder


def ikb_settings_quiz():
    btn6 = InlineKeyboardButton(text="📝Название опроса", callback_data="ikb_name_for_quizz")
    btn2 = InlineKeyboardButton(text="🕒Время на выполнение", callback_data="time_to_answer_quizz")
    btn3 = InlineKeyboardButton(text="🕒Время существования", callback_data="time_of_quizz")
    btn4 = InlineKeyboardButton(text="➕Создать", callback_data="ikb_create_quizz_1")
    btn5 = InlineKeyboardButton(text="↩️Назад", callback_data="ikb_back_actions_quizz")
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn6], [btn2], [btn3], [btn4], [btn5]])
    return builder
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton



def ikb_current_test():
    btn1 = InlineKeyboardButton(text="Создать тест",callback_data="create_test")
    btn2 = InlineKeyboardButton(text="📋Список тестов", callback_data="list_tests")
    btn3 = InlineKeyboardButton(text="Список пользователей", callback_data="get_stat")
    btn4 = InlineKeyboardButton(text="Удалить мероприятие", callback_data="delete_event")
    btn5 = InlineKeyboardButton(text="Назад", callback_data="ikb_back_list_events")
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn1, btn2], [btn3, btn4], [btn5]])
    return builder

from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton



def ikb_main_menu():
    btn1 = InlineKeyboardButton(text="Создать мероприятие",callback_data="create_event")
    btn2 = InlineKeyboardButton(text="Список существующих событий", callback_data="get_events")
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn1], [btn2]])
    return builder

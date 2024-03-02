from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton



def ikb_adding_questions():
    btn1 = InlineKeyboardButton(text="➕Создать вопрос",callback_data="create_question")
    btn3 = InlineKeyboardButton(text="↩️Назад", callback_data="get_stat")
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn1], [btn3]])
    return builder

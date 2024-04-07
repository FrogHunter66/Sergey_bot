from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton


def ikb_change_variants_question():
    btn1 = InlineKeyboardButton(text="➕Добавить вариант", callback_data="ikb_add_new_variant")
    btn2 = InlineKeyboardButton(text="🗑️Удалить", callback_data="ikb_delete_one_var")
    btn3 = InlineKeyboardButton(text="🗑️Удалить все", callback_data="ikb_clear_all_vars")
    btn4 = InlineKeyboardButton(text="↩️Назад", callback_data="ikb_back_settings_quest")
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn1], [btn2], [btn3], [btn4]])
    return builder
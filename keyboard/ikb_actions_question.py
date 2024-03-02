from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton



def ikb_actions_qustion():
    btn1 = InlineKeyboardButton(text="❓ Текст вопроса", callback_data="ikb_text_quest")
    btn2 = InlineKeyboardButton(text="➕Добавить варианты ответа", callback_data="ikb_add_variant")
    btn3 = InlineKeyboardButton(text="🎯Выбрать правильный ответ", callback_data="ikb_correct_one")
    btn4 = InlineKeyboardButton(text="💾Сохранить вопрос", callback_data="ikb_add_question_test")
    btn5 = InlineKeyboardButton(text="↩️Назад", callback_data="ikb_back_choose_type")
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn1], [btn2], [btn3], [btn4], [btn5]])
    return builder


def ikb_actions_rebuild_qustion():
    btn1 = InlineKeyboardButton(text="❓ Текст вопроса", callback_data="ikb_text_quest")
    btn2 = InlineKeyboardButton(text="➕Добавить варианты ответа", callback_data="ikb_add_variant")
    btn3 = InlineKeyboardButton(text="🎯Выбрать правильный ответ", callback_data="ikb_correct_one")
    btn4 = InlineKeyboardButton(text="💾Сохранить изменения", callback_data="ikb_save_quest_changes")
    btn5 = InlineKeyboardButton(text="↩️Назад", callback_data="ikb_back_choose_type")
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn1], [btn2], [btn3], [btn4], [btn5]])
    return builder
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton



def ikb_actions_qustion():
    btn1 = InlineKeyboardButton(text="❓ Текст вопроса", callback_data="ikb_text_quest")
    btn2 = InlineKeyboardButton(text="➕Изменить варианты ответа", callback_data="ikb_change_quest_variant")
    btn3 = InlineKeyboardButton(text="🎯Выбрать правильный ответ", callback_data="ikb_correct_one")
    btn4 = InlineKeyboardButton(text="💾Сохранить вопрос", callback_data="ikb_add_question_test")
    btn5 = InlineKeyboardButton(text="↩️Назад", callback_data="ikb_back_choose_type")
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn1], [btn2], [btn3], [btn4], [btn5]])
    return builder


def ikb_question_quiz_menu():
    btn1 = InlineKeyboardButton(text="❓ Текст вопроса", callback_data="ikb_text_quest_quiz")
    btn2 = InlineKeyboardButton(text="➕Изменить варианты ответа", callback_data="ikb_change_quest_variant_quiz")
    btn4 = InlineKeyboardButton(text="💾Сохранить вопрос", callback_data="ikb_add_question_test_quiz")
    btn5 = InlineKeyboardButton(text="↩️Назад", callback_data="ikb_back_choose_type_quiz")
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn1], [btn2], [btn4], [btn5]])
    return builder


def ikb_actions_rebuild_qustion():
    btn1 = InlineKeyboardButton(text="❓ Текст вопроса", callback_data="ikb_text_quest")
    btn2 = InlineKeyboardButton(text="➕Изменить варианты ответа", callback_data="ikb_change_quest_variant")
    btn3 = InlineKeyboardButton(text="🎯Выбрать правильный ответ", callback_data="ikb_correct_one")
    btn4 = InlineKeyboardButton(text="💾Сохранить изменения", callback_data="ikb_save_quest_changes")
    btn5 = InlineKeyboardButton(text="↩️Назад", callback_data="ikb_back_choose_type")
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn1], [btn2], [btn3], [btn4], [btn5]])
    return builder
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton
from utils.db_api.quck_commands import tests, questions
from aiogram.filters.callback_data import CallbackData


class Choose_quest(CallbackData, prefix="my"):
    cb: str
    id: int



async def ikb_all_questions(id):
    events = await questions.get_questions(id)
    lst = list()
    for i, event in enumerate(events):
        cb = Choose_quest(cb="ikb_pickquestion", id=event.id_quest).pack()
        btn1 = InlineKeyboardButton(text=f"{i+1} - й вопрос", callback_data=cb)
        lst.append(btn1)
    btn2 = InlineKeyboardButton(text="➕Добавить вопрос", callback_data=f"ikb_add_to_current")
    btn3 = (InlineKeyboardButton(text="↩️Назад", callback_data=f"ikb_back_all_questions"))
    builder = InlineKeyboardMarkup(inline_keyboard=[lst, [btn2], [btn3]])
    return builder

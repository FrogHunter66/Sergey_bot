from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton
from utils.db_api.quck_commands import questions
from aiogram.filters.callback_data import CallbackData


class Take_quest(CallbackData, prefix="my"):
    cb: str
    id: int



async def ikb_get_all_quests(id_test):
    events = await questions.get_questions(id_test=id_test)
    lst = list()
    for i, event in enumerate(events):
        cb = Take_quest(cb="ikb_quest", id=event.id_quest).pack()
        btn1 = InlineKeyboardButton(text=f"{i+1} - й вопрос",
                                    callback_data=cb)
        lst.append(btn1)
    btn3 = (InlineKeyboardButton(text="🏁Заврешить тест", callback_data=f"ikb_finish"))
    builder = InlineKeyboardMarkup(inline_keyboard=[lst, [btn3]])
    return builder

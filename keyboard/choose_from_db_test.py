from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton
from utils.db_api.quck_commands import questions
from utils.db_api.quck_commands import tests
from aiogram.filters.callback_data import CallbackData


class test_from_db(CallbackData, prefix="my"):
    cb: str
    id: int



async def ikb_test_from_db(id_event):
    all_tests = await tests.get_all_tests()
    lst_buttons = list()
    for i, test in enumerate(all_tests):
        id_events = test.id_event
        cb = test_from_db(cb="ikb_test_from_db", id=test.id_test).pack()
        if id_events:
            if id_event in id_events:
                btn = InlineKeyboardButton(text=f"✔ {test.name}", callback_data=cb)
            else:
                btn = InlineKeyboardButton(text=f"{test.name}", callback_data=cb)
        else:
            btn = InlineKeyboardButton(text=f"{test.name}", callback_data=cb)
        lst_buttons.append(btn)
    btn3 = (InlineKeyboardButton(text="💾Сохранить", callback_data=f"ikb_save_answer_dbs"))
    ss = [[m] for m in lst_buttons]
    ss.append([btn3])
    builder = InlineKeyboardMarkup(inline_keyboard=ss)
    return builder
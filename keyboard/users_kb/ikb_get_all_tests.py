from aiogram.types import ReplyKeyboardMarkup
from utils.db_api.quck_commands import users
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton
from utils.db_api.quck_commands import questions
from aiogram.filters.callback_data import CallbackData
from utils.db_api.quck_commands import tests

class pick_a_test_user(CallbackData, prefix="my"):
    cb: str
    id: int


async def ikb_all_tests_event_user(id):
    all_tests = await tests.get_all_tests_in_event(id)
    lst = list()
    for i, test in enumerate(all_tests):
        cb = pick_a_test_user(cb="ikb_current_test", id=test.id_test).pack()
        btn1 = InlineKeyboardButton(text=f"{i+1} - й тест", callback_data=cb)
        lst.append(btn1)
    btn2 = InlineKeyboardButton(text="↩️Назад", callback_data="ikb_exit_event")  #todo реализовать
    builder = InlineKeyboardMarkup(inline_keyboard=[lst])
    return builder
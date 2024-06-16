from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton
from utils.db_api.quck_commands import questions
from utils.db_api.quck_commands import tests
from aiogram.filters.callback_data import CallbackData


class answer(CallbackData, prefix="my"):
    cb: str
    id: int



async def ikb_pass_test(id_event):
    evnts_test = await tests.get_all_tests_in_event(id_event)
    all_tests = await tests.get_all_tests()
    for



    variants = list(map(str, all_variants.split(".*.")))
    lst = list()
    for i, var in enumerate(variants):
        cb = answer(cb="ikb_answer", id=i + 1).pack()
        if mark:
            lst_mark = [m for m in mark]
            if str(i+1) in lst_mark:
                btn1 = InlineKeyboardButton(text=f"{i + 1}-й ответ ✔",
                                            callback_data=cb)
                lst.append(btn1)
            else:
                btn1 = InlineKeyboardButton(text=f"{i + 1}-й ответ",
                                            callback_data=cb)
                lst.append(btn1)

        else:
            btn1 = InlineKeyboardButton(text=f"{i+1}-й ответ",
                                        callback_data=cb)
            lst.append(btn1)
    btn3 = (InlineKeyboardButton(text="💾Сохранить ответ", callback_data=f"ikb_save_answer"))
    ss = [[m] for m in lst]
    ss.append([btn3])
    builder = InlineKeyboardMarkup(inline_keyboard=ss)
    return builder
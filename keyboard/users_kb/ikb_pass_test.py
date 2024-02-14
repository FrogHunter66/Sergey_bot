from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton
from utils.db_api.quck_commands import questions
from aiogram.filters.callback_data import CallbackData


class answer(CallbackData, prefix="my"):
    cb: str
    id: int



async def ikb_pass_test(id_quest):
    events = await questions.get_current(id_quest)
    all_variants = events.variants
    variants = list(map(str, all_variants.split(".*.")))
    lst = list()
    for i, var in enumerate(variants):
        cb = answer(cb="ikb_answer", id=i).pack()
        btn1 = InlineKeyboardButton(text=f"{i+1} - й ответ",
                                    callback_data=cb)
        lst.append(btn1)
    btn3 = (InlineKeyboardButton(text="Сохранить ответ", callback_data=f"ikb_save_answer"))
    builder = InlineKeyboardMarkup(inline_keyboard=[lst, [btn3]])
    return builder
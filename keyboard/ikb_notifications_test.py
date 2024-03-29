from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton
from utils.db_api.quck_commands import tests
from aiogram.filters.callback_data import CallbackData



class Notifications_test(CallbackData, prefix="my"):
    cb: str
    id: int


async def ikb_notifications(id_event):
    events = await tests.get_all_tests_in_event(id_event)
    lst = list()
    for i, event in enumerate(events):
        cb = Notifications_test(cb="ikb_notifications", id=event.id_test).pack()
        btn1 = InlineKeyboardButton(text=f"{event.id_test+1} - й тест", callback_data=cb)
        lst.append(btn1)
    btn3 = (InlineKeyboardButton(text="↩️Назад", callback_data=f"ikb_back_to_notifications"))
    builder = InlineKeyboardMarkup(inline_keyboard=[lst, [btn3]])
    return builder

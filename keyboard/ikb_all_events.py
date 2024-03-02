from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton
from utils.db_api.quck_commands import event
from aiogram.filters.callback_data import CallbackData


class Choose_event(CallbackData, prefix="my"):
    cb: str
    id: int



async def ikb_all_events():
    events = await event.get_all_events()
    lst = list()
    for i in events:
        cb = Choose_event(cb="ikb_choose", id=i.id_event).pack()
        btn1 = InlineKeyboardButton(text=i.event_name,
                                    callback_data=cb)
        lst.append(btn1)
    btn3 = (InlineKeyboardButton(text="↩️Назад", callback_data=f"ikb_back"))
    builder = InlineKeyboardMarkup(inline_keyboard=[lst, [btn3]])
    return builder

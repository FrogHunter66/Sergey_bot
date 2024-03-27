from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton
from utils.db_api.quck_commands import event, users
from aiogram.filters.callback_data import CallbackData


class Choose_event(CallbackData, prefix="my"):
    cb: str
    id: int



async def ikb_all_events(user_id):
    user = await users.get_current_user(user_id)
    events = await event.get_all_events()
    lst = list()
    if user.events == None:
        btn3 = (InlineKeyboardButton(text="↩️Назад", callback_data=f"ikb_back"))
        builder = InlineKeyboardMarkup(inline_keyboard=[[btn3]])
        return builder

    if user.status == "admin_buy":
        event_admin = list(user.events)
        for ev_id in event_admin:
            current = await event.select_event(ev_id)
            cb = Choose_event(cb="ikb_choose", id=current.id_event).pack()
            btn1 = InlineKeyboardButton(text=current.event_name,
                                        callback_data=cb)
            lst.append(btn1)

    else:
        for i in events:
            cb = Choose_event(cb="ikb_choose", id=i.id_event).pack()
            btn1 = InlineKeyboardButton(text=i.event_name,
                                        callback_data=cb)
            lst.append(btn1)
    btn3 = (InlineKeyboardButton(text="↩️Назад", callback_data=f"ikb_back"))
    builder = InlineKeyboardMarkup(inline_keyboard=[lst, [btn3]])
    return builder

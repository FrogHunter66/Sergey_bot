from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton


class Choose_timeer(CallbackData, prefix="my"):
    cb: str
    id: str


def ikb_timer():
    cb1 = Choose_timeer(cb="ikb_time", id="15m").pack()
    btn1 = InlineKeyboardButton(text="15 минут", callback_data=cb1)
    cb2 = Choose_timeer(cb="ikb_time", id="30m").pack()
    btn2 = InlineKeyboardButton(text="30 минут", callback_data=cb2)
    cb3 = Choose_timeer(cb="ikb_time", id="1h").pack()
    btn3 = InlineKeyboardButton(text="1 час", callback_data=cb3)
    cb4 = Choose_timeer(cb="ikb_time", id="2h").pack()
    btn4 = InlineKeyboardButton(text="2 часа", callback_data=cb4)
    cb5 = Choose_timeer(cb="ikb_time", id="3h").pack()
    btn5 = InlineKeyboardButton(text="3 часа", callback_data=cb5)
    cb6 = Choose_timeer(cb="ikb_time", id="6h").pack()
    btn6 = InlineKeyboardButton(text="6 часов", callback_data=cb6)
    cb7 = Choose_timeer(cb="ikb_time", id="12h").pack()
    btn7 = InlineKeyboardButton(text="12 часов", callback_data=cb7)
    cb8 = Choose_timeer(cb="ikb_time", id="1d").pack()
    btn8 = InlineKeyboardButton(text="1 сутки", callback_data=cb8)
    cb9 = Choose_timeer(cb="ikb_time", id="2d").pack()
    btn9 = InlineKeyboardButton(text="2 суток", callback_data=cb9)
    cb10 = Choose_timeer(cb="ikb_time", id="5d").pack()
    btn10 = InlineKeyboardButton(text="5 суток", callback_data=cb10)
    cb11 = Choose_timeer(cb="ikb_time", id="7d").pack()
    btn11 = InlineKeyboardButton(text="1 неделя", callback_data=cb11)
    cb12 = Choose_timeer(cb="ikb_time", id="without").pack()
    btn12 = InlineKeyboardButton(text="Неограниченно", callback_data=cb12)
    btn13 = InlineKeyboardButton(text="Назад", callback_data="ikb_back")
    builder = InlineKeyboardMarkup(
        inline_keyboard=[[btn1, btn2, btn3, btn4],
                         [btn5, btn6, btn7, btn8],
                         [btn9, btn10, btn11, btn12],
                         [btn13]]
    )
    return builder




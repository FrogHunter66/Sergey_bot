from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class Choose_price(CallbackData, prefix="my"):
    cb: str
    id: int


def ikb_buy_admin():
    lst = []
    lst2 = []
    for i in range(1, 5):
        cb = Choose_price(cb="ikb_buy", id=i).pack()
        btn1 = InlineKeyboardButton(text=f"🚀 {i} - й пакет",
                                    callback_data=cb)
        lst.append(btn1)
    for i in range(5, 9):
        cb = Choose_price(cb="ikb_buy", id=i).pack()
        btn1 = InlineKeyboardButton(text=f"🚀 {i} - й пакет",
                                    callback_data=cb)
        lst2.append(btn1)

    btn3 = (InlineKeyboardButton(text="↩️Назад", callback_data=f"ikb_back_buy"))

    cb1 = Choose_price(cb="ikb_buy", id=9).pack()
    btn1 = (InlineKeyboardButton(text="💥 Безлимит на месяц", callback_data=cb1))

    cb2 = Choose_price(cb="ikb_buy", id=10).pack()
    btn2 = (InlineKeyboardButton(text="💥 Безлимит на год", callback_data=cb2))

    builder = InlineKeyboardMarkup(inline_keyboard=[lst, lst2, [btn1], [btn2]])
    return builder
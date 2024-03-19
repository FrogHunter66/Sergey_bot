from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class Choose_price(CallbackData, prefix="my"):
    cb: str
    id: int


def ikb_buy_admin():
    lst = []
    for i in range(1, 4):
        cb = Choose_price(cb="ikb_buy", id=i).pack()
        btn1 = InlineKeyboardButton(text=f"{i} - й прайс",
                                    callback_data=cb)
        lst.append(btn1)
    btn3 = (InlineKeyboardButton(text="↩️Назад", callback_data=f"ikb_back_buy"))
    builder = InlineKeyboardMarkup(inline_keyboard=[lst, [btn3]])
    return builder
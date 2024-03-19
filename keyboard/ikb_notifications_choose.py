from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton
from utils.db_api.quck_commands import users, tests

async def ikb_notifications_choose(id_admin, id_test):
    test = await tests.get_current(id_event=1, id_test=id_test)

    try:
        notifications = list(test.notifications)
        ind = notifications.index(id_admin)
        btn1 = InlineKeyboardButton(text="📈Просмотреть результаты", callback_data="ikb_check_results_admin")
        btn2 = InlineKeyboardButton(text="✔️Присылать результаты", callback_data="ikb_send")
        btn3 = InlineKeyboardButton(text="Не получать результаты", callback_data="ikb_dont_send")
        builder = InlineKeyboardMarkup(inline_keyboard=[[btn1], [btn2], [btn3]])
        return builder
    except:
        btn1 = InlineKeyboardButton(text="📈Просмотреть результаты", callback_data="ikb_check_results_admin")
        btn2 = InlineKeyboardButton(text="Присылать результаты", callback_data="ikb_send")
        btn3 = InlineKeyboardButton(text="✔️Не получать результаты", callback_data="ikb_dont_send") #todo Допилить 2 бэка осталось
        builder = InlineKeyboardMarkup(inline_keyboard=[[btn1], [btn2], [btn3]])
        return builder


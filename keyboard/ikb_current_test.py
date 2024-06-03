from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton



def ikb_current_test():
    btn1 = InlineKeyboardButton(text="➕Создать тест",callback_data="create_test")
    btn2 = InlineKeyboardButton(text="➕Создать опрос",callback_data="create_quiz")
    btn4 = InlineKeyboardButton(text="🛢Выбор теста из базы",callback_data="choose_quiz_from_db")
    btn3 = InlineKeyboardButton(text="🛢Выбор опроса из базы",callback_data="choose_test_from_db")
    btn5 = InlineKeyboardButton(text="📋Список приекрепленных тестов", callback_data="list_tests")
    btn6 = InlineKeyboardButton(text="📋Список приекрепленных опросов", callback_data="list_quiz")
    btn7 = InlineKeyboardButton(text="🔔Настройки уведомлений", callback_data="get_stat")
    btn8 = InlineKeyboardButton(text="🔓Код доступа к мероприятию", callback_data="set_password")
    btn9 = InlineKeyboardButton(text="🗑️Удалить мероприятие", callback_data="delete_event")
    btn10 = InlineKeyboardButton(text="↩️Назад", callback_data="ikb_back_list_events")
    builder = InlineKeyboardMarkup(inline_keyboard=[[btn1, btn2], [btn3, btn4], [btn5, btn6], [btn7, btn8], [btn9, btn10]])
    return builder

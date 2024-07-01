import datetime

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram import types
from aiogram.filters import Command

from loader import bot
from keyboard.ikb_actions_question import ikb_actions_qustion, ikb_actions_rebuild_qustion
from keyboard.inline_main_menu import ikb_main_menu
from keyboard.ikb_back import ikb_back
from keyboard.save_event import ikb_save
from keyboard.ikb_all_events import ikb_all_events
from filters.is_admin import Admin
from set_logs1.logger_all1 import log_exceptions1
from utils.db_api.quck_commands import event
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from states.fsm import Creation, Current, Current2
from keyboard.list_tests import ikb_all_tests, Choose_test
from keyboard.ikb_current_test import ikb_current_test
from keyboard.ikb_settings_test import ikb_settings_test
from keyboard.ikb_timer import ikb_timer, Choose_timeer
from keyboard.ikb_adding_questions import ikb_adding_questions
from keyboard.ikb_types_questions import ikb_types_of_questions
from keyboard.list_tests import ikb_all_tests
from keyboard.ikb_rebuilding_test import ikb_rebuild
from keyboard.list_questions import ikb_all_questions, Choose_quest
from keyboard.choose_from_db_test import test_from_db, ikb_test_from_db
from utils.db_api.quck_commands import tests, questions
from aiogram.enums import ParseMode
router = Router()

Picked_tests = dict()


@router.callback_query(Current.event, F.data =="choose_quiz_from_db")
async def dbs(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_ev_id = data.get("event_id")
    ev = await event.get_event(current_ev_id)
    ikb = await ikb_test_from_db(current_ev_id)
    await query.message.answer(f"📑Выберите тесты которые вы хотите прикрепить к мероприятию <b>{ev.event_name}</b>", reply_markup=ikb, parse_mode=ParseMode.HTML)


@router.callback_query(Current.event, test_from_db.filter(F.cb=="ikb_test_from_db"))
async def dbs(query: CallbackQuery, callback_data: test_from_db, state: FSMContext):
    id_test = callback_data.id
    data = await state.get_data()
    current_ev_id = data.get("event_id")
    current_test = await tests.get_current(0, id_test)
    events_id_test = (current_test.id_event)
    if events_id_test:
        if current_ev_id in events_id_test:
            await tests.delete_event_test(event_id=current_ev_id, id_test=id_test)
        else:
            await tests.add_event_test(current_ev_id, id_test)
    else:
        await tests.add_event_test(current_ev_id, id_test)
    new_kb = await ikb_test_from_db(current_ev_id)
    await bot.edit_message_reply_markup(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        reply_markup=new_kb,
        inline_message_id=query.inline_message_id
    )


@router.callback_query(Current.event, F.data =="ikb_save_answer_dbs")
async def dbs(query: CallbackQuery, state: FSMContext):
    await query.message.answer("✔️Список тестов успешно обновлен")
    data = await state.get_data()

    name = data.get("event")
    id_event = data.get("event_id")
    ev = await event.get_event(id_event)
    await query.message.answer(f"""⚡ Выберите действие для мероприятия <b>{name}</b>
    
⚡Текущий код доступа <code>{ev.password if ev.password else "⛔Пока не определен"}</code>""", reply_markup=ikb_current_test(), parse_mode=ParseMode.HTML)

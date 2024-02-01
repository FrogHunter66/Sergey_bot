from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram import types
from aiogram.filters import Command
from keyboard.inline_main_menu import ikb_main_menu
from keyboard.ikb_back import ikb_back
from keyboard.save_event import ikb_save
from keyboard.ikb_all_events import ikb_all_events
from filters.is_admin import Admin
from utils.db_api.quck_commands import event
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from states.fsm import Creation, Current
from keyboard.list_tests import ikb_all_tests, Choose_test
from keyboard.ikb_current_test import ikb_current_test
from keyboard.ikb_settings_test import ikb_settings_test
from keyboard.ikb_timer import ikb_timer
from keyboard.ikb_adding_questions import ikb_adding_questions
from keyboard.ikb_types_questions import ikb_types_of_questions
from keyboard.list_tests import ikb_all_tests
from keyboard.ikb_rebuilding_test import ikb_rebuild
from keyboard.list_questions import ikb_all_questions, Choose_quest
from utils.db_api.quck_commands import tests, questions
router = Router()

@router.message(
    Command("stadfgfhdfgrt"),
    Admin()
)
async def first(message: Message):
    await message.answer("Приветствую, админ, выбери действие", reply_markup=ikb_main_menu())


@router.callback_query(Choose_test.filter(F.cb == "ikb_tests"), Current.event)
async def second(query: CallbackQuery, callback_data: Choose_test, state: FSMContext):
    data_state = await state.get_data()
    id = data_state.get("event_id")
    data = await tests.get_current(id_event=id, id_test=callback_data.id)
    num = data.id_test
    name = data_state.get("event")
    await state.update_data(current_test=num)
    await query.message.answer(f"Выберите действие для теста номер '{num}' в мероприятии '{name}'", reply_markup=ikb_rebuild())
    await state.set_state(Current.current_test)
    await state.update_data(event_id=callback_data.id)
    await state.update_data(event=name)


@router.callback_query(F.data == "ikb_qustions_rebuild", Current.current_test)
async def second(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    id = data.get("current_test")
    kb = await ikb_all_questions(id)
    await query.message.answer("Выберите действие", reply_markup=kb)


@router.callback_query(F.data == "ikb_add_to_current", Current.current_test)
async def second(query: CallbackQuery, state: FSMContext):
    await state.set_state(Current.event)
    await query.message.answer("""Выберите тип вопроса:
        1 тип - вопрос с единственным правильным ответом
        2 тип - вопрос с множественным выбором""", reply_markup=ikb_types_of_questions())



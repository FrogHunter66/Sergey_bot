import pickle

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram import types
from aiogram.filters import Command
import datetime
from keyboard.ikb_actions_question import ikb_actions_qustion, ikb_actions_rebuild_qustion
from keyboard.inline_main_menu import ikb_main_menu
from keyboard.ikb_back import ikb_back
from keyboard.save_event import ikb_save
from keyboard.ikb_all_events import ikb_all_events
from filters.is_admin import Admin
from filters.is_new_user import New_User
from filters.Old_User import Old_user
from utils.db_api.quck_commands import event
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from states.fsm import Creation, Current, Current2, User
from keyboard.list_tests import ikb_all_tests, Choose_test
from keyboard.ikb_current_test import ikb_current_test
from keyboard.ikb_settings_test import ikb_settings_test
from keyboard.ikb_timer import ikb_timer, Choose_timeer
from keyboard.ikb_adding_questions import ikb_adding_questions
from keyboard.ikb_types_questions import ikb_types_of_questions
from keyboard.list_tests import ikb_all_tests
from keyboard.ikb_rebuilding_test import ikb_rebuild
from keyboard.list_questions import ikb_all_questions, Choose_quest
from keyboard.users_kb.ikb_start import ikb_start
from utils.db_api.quck_commands import tests, questions
from keyboard.users_kb.ikb_start_test import ikb_start_test
from keyboard.users_kb.ikb_back_code import ikb_back_code
from keyboard.users_kb.ikb_choose_quests import ikb_get_all_quests
from utils.db_api.quck_commands import users
router = Router()

@router.message(
    Command("start"),
    New_User()
)
async def first(message: Message):
    await message.answer("Приветствую, пользователь, нажми зарегистрироваться, чтобы получить доступ к тестам", reply_markup=ikb_start())


@router.callback_query(F.data == "ikb_register_new", New_User())
async def second(query: CallbackQuery, state: FSMContext):
    await state.set_state(User.id)
    await state.update_data(id=query.from_user.id)
    await state.update_data(username=query.from_user.username)
    await query.message.answer("Представьтесь, как к вам обращаться?")



@router.message(User.id, New_User())
async def first(message: Message, state: FSMContext):
    await users.add_user(id=message.from_user.id, username=message.from_user.username, first_name=message.text, last_name="", status="user")
    name = message.text
    await state.update_data(first_name=name)
    await message.answer(f"Привет, {name}, напишите код доступа к тесту, чтобы его пройти")
    await state.set_state(User.test_code)

@router.message(Command("start"), Old_user())
async def first(message: Message, state: FSMContext):
    user = await users.get_current_user(message.from_user.id)
    name = user.first_name
    await message.answer(f"Привет, {name}, напишите код доступа к тесту, чтобы его пройти")
    await state.set_state(User.test_code)
    await state.update_data(first_name=name)


@router.message(User.test_code, Old_user())
async def start_test(message: Message, state: FSMContext):
    data = await state.get_data()
    code = message.text
    all_tests = await tests.get_all_tests()
    flag = False
    for i_test in all_tests:
        if str(i_test.token) == str(code):
            await state.update_data(current_test=i_test.id_test)
            flag = True
            break
    if flag:
        data = await state.get_data()
        id_test = data.get("current_test")
        current_test = await tests.get_current(1, id_test=id_test)
        count_quests = await questions.get_questions(id_test)
        current_time = datetime.datetime.utcnow()
        current_time = current_time.replace(tzinfo=datetime.timezone.utc, microsecond=0)
        end_time = current_test.end_time.replace(microsecond=0)
        differ = end_time - current_time
        if current_time < end_time:
            await message.answer(f"""Готовы ли вы приступить к началу тестирования 
Время на прохождение теста ограниченно {current_test.lifetime}
Время до конца существования теста - {differ}
Количество вопросов - {len(count_quests)}""", reply_markup=ikb_start_test())
        else:
            await message.answer(f"Тест больше не доступен. Время существования теста истекло")
    else:
        await message.answer("По данному коду не было найденно тестов", reply_markup=ikb_back_code())
        name = data.get("name")
        await message.answer(f"Привет, {name}, напишите код доступа к тесту, чтобы его пройти")


def serialize_datetime(dt):
    return pickle.dumps(dt).hex()


@router.callback_query(F.data == "ikb_start_test", User.test_code, Old_user())
async def second(query: CallbackQuery, state: FSMContext):
    await state.set_state(User.choose_quest)
    data = await state.get_data()
    id_test = data.get("current_test")
    kb = await ikb_get_all_quests(id_test)
    test = await tests.get_current(1, id_test)
    time_to_answer = int(test.bound_time)
    end_time = datetime.datetime.utcnow() + datetime.timedelta(hours=3, minutes=time_to_answer)
    serialized_time = serialize_datetime(end_time)
    await state.update_data(time=serialized_time)
    await query.message.answer("Вы начали тестирование!!")
    await query.message.answer(f"Выберите вопрос", reply_markup=kb)


@router.callback_query(F.data == "ikb_back_code", User.test_code, Old_user())
async def second(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get("first_name")
    await query.message.answer(f"Привет, {name}, напишите код доступа к тесту, чтобы его пройти")



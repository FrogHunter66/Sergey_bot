import pickle

from aiogram.enums import ParseMode
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
from keyboard.users_kb.ikb_get_all_tests import pick_a_test_user, ikb_all_tests_event_user
from keyboard.ikb_settings_test import ikb_settings_test
from keyboard.ikb_timer import ikb_timer, Choose_timeer
from keyboard.ikb_adding_questions import ikb_adding_questions
from keyboard.ikb_types_questions import ikb_types_of_questions
from keyboard.ikb_rebuilding_test import ikb_rebuild
from keyboard.list_questions import ikb_all_questions, Choose_quest
from keyboard.users_kb.ikb_start import ikb_start
from utils.db_api.quck_commands import tests, questions
from keyboard.users_kb.ikb_start_test import ikb_start_test
from keyboard.users_kb.ikb_back_code import ikb_back_code
from keyboard.users_kb.ikb_choose_quests import ikb_get_all_quests
from utils.db_api.quck_commands import results
from keyboard.users_kb.ikb_lks import ikb_lks, Current_lks
from utils.db_api.quck_commands import users
router = Router()

def serialize_datetime(dt):
    return pickle.dumps(dt).hex()

@router.message(
    Command("start"),
    New_User()
)
async def first(message: Message):
    await message.answer("👋Приветствую, пользователь, нажми зарегистрироваться, чтобы получить доступ к тестам", reply_markup=ikb_start())


@router.callback_query(F.data == "ikb_register_new", New_User())
async def second(query: CallbackQuery, state: FSMContext):
    await state.set_state(User.id)
    await state.update_data(id=query.from_user.id)
    await state.update_data(username=query.from_user.username)
    await query.message.answer("🤝Представьтесь, как к вам обращаться?")



@router.message(User.id, New_User())
async def first(message: Message, state: FSMContext):
    await users.add_user(id=message.from_user.id, username=message.from_user.username, first_name=message.text, last_name="", status="user")
    name = message.text
    await state.update_data(first_name=name)
    await state.update_data(username="@" + message.from_user.username)
    await message.answer(f"👋Привет, {name}, напишите код доступа к мероприятию, чтобы получить доступ к тестам.", reply_markup=ikb_lks(message.from_user.id))
    await state.set_state(User.test_code)

@router.message(Command("start"), Old_user())
async def first(message: Message, state: FSMContext):
    user = await users.get_current_user(message.from_user.id)
    name = user.first_name
    await message.answer(f"""👋Привет, {name}, напишите код доступа к мероприятию, чтобы получить доступ к тестам.""", parse_mode=ParseMode.HTML, reply_markup=ikb_lks(message.from_user.id))
    await state.set_state(User.test_code)
    await state.update_data(first_name=name)
    await state.update_data(username="@" + message.from_user.username)



@router.callback_query(Current_lks.filter(F.cb=="ikb_lks"))
async def take_quest(query: CallbackQuery, callback_data: Current_lks):
    id = callback_data.id
    users_result = await results.get_all_results_id_user(id)
    if users_result:
        for result in users_result:
            current_test = await tests.get_current(id_test=result.id_test, id_event=0)
            name = current_test.name
            ev = await event.get_event(id=current_test.id_event)
            pluses = (result.result).count('1')
            minuses = (result.result).count('0')
            await query.message.answer(f"""Мероприятие: <b>{ev.name}</b>
    📋Тест: <b>{name}</b>
            
    🎯 Процент выполнения - <b>{pluses/(pluses+minuses)//1}</b>
    
    ✅ Правильных ответов - <b>{pluses}</b>
    
    ❌ Неправильных овтеты - <b>{minuses}</b>
    
    
    #result""", parse_mode=ParseMode.HTML)
    else:
        await query.message.answer("⛔Вы еще не прошли ни одного теста")

    await query.message.answer("🔓Введите код доступа к мероприятию, чтобы получить доступ к тестам", reply_markup=ikb_lks(query.message.from_user.id))


@router.message(User.test_code, Old_user())
async def start_test(message: Message, state: FSMContext):
    data = await state.get_data()
    code = message.text
    all_events = await event.get_all_events()
    flag = False
    for ev in all_events:
        print("code - ", code, "event pass - ", ev.password, code == ev.password, type(code), type(ev.password))
        if ev.password == int(code):
            current_ev = ev
            await state.update_data(current_event=ev.id_event)
            flag = True
            break
    if flag:
        kb = await ikb_all_tests_event_user(current_ev.id_event)
        await message.answer(f"""Список всех тестов мероприятия <b>{current_ev.event_name}</b>""", parse_mode=ParseMode.HTML, reply_markup=kb)
        await state.set_state(User.current_test)

    else:
        await message.answer("❌По данному коду не было найденно тестов", reply_markup=ikb_back_code())
        name = data.get("first_name")
        await message.answer(f"👋Привет, {name}, напишите код доступа к тесту, чтобы его пройти.")



@router.callback_query(pick_a_test_user.filter(F.cb=="ikb_current_test"))
async def start_test(query: CallbackQuery, callback_data: pick_a_test_user, state: FSMContext):
    print("ЗАШЛО")
    await state.update_data(current_test=callback_data.id)
    id_test = callback_data.id
    current_test = await tests.get_current(1, id_test=id_test)
    count_quests = await questions.get_questions(id_test)
    current_time = datetime.datetime.utcnow()
    current_time = current_time.replace(tzinfo=datetime.timezone.utc, microsecond=0)
    end_time = current_test.end_time.replace(microsecond=0)
    differ = end_time - current_time
    if current_time < end_time:
        await query.message.answer(f"""🎬Готовы ли вы приступить к началу тестирования?
📝Название теста - {current_test.name}
🕘Время на прохождение теста ограниченно - {current_test.lifetime}
🕘Время до конца существования теста - {differ}
🔢Количество вопросов - {len(count_quests)}""", reply_markup=ikb_start_test(), parse_mode=ParseMode.HTML)
    else:
        await query.message.answer(f"⛔Тест больше не доступен. Время существования теста истекло")


@router.callback_query(F.data == "ikb_start_test", User.current_test, Old_user())
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
    await query.message.answer("✔️Вы начали тестирование!")
    await query.message.answer(f"👉Выберите вопрос", reply_markup=kb)


@router.callback_query(F.data == "ikb_back_code", User.test_code, Old_user())
async def second(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get("first_name")
    await query.message.answer(f"👋Привет, {name}, напишите код доступа к тесту, чтобы его пройти.")



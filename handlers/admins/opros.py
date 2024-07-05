from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram import types
from aiogram.filters import Command
from filters.is_admin import Admin
from keyboard.list_questions import ikb_all_questions
from set_logs1.logger_all1 import log_exceptions1
from utils.db_api.quck_commands import event, tests, questions
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from states.fsm import Creation, Current

from keyboard.inline_main_menu import ikb_main_menu
from keyboard.ikb_back import ikb_back
from keyboard.save_event import ikb_save
from keyboard.ikb_all_events import ikb_all_events
from keyboard.ikb_all_events import ikb_all_events, Choose_event
from keyboard.ikb_current_test import ikb_current_test
from keyboard.ikb_settings_test import ikb_settings_test
from keyboard.ikb_timer import ikb_timer
from keyboard.ikb_adding_questions import ikb_adding_questions
from keyboard.ikb_types_questions import ikb_types_of_questions
from keyboard.ikb_actions_question import ikb_actions_qustion
from keyboard.ikb_change_variants_question import ikb_change_variants_question
router = Router()

@router.callback_query(Current.event, F.data == "create_test")
async def add_test(query: CallbackQuery, state: FSMContext):
    user = await users.get_current_user(query.from_user.id)
    data = await state.get_data()
    await query.message.answer(f"""Количество оставшихся тестов: *{user.c_tests}*

🛠️Выберите настройки опроса:""", reply_markup=ikb_settings_test(), parse_mode=ParseMode.MARKDOWN_V2)

@router.callback_query(Current.event, F.data == "ikb_name_for_test")
async def add_test2(query: CallbackQuery, state: FSMContext):
    await state.set_state(Current.setting_name)
    await query.message.answer("📝Укажите имя теста, *имя может содержать любые символы*", reply_markup=ikb_back(), parse_mode=ParseMode.MARKDOWN_V2)


@router.callback_query(Current.event, F.data == "time_to_answer")
async def add_test2(query: CallbackQuery, state: FSMContext):
    await state.set_state(Current.setting_passing)
    await query.message.answer("🕒Выберите ограничение по времени выполнения теста, *выразите в минутах*", reply_markup=ikb_back(),  parse_mode=ParseMode.MARKDOWN_V2)


@router.callback_query(Current.event, F.data == "time_of_test")
async def add_test2(query: CallbackQuery, state: FSMContext):
    await state.set_state(Current.setting_time)
    await query.message.answer("🕒Выберите ограничение по времени существования теста", reply_markup=ikb_timer(), parse_mode=ParseMode.MARKDOWN_V2)


@router.message(Current.setting_name, Admin())
async def add_test3(message: Message, state: FSMContext):
    code = message.text
    await state.update_data(setting_name=code)
    data = await state.get_data()
    setting_passing = data.get("setting_passing")
    setting_time = data.get("setting_time")
    await message.answer(f"✅Название теста успешно установлено <b>{code}</b>", parse_mode=ParseMode.HTML)
    await message.answer(f"""📝Название теста <b>{code}</b>
🕒Время на выполнение теста: <b>{str(setting_passing) + " минут" if setting_passing else "⛔Пока не определено"}</b>
🕒Время существования теста: <b>{decode_lifetime(setting_time)}</b>""", reply_markup=ikb_settings_test(), parse_mode=ParseMode.HTML)
    await state.set_state(Current.event)



@router.message(Current.setting_passing, Admin())
async def add_test3(message: Message, state: FSMContext):
    code = message.text
    data = await state.get_data()
    setting_name = data.get('setting_name')
    setting_time = data.get("setting_time")
    setting_passing = data.get("setting_passing")

    try:
        code = int(code)
        if code > 0:
            code = int(code)
            await state.update_data(setting_passing=code)
            await message.answer(f"✅Время на выполнение теста *успешно* установлено *{code}*", parse_mode=ParseMode.MARKDOWN_V2)
            await message.answer(f"""📝Название теста <b>{setting_name if setting_name else "⛔Пока не определено"}</b>
🕒Время на выполнение теста <b>{code} минут</b>
🕒Время существования теста <b>{decode_lifetime(setting_time)}</b>""", reply_markup=ikb_settings_test(), parse_mode=ParseMode.HTML)
        else:
            await message.answer("❌Время должно быть *натуральным числом*", parse_mode=ParseMode.MARKDOWN_V2)
            await message.answer(f"""📝Название теста <b>{setting_name if setting_name else "⛔Пока не определено"}</b>
🕒Время на выполнение теста <b>{str(setting_passing) + " минут" if setting_passing else "⛔Пока не определено"}</b>
🕒Время существования теста <b>{decode_lifetime(setting_time)}</b>""", reply_markup=ikb_settings_test(), parse_mode=ParseMode.HTML)
        await state.set_state(Current.event)
    except:
        await state.set_state(Current.event)
        await message.answer("❌Время может быть только *численнного формата*", parse_mode=ParseMode.MARKDOWN_V2)
        await message.answer(f"""📝Название теста <b>{setting_name if setting_name else "⛔Пока не определено"}</b>
🕒Время на выполнение теста <b>{str(setting_passing) + " минут" if setting_passing else "⛔Пока не определено"}</b>
🕒Время существования теста <b>{decode_lifetime(setting_time)}</b>""", reply_markup=ikb_settings_test(), parse_mode=ParseMode.HTML)


@router.callback_query(Current.setting_time, Choose_timeer.filter(F.cb=="ikb_time"))
async def add_test2(query: CallbackQuery, state: FSMContext, callback_data: Choose_timeer):
    await state.update_data(setting_time=callback_data.id)
    data = await state.get_data()
    setting_name = data.get('setting_name')
    setting_passing = data.get("setting_passing")
    await query.message.answer(f"✅Время существования теста успешно установлено *{decode_lifetime(callback_data.id)}*", parse_mode=ParseMode.MARKDOWN_V2)
    await query.message.answer(f"""📝Название теста <b>{setting_name if setting_name else "⛔Пока не определено"}</b>
🕒Время на выполнение теста <b>{str(setting_passing) + " минут" if setting_passing else "⛔Пока не определено"}</b>
🕒Время существования теста <b>{decode_lifetime(callback_data.id)}</b>""", reply_markup=ikb_settings_test(), parse_mode=ParseMode.HTML)
    await state.set_state(Current.event)

#---------------------------------- Создание теста и добавление в бд --------------------------------------
async def get_unique_key(keys):
    for i in range(1000):
        if i not in keys:
            return i
    else: return None


@router.callback_query(Current.event, F.data == "ikb_create_questions")
async def add_test2(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    id = data.get("event_id")
    passing = data.get("setting_passing")
    time = data.get("setting_time")
    test_name = data.get("setting_name")

    if passing and time and test_name:
        try:
            all_test = await tests.get_all_tests()
            values = list()
            for t in all_test:
                values.append(int(t.id_test))
            id_test = await get_unique_key(values)
            await state.update_data(current_test=id_test)
            await tests.add_test(id_event=id, setting_time=time, setting_passing=passing, id_test=id_test, name=test_name)

            await tests.decrement_tests(query.from_user.id)

            user = await users.get_current_user(query.from_user.id)
            await query.message.answer(f"✔️Тест успешно создан. Количество оставшихся тестов: <b>{user.c_tests}</b>", parse_mode=ParseMode.HTML)
            await query.message.answer("❔Можете приступить к заполнению вопросами", reply_markup=ikb_adding_questions())
            await state.update_data(setting_passing="")
            await state.update_data(setting_time="")
            await state.update_data(setting_name="")
        except Exception as err:
            await query.message.answer("❌При создании теста возникла ошибка", reply_markup=ikb_back())
            await log_exceptions1("create_test_final", "ERROR", "create_test.py", 339, err, query.from_user.id)
    else:
        await query.message.answer(f"""📝Название теста: <b>{test_name if test_name else "⛔Пока не определено"}</b> 
🕘Время на выполнение теста: <b>{str(time) + " минут" if time else "⛔Пока не определено"}</b>
🕘Время существования теста: <b>{decode_lifetime(passing)}</b>

✍️Пожалуйста, заполните недостающие настройки теста""", reply_markup=ikb_settings_test(), parse_mode=ParseMode.HTML)














@router.callback_query(Current.event, F.data =="create_quiz")
async def second(query: CallbackQuery, state: FSMContext):






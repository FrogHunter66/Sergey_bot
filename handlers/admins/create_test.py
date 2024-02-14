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
from keyboard.ikb_all_events import ikb_all_events, Choose_event
from keyboard.ikb_current_test import ikb_current_test
from keyboard.ikb_settings_test import ikb_settings_test
from keyboard.ikb_timer import ikb_timer, Choose_timeer
from keyboard.ikb_adding_questions import ikb_adding_questions
from keyboard.ikb_types_questions import ikb_types_of_questions
from keyboard.list_tests import ikb_all_tests
from utils.db_api.quck_commands import tests
router = Router()

@router.message(
    Command("stadfgfhdfgrt"),
    Admin()
)
async def first(message: Message):
    await message.answer("Приветствую, админ, выбери действие", reply_markup=ikb_main_menu())


@router.callback_query(Choose_event.filter(F.cb=="ikb_choose"))
async def second(query: CallbackQuery, callback_data: Choose_event, state: FSMContext):
    data = await event.get_event(callback_data.id)
    name = data.event_name
    await query.message.answer(f"Выберите действие для мероприятия '{name}'", reply_markup=ikb_current_test())
    await state.set_state(Current.event)
    await state.update_data(event_id=callback_data.id)
    await state.update_data(event=name)



@router.callback_query(Current.event, F.data == "create_test")
async def add_test(query: CallbackQuery, state: FSMContext):
    await query.message.answer("""Выберите настройки опроса:
1) Код доступа по которому пользователи смогут получить доступ к тесту
2) Время на прохождение теста
3) Время через которое тест перестанет быть действительным""", reply_markup=ikb_settings_test())


@router.callback_query(Current.event, F.data == "access_code")
async def add_test2(query: CallbackQuery, state: FSMContext):
    await state.set_state(Current.setting_code)
    await query.message.answer("Напишите код по которому будет осуществлен доступ к тесту", reply_markup=ikb_back())


@router.callback_query(Current.event, F.data == "time_to_answer")
async def add_test2(query: CallbackQuery, state: FSMContext):
    await state.set_state(Current.setting_passing)
    await query.message.answer("Выберите ограничение по времени выполнения теста, выразите в минутах", reply_markup=ikb_back())


@router.callback_query(Current.event, F.data == "time_of_test")
async def add_test2(query: CallbackQuery, state: FSMContext):
    await state.set_state(Current.setting_time)
    await query.message.answer("Выберите ограничение по времени существования теста, выразите в минутах", reply_markup=ikb_timer())


@router.message(Current.setting_passing, Admin())
async def add_test3(message: Message, state: FSMContext):
    code = message.text
    try:
        code = int(code)
        if code > 0:
            code = int(code)
            await state.update_data(setting_passing=code)
            await message.answer(f"Время на прохождение теста успешно установлено [{code}]")
            await message.answer("""
1) Код доступа по которому пользователи смогут получить доступ к тесту 
2) Время на прохождение теста 
3) Время через которое тест перестанет быть действительным""", reply_markup=ikb_settings_test())
        else:
            await message.answer("Время должно быть натуральным числом")
            await message.answer("""
1) Код доступа по которому пользователи смогут получить доступ к тесту 
2) Время на прохождение теста 
3) Время через которое тест перестанет быть действительным""", reply_markup=ikb_settings_test())
        await state.set_state(Current.event)
    except:
        await state.set_state(Current.event)
        await message.answer("Время может быть только численнного формата")
        await message.answer("""
1) Код доступа по которому пользователи смогут получить доступ к тесту 
2) Время на прохождение теста 
3) Время через которое тест перестанет быть действительным""", reply_markup=ikb_settings_test())


@router.message(Current.setting_code, Admin())
async def add_test3(message: Message, state: FSMContext):
    code = message.text
    try:
        code = int(code)
        if code > 0:
            is_unique = True
            data_tests = await tests.get_all_tests()
            for test in data_tests:
                if test.token == code:
                    is_unique = False
                    break
            if is_unique:
                code = int(code)
                await state.update_data(setting_code=code)
                await message.answer(f"Время на прохождение теста успешно установлено [{code}]")
                await message.answer("""1) Код доступа по которому пользователи смогут получить доступ к тесту 
2) Время на прохождение теста 
3) Время через которое тест перестанет быть действительным""", reply_markup=ikb_settings_test())

            else:
                await message.answer("Данный код доступа уже используется в другом тесте. Придумайте другой код")
                await message.answer("""1) Код доступа по которому пользователи смогут получить доступ к тесту 
2) Время на прохождение теста 
3) Время через которое тест перестанет быть действительным""",
                                     reply_markup=ikb_settings_test())
        else:
            await message.answer("Время должно быть натуральным числом")
            await message.answer("""
        1) Код доступа по которому пользователи смогут получить доступ к тесту 
        2) Время на прохождение теста 
        3) Время через которое тест перестанет быть действительным""", reply_markup=ikb_settings_test())
        await state.set_state(Current.event)
    except:
        await state.set_state(Current.event)
        await message.answer("Код может быть только численнного формата")
        await message.answer("""
1) Код доступа по которому пользователи смогут получить доступ к тесту 
2) Время на прохождение теста 
3) Время через которое тест перестанет быть действительным""", reply_markup=ikb_settings_test())


@router.callback_query(Current.setting_time, Choose_timeer.filter(F.cb=="ikb_time"))
async def add_test2(query: CallbackQuery, state: FSMContext, callback_data: Choose_timeer):
    await state.update_data(setting_time=callback_data.id)

    await query.message.answer(f"Время существования теста успешно установленно [{callback_data.id}]")
    await query.message.answer("""
1) Код доступа по которому пользователи смогут получить доступ к тесту 
2) Время на прохождение теста 
3) Время через которое тест перестанет быть действительным""", reply_markup=ikb_settings_test())
    await state.set_state(Current.event)


@router.callback_query(Current.event, F.data == "ikb_create_questions")
async def add_test2(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    id = data.get("event_id")
    code = data.get("setting_code")
    passing = data.get("setting_passing")
    time = data.get("setting_time")
    if code and passing and time:
        try:
            all_test = await tests.get_all_tests()
            await tests.add_test(id_event=id, setting_code=code, setting_time=time, setting_passing=passing, id_test=len(all_test)+1)
            await query.message.answer("Можете приступить к заполнению вопросами", reply_markup=ikb_adding_questions())
            await state.update_data(setting_code="")
            await state.update_data(setting_passing="")
            await state.update_data(setting_time="")
        except Exception as err:
            await query.message.answer("При создании опроса возникла ошибка", reply_markup=ikb_back())
            print(err)
    else:
        await query.message.answer(f"""Код доступа - {code if code else "Не заполненно"}
Время на прохождение теста - {time if time else "Не выбрано"}
Время существования теста - {passing if passing else "Не выбрано"}
Пожалуйста, заполните недостающие настройки теста
1) Код доступа по которому пользователи смогут получить доступ к тесту 
2) Время на прохождение теста 
3) Время через которое тест перестанет быть действительным""", reply_markup=ikb_settings_test())
        # if (not code) and passing and time:
        #     await query.message.answer("Вы не указали код доступа", ikb_settings_test())
        # if code and (not passing) and time:
        #     await query.message.answer("Вы не указали время на прохождение", ikb_settings_test())
        # if code and passing and (not time):
        #     await query.message.answer("Вы не указали время существования теста", ikb_settings_test())
        # else:
        #     await query.message.answer("Ошибка", reply_markup=ikb_settings_test())


@router.callback_query(Current.event, F.data == "create_question")
async def add_test2(query: CallbackQuery, state: FSMContext):
    await query.message.answer("""Выберите тип вопроса:
1 тип - вопрос с единственным правильным ответом
2 тип - вопрос с множественными правильными ответами""", reply_markup=ikb_types_of_questions())


@router.callback_query(Current.event, F.data == "list_tests")
async def add_test2(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    id = data.get("event_id")
    print("id ", id)
    if id:
        kb = await ikb_all_tests(id)
        await query.message.answer("Список опросов", reply_markup=kb)
    else:
        await query.message.answer("Список опросов", reply_markup=ikb_back())


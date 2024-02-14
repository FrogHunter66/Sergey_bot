from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram import types
from aiogram.filters import Command

from keyboard.ikb_actions_question import ikb_actions_qustion, ikb_actions_rebuild_qustion
from keyboard.inline_main_menu import ikb_main_menu
from keyboard.ikb_back import ikb_back
from keyboard.save_event import ikb_save
from keyboard.ikb_all_events import ikb_all_events
from filters.is_admin import Admin
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
    #await state.update_data(event_id=callback_data.id)
    await state.update_data(event=name)


@router.callback_query(F.data == "ikb_qustions_rebuild", Current.current_test)
async def second(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    id = data.get("current_test")
    kb = await ikb_all_questions(id)
    await query.message.answer("Выберите действие", reply_markup=kb)


@router.callback_query(Current.current_test, F.data == "access_code")
async def add_test2(query: CallbackQuery, state: FSMContext):
    await state.set_state(Current.setting_code2)
    data = await state.get_data()
    id_ev = data.get("event_id")
    id_test = data.get("current_test")
    test = await tests.get_current(id_test=id_test, id_event=id_ev)
    current_code = test.token
    await query.message.answer(f"Напишите код по которому будет осуществлен доступ к тесту. Текущий код [{current_code}]", reply_markup=ikb_back())


@router.callback_query(Current.current_test, F.data == "time_to_answer")
async def add_test2(query: CallbackQuery, state: FSMContext):
    await state.set_state(Current.setting_passing2)
    data = await state.get_data()
    id_ev = data.get("event_id")
    id_test = data.get("current_test")
    test = await tests.get_current(id_test=id_test, id_event=id_ev)
    time = test.bound_time
    await query.message.answer(f"Выберите ограничение по времени выполнения теста, выразите в минутах. текущее время - [{time}]", reply_markup=ikb_back())


@router.callback_query(Current.current_test, F.data == "time_of_test")
async def add_test2(query: CallbackQuery, state: FSMContext):
    await state.set_state(Current.setting_time2)
    data = await state.get_data()
    id_ev = data.get("event_id")
    id_test = data.get("current_test")
    test = await tests.get_current(id_test=id_test, id_event=id_ev)
    time = test.lifetime
    await query.message.answer(f"Выберите ограничение по времени существования теста, выразите в минутах. Текущее время установленно - [{time}]", reply_markup=ikb_timer())


@router.message(Current.setting_passing2, Admin())
async def add_test3(message: Message, state: FSMContext):
    code = message.text
    try:
        code = int(code)
        data = await state.get_data()
        id_ev = data.get("event_id")
        test_id = data.get("current_test")
        await tests.update_bound_time(id_event=id_ev, id_test=test_id, new_time=code)
        await state.set_state(Current.current_test)
        await message.answer(f"Время на прохождения теста успешно установленно [{code}]")
        await message.answer("""1) Код доступа по которому пользователи смогут получить доступ к тесту
    2) Время на прохождение теста
    3) Время через которое тест перестанет быть действительным""", reply_markup=ikb_rebuild())
    except:
        await state.set_state(Current.current_test)
        await message.answer("Время может быть только численнного формата")
        await message.answer("""1) Код доступа по которому пользователи смогут получить доступ к тесту 
    2) Время на прохождение теста 
    3) Время через которое тест перестанет быть действительным""", reply_markup=ikb_rebuild())


@router.message(Current.setting_code2, Admin())
async def add_test3(message: Message, state: FSMContext):
    code = message.text
    data = await state.get_data()
    id_ev = data.get("event_id")
    test_id = data.get("current_test")
    try:
        code = int(code)
        if code > 0:
            is_unique = True
            data_tests = await tests.get_all_tests()
            for test in data_tests:
                print(test.token)
                if test.token == code:
                    is_unique = False
                    break
            if is_unique:
                code = int(code)
                print(test_id)
                await tests.update_code(id_event=id_ev, id_test=test_id, new_code=code)
                await message.answer(f"Код доступа к тесту успешно установлен [{code}]")
                await message.answer("""1) Код доступа по которому пользователи смогут получить доступ к тесту 
2) Время на прохождение теста 
3) Время через которое тест перестанет быть действительным""", reply_markup=ikb_rebuild())
            else:
                await message.answer("Данный код доступа уже используется в другом тесте. Придумайте другой код")
                await message.answer("""1) Код доступа по которому пользователи смогут получить доступ к тесту 
2) Время на прохождение теста 
3) Время через которое тест перестанет быть действительным""",
                                     reply_markup=ikb_rebuild())
        else:
            await message.answer("Код доступа должен быть натуральным числом")
            await message.answer("""1) Код доступа по которому пользователи смогут получить доступ к тесту 
2) Время на прохождение теста 
3) Время через которое тест перестанет быть действительным""", reply_markup=ikb_rebuild())
        await state.set_state(Current.current_test)
    except:
        await state.set_state(Current.current_test)
        await message.answer("Код доступа может быть только численнного формата")
        await message.answer("""1) Код доступа по которому пользователи смогут получить доступ к тесту 
2) Время на прохождение теста 
3) Время через которое тест перестанет быть действительным""", reply_markup=ikb_settings_test())


@router.callback_query(Current.setting_time2, Choose_timeer.filter(F.cb=="ikb_time"))
async def add_test2(query: CallbackQuery, state: FSMContext, callback_data: Choose_timeer):
    await state.update_data(setting_time=callback_data.id)
    data = await state.get_data()
    id_ev = data.get("event_id")
    test_id = data.get("current_test")
    await tests.update_lifetime(id_event=id_ev, id_test=test_id, new_time=callback_data.id)
    await query.message.answer(f"Время существования теста успешно установленно [{callback_data.id}]")
    await query.message.answer("""1) Код доступа по которому пользователи смогут получить доступ к тесту 
2) Время на прохождение теста 
3) Время через которое тест перестанет быть действительным""", reply_markup=ikb_rebuild())
    await state.set_state(Current.current_test)




@router.callback_query(F.data == "ikb_add_to_current", Current.current_test)
async def second(query: CallbackQuery, state: FSMContext):
    await state.set_state(Current.event)
    await query.message.answer("""Выберите тип вопроса:
1 тип - вопрос с единственным правильным ответом
2 тип - вопрос с множественным выбором""", reply_markup=ikb_types_of_questions())


@router.callback_query(Choose_quest.filter(F.cb=="ikb_pickquestion"), Current.current_test)
async def rebuild_current_quest(querry: CallbackQuery, state: FSMContext, callback_data: Choose_quest):
    id_quest = callback_data.id
    curr_quest = await questions.get_current(id_quest)
    await state.update_data(current_quest=id_quest)
    if curr_quest:
        await state.set_state(Current.rebuild_quest) #todo Нужна новая клавиатура которая позволит удалять вопрос, очищать данные вопроса по отдельности, запись данных напрямую в бд без создания нового вопроса
        varss = curr_quest.variants
        vars = list(map(str, varss.split(".*.")))
        if curr_quest.type == 2:
            correct = list(map(str, curr_quest.correct_answer.split(".*.")))
            await querry.message.answer(
                f"""Вы в редакторе вопроса {curr_quest.id_quest} с выбором {" единственного правильно ответа" if curr_quest.type == 1 else " множественного правильного ответа "}, выберите что бы вы хотели изменить:
Текст вопроса -
{curr_quest.text if curr_quest.text else "Не заполненно"}

Варианты ответа -
{vars if vars else "Не заполненно"}

Правильный ответ
{correct if correct else "Не заполненно"}""", reply_markup=ikb_actions_rebuild_qustion())
            await state.update_data(question=curr_quest.text)
            await state.update_data(type=2)
            await state.update_data(variants=vars)
            await state.update_data(correct=correct)
        else:
            correct = curr_quest.correct_answer
            await querry.message.answer(f"""
Вы в редакторе вопроса {curr_quest.id_quest} с выбором {" единственного правильно ответа" if curr_quest.type == 1 else " множественного правильного ответа "}, выберите что бы вы хотели изменить:
Текст вопроса -
{curr_quest.text if curr_quest.text else "Не заполненно"}

Варианты ответа -
{vars if vars else "Не заполненно"}

Правильный ответ
{correct if correct else "Не заполненно"}""", reply_markup=ikb_actions_rebuild_qustion())
            await state.update_data(question=curr_quest.text)
            await state.update_data(type=1)
            await state.update_data(variants=vars)
            await state.update_data(correct=correct)
    else:
        await querry.answer("Произошла ошибка")



@router.callback_query(F.data == "ikb_save_quest_changes", Current.rebuild_quest)
async def second(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("question")
    variants = data.get("variants")
    correct = data.get("correct")
    id_test = data.get("current_test")
    typee = data.get("type")
    try:
        await questions.change_correct(id_quest=id_test, new_correct=correct)
        await questions.change_text(id_quest=id_test, new_text=text)
        await questions.change_vars(id_quest=id_test, new_vars=variants)
        await query.message.answer("Данные успешно сохранены")
        kb = await ikb_all_questions(id_test)
        await query.message.answer("Выберите действие", reply_markup=kb)
        await state.set_state(Current.current_test)
    except Exception as err:
        await state.set_state(Current.current_test)
        await query.message.answer("Произошла ошибка")
        await query.message.answer(
f"""Вы в редакторе вопроса {id_test} с выбором {" единственного правильно ответа" if typee == 1 else " множественного правильного ответа "}, выберите что бы вы хотели изменить:
Текст вопроса -
{text if text else "Не заполненно"}

Варианты ответа -
{variants if variants else "Не заполненно"}

Правильный ответ
{correct if correct else "Не заполненно"}""", reply_markup=ikb_actions_rebuild_qustion())
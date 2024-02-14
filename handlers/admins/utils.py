from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.types import Message, InlineKeyboardButton
from aiogram import types
from aiogram.filters import Command

from keyboard.ikb_actions_question import ikb_actions_qustion
from keyboard.ikb_all_events import ikb_all_events
from keyboard.ikb_current_test import ikb_current_test
from keyboard.ikb_rebuilding_test import ikb_rebuild
from keyboard.ikb_settings_test import ikb_settings_test
from keyboard.ikb_types_questions import ikb_types_of_questions
from keyboard.inline_main_menu import ikb_main_menu
from keyboard.ikb_back import ikb_back
from filters.is_admin import Admin
from keyboard.list_questions import ikb_all_questions
from keyboard.list_tests import ikb_all_tests
from utils.db_api.quck_commands import event
from aiogram.fsm.context import FSMContext
from states.fsm import Current, Current2
from aiogram.fsm.state import StatesGroup, State
router = Router()
#todo Прописать все бэки



@router.callback_query(F.data == "ikb_back", Current.event)
async def second(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Приветствую, дорогой админ, выберите действие", reply_markup=ikb_main_menu())


@router.callback_query(F.data == "ikb_back_list_events", Current.event)
async def second(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    ikb = await ikb_all_events()
    await callback.message.answer('Вот они, крассучики', reply_markup=ikb)


@router.callback_query(F.data == "ikb_back_actions", Current.event)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get("event")
    await callback.message.answer(f"Выберите действие для мероприятия '{name}'", reply_markup=ikb_current_test())


@router.callback_query(F.data == "ikb_back_choose_type", Current.event)
async def second(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("""Выберите тип вопроса:
1 тип - вопрос с единственным правильным ответом
2 тип - вопрос с множественными правильными ответами""", reply_markup=ikb_types_of_questions())



@router.callback_query(F.data == "ikb_back_choose_questionnn", Current.event)
async def second(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Current.current_test)
    data = await state.get_data()
    id = data.get("current_test")
    kb = await ikb_all_questions(id)
    await callback.message.answer("Выберите действие", reply_markup=kb)
    print("3")


@router.callback_query(F.data == "ikb_back_tochoose_opros", Current.event)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get("event")
    await callback.message.answer(f"Выберите действие для мероприятия '{name}'", reply_markup=ikb_current_test())


@router.callback_query(F.data == "ikb_back", Current2.correct)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("text")
    variants = data.get("variants")
    correct = data.get("correct")
    await callback.message.answer(f"""Вы в конструктуоре вопроса с множественным ответом выберите действие
    Предпросмотр вопроса - 
    Текст вопроса:
    {text if text else "Пока не заполненно"}
    ------------------------------------------------------
    Варианты ответа:
    {variants if variants else "Пока не заполненно"}
    ------------------------------------------------------
    Правильные ответы:
    {correct if correct else "Пока не заполненно"}""", reply_markup=ikb_actions_qustion())
    await state.set_state(Current2.event)


@router.callback_query(F.data == "ikb_back", Current2.question)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("text")
    variants = data.get("variants")
    correct = data.get("correct")
    await callback.message.answer(f"""Вы в конструктуоре вопроса с множественным ответом выберите действие
    Предпросмотр вопроса - 
    Текст вопроса:
    {text if text else "Пока не заполненно"}
    ------------------------------------------------------
    Варианты ответа:
    {variants if variants else "Пока не заполненно"}
    ------------------------------------------------------
    Правильные ответы:
    {correct if correct else "Пока не заполненно"}""", reply_markup=ikb_actions_qustion())
    await state.set_state(Current2.event)


@router.callback_query(F.data == "ikb_back", Current2.variants)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("text")
    variants = data.get("variants")
    correct = data.get("correct")
    await callback.message.answer(f"""Вы в конструктуоре вопроса с множественным ответом выберите действие
    Предпросмотр вопроса - 
    Текст вопроса:
    {text if text else "Пока не заполненно"}
    ------------------------------------------------------
    Варианты ответа:
    {variants if variants else "Пока не заполненно"}
    ------------------------------------------------------
    Правильные ответы:
    {correct if correct else "Пока не заполненно"}""", reply_markup=ikb_actions_qustion())
    await state.set_state(Current2.event)


@router.callback_query(F.data == "ikb_back", Current.correct)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("text")
    variants = data.get("variants")
    correct = data.get("correct")
    await callback.message.answer(f"""Вы в конструктуоре вопроса с множественным ответом выберите действие
    Предпросмотр вопроса - 
    Текст вопроса:
    {text if text else "Пока не заполненно"}
    ------------------------------------------------------
    Варианты ответа:
    {variants if variants else "Пока не заполненно"}
    ------------------------------------------------------
    Правильные ответы:
    {correct if correct else "Пока не заполненно"}""", reply_markup=ikb_actions_qustion())
    await state.set_state(Current.event)


@router.callback_query(F.data == "ikb_back", Current.question)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("text")
    variants = data.get("variants")
    correct = data.get("correct")
    await callback.message.answer(f"""Вы в конструктуоре вопроса с множественным ответом выберите действие
    Предпросмотр вопроса - 
    Текст вопроса:
    {text if text else "Пока не заполненно"}
    ------------------------------------------------------
    Варианты ответа:
    {variants if variants else "Пока не заполненно"}
    ------------------------------------------------------
    Правильные ответы:
    {correct if correct else "Пока не заполненно"}""", reply_markup=ikb_actions_qustion())
    await state.set_state(Current.event)


@router.callback_query(F.data == "ikb_back", Current.variants)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("text")
    variants = data.get("variants")
    correct = data.get("correct")
    await callback.message.answer(f"""Вы в конструктуоре вопроса с множественным ответом выберите действие
    Предпросмотр вопроса - 
    Текст вопроса:
    {text if text else "Пока не заполненно"}
    ------------------------------------------------------
    Варианты ответа:
    {variants if variants else "Пока не заполненно"}
    ------------------------------------------------------
    Правильные ответы:
    {correct if correct else "Пока не заполненно"}""", reply_markup=ikb_actions_qustion())
    await state.set_state(Current.event)


#-----------------------------------------------------


@router.callback_query(F.data == "ikb_back", Current.setting_time2)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data_state = await state.get_data()
    num = data_state.get("current_test")
    name = data_state.get("event")
    await callback.message.answer(f"Выберите действие для теста номер '{num}' в мероприятии '{name}'", reply_markup=ikb_rebuild())
    await state.set_state(Current.current_test)


@router.callback_query(F.data == "ikb_back", Current.setting_passing2)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data_state = await state.get_data()
    num = data_state.get("current_test")
    name = data_state.get("event")
    await callback.message.answer(f"Выберите действие для теста номер '{num}' в мероприятии '{name}'", reply_markup=ikb_rebuild())
    await state.set_state(Current.current_test)


@router.callback_query(F.data == "ikb_back", Current.setting_code2)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data_state = await state.get_data()
    num = data_state.get("current_test")
    name = data_state.get("event")
    await callback.message.answer(f"Выберите действие для теста номер '{num}' в мероприятии '{name}'", reply_markup=ikb_rebuild())
    await state.set_state(Current.current_test)

#-----------------------------------------------------------------


@router.callback_query(F.data == "ikb_back", Current.setting_time)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data_state = await state.get_data()
    num = data_state.get("current_test")
    name = data_state.get("event")
    await callback.message.answer("""Выберите настройки опроса:
1) Код доступа по которому пользователи смогут получить доступ к тесту
2) Время на прохождение теста
3) Время через которое тест перестанет быть действительным""", reply_markup=ikb_settings_test())
    await state.set_state(Current.event)


@router.callback_query(F.data == "ikb_back", Current.setting_passing)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data_state = await state.get_data()
    num = data_state.get("current_test")
    name = data_state.get("event")
    await callback.message.answer("""Выберите настройки опроса:
1) Код доступа по которому пользователи смогут получить доступ к тесту
2) Время на прохождение теста
3) Время через которое тест перестанет быть действительным""", reply_markup=ikb_settings_test())
    await state.set_state(Current.event)


@router.callback_query(F.data == "ikb_back", Current.setting_code)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data_state = await state.get_data()
    num = data_state.get("current_test")
    name = data_state.get("event")
    await callback.message.answer("""Выберите настройки опроса:
1) Код доступа по которому пользователи смогут получить доступ к тесту
2) Время на прохождение теста
3) Время через которое тест перестанет быть действительным""", reply_markup=ikb_settings_test())
    await state.set_state(Current.event)

#------------------------------------------------------


@router.callback_query(F.data == "ikb_back_actions", Current.current_test)
async def second(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Current.event)
    data = await state.get_data()
    id = data.get("event_id")
    print("id ", id)

    if id:
        kb = await ikb_all_tests(id)
        await callback.message.answer("Список опросов", reply_markup=kb)
    else:
        await callback.message.answer("Список опросов", reply_markup=ikb_back())


@router.callback_query(Current.current_test, F.data == "ikb_back_all_questions")
async def add_test2(query: types.CallbackQuery, state: FSMContext):
    data_state = await state.get_data()
    name = data_state.get("event")
    num = data_state.get("current_test")
    await state.update_data(current_test=num)
    await query.message.answer(f"Выберите действие для теста номер '{num}' в мероприятии '{name}'", reply_markup=ikb_rebuild())


@router.callback_query(Current.event, F.data == "ikb_back_all_questions")
async def add_test2(query: types.CallbackQuery, state: FSMContext):
    data_state = await state.get_data()
    name = data_state.get("event")
    num = data_state.get("current_test")
    await state.update_data(current_test=num)
    await query.message.answer(f"Выберите действие для теста номер '{num}' в мероприятии '{name}'", reply_markup=ikb_rebuild())


@router.callback_query(F.data == "ikb_back")
async def second(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Приветствую, дорогой админ, выберите действие", reply_markup=ikb_main_menu())
import datetime

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
from utils.db_api.quck_commands import tests, questions
from aiogram.enums import ParseMode
router = Router()


def decode_lifetime(lifetime):
    try:
        if lifetime[-1] == "m":
            return lifetime[:-1] + " минут"
        elif lifetime[-1] == "h":
            return lifetime[:-1] + " часов"
        elif lifetime[-1] == "d":
            return lifetime[:-1] + " дней"
        elif lifetime == "without":
            return "Неограниченно"
    except:
        return "⛔Пока не определен"


@router.callback_query(Choose_test.filter(F.cb == "ikb_tests"), Current.event)
async def second(query: CallbackQuery, callback_data: Choose_test, state: FSMContext):
    data_state = await state.get_data()
    id = data_state.get("event_id")
    current_test = await tests.get_current(id_event=id, id_test=callback_data.id)
    num = current_test.id_test
    name = data_state.get("event")
    bound = current_test.bound_time
    current_time = datetime.datetime.utcnow()
    current_time = current_time.replace(tzinfo=datetime.timezone.utc, microsecond=0)
    end_time = current_test.end_time.replace(microsecond=0)
    differ = end_time - current_time
    days = differ.days
    hours, remainder = divmod(differ.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    await state.update_data(current_test=num)
    await state.update_data(setting_name=current_test.name)
    if end_time < current_time:
        await query.message.answer(f"""<b>Вы в панели действий для теста</b> {current_test.name} 

<b>Мероприятия</b> {name}

<b>Текущие настройки:</b>
🕒<b>Время на выполнение</b> теста: {bound} минут
🕒<b>Время существования</b> теста: ⛔Истекло 

⚡<b>Выберите действие</b>⚡""", reply_markup=ikb_rebuild(), parse_mode=ParseMode.HTML)
    else:
        await query.message.answer(f"""<b>Вы в панели действий для теста</b> {current_test.name} 
    
<b>Мероприятия</b> {name}
    
<b>Текущие настройки:</b>
🕒<b>Время на выполнение</b> теста: {bound} минут
🕒<b>Время существования</b> теста: {days} д {hours:02}:{minutes:02}:{seconds:02}
    
⚡<b>Выберите действие</b>⚡""", reply_markup=ikb_rebuild(), parse_mode=ParseMode.HTML)
    await state.set_state(Current.current_test)
    await state.update_data(event=name)


@router.callback_query(F.data == "ikb_qustions_rebuild", Current.current_test)
async def second(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    id = data.get("current_test")
    kb = await ikb_all_questions(id)
    await query.message.answer("⚡Выберите действие⚡", reply_markup=kb)



@router.callback_query(Current.current_test, F.data == "ikb_name_for_test")
async def add_test2(query: CallbackQuery, state: FSMContext):

    await state.set_state(Current.setting_name2)

    data = await state.get_data()
    id_ev = data.get("event_id")
    id_test = data.get("current_test")
    test = await tests.get_current(id_test=id_test, id_event=id_ev)
    print(test)
    print("id_test", id_test)
    current_name = test.name
    await query.message.answer(f"""📝Укажите имя теста
<b>Текущее имя:</b> {current_name}""", reply_markup=ikb_back(), parse_mode=ParseMode.HTML)


@router.callback_query(Current.current_test, F.data == "time_to_answer")
async def add_test2(query: CallbackQuery, state: FSMContext):
    await state.set_state(Current.setting_passing2)
    data = await state.get_data()
    id_ev = data.get("event_id")
    id_test = data.get("current_test")
    test = await tests.get_current(id_test=id_test, id_event=id_ev)
    time = test.bound_time
    await query.message.answer(f"""🕒Выберите ограничение по времени выполнения теста, выразите в минутах
*Текущее время {time} минут*""", parse_mode=ParseMode.MARKDOWN_V2)


@router.callback_query(Current.current_test, F.data == "time_of_test")
async def add_test2(query: CallbackQuery, state: FSMContext):
    await state.set_state(Current.setting_time2)
    data = await state.get_data()
    id_ev = data.get("event_id")
    id_test = data.get("current_test")
    test = await tests.get_current(id_test=id_test, id_event=id_ev)
    time = test.lifetime
    await query.message.answer(f"""🕒Выберите ограничение по времени существования теста
*Текущее время установлено:* {decode_lifetime(time)}""", reply_markup=ikb_timer(), parse_mode=ParseMode.MARKDOWN_V2)


@router.message(Current.setting_passing2, Admin())
async def add_test3(message: Message, state: FSMContext):
    code = message.text
    data = await state.get_data()
    id_ev = data.get("event_id")
    test_id = data.get("current_test")
    current_test = await tests.get_current(1, test_id)
    try:
        code = int(code)
        await tests.update_bound_time(id_event=id_ev, id_test=test_id, new_time=code)
        await state.set_state(Current.current_test)
        await message.answer(f"✅Время на прохождения теста успешно установлено: *{code}* минут", parse_mode=ParseMode.MARKDOWN_V2)
        await message.answer(f"""📝<b>Название теста:</b> {current_test.name if current_test.name else "⛔Пока не определен"}  
🕒<b>Время на выполнение</b> теста: {code} минут
🕒<b>Время существования</b> теста: {decode_lifetime(current_test.lifetime)}""", reply_markup=ikb_rebuild(), parse_mode=ParseMode.HTML)
    except:
        await state.set_state(Current.current_test)
        await message.answer("❌Время может быть *только численнного* формата", parse_mode=ParseMode.MARKDOWN_V2)
        await message.answer(f"""📝<b>Название теста:</b> {current_test.name if current_test.name else "⛔Пока не определен"}  
🕒<b>Время на выполнение</b> теста: {current_test.bound_time if current_test.bound_time else "⛔Пока не определен"} минут
🕒<b>Время существования</b> теста: {decode_lifetime(current_test.lifetime)}""", reply_markup=ikb_rebuild(), parse_mode=ParseMode.HTML)


@router.message(Current.setting_name2, Admin())
async def add_test3(message: Message, state: FSMContext):
    data = await state.get_data()
    id_test = data.get("current_test")
    code = message.text
    test_id = data.get("current_test")
    current_test = await tests.get_current(1, test_id)
    await tests.update_name(id_test=id_test, id_event=1, new_name=code)
    await message.answer(f"✅Название теста успешно установлено <b>{code}</b>", parse_mode=ParseMode.HTML)
    await message.answer(f"""📝<b>Название теста:</b> {code}  
🕒<b>Время на выполнение</b> теста: {current_test.bound_time if current_test.bound_time else "⛔Пока не определен"} минут
🕒<b>Время существования</b> теста: {decode_lifetime(current_test.lifetime)}""", reply_markup=ikb_rebuild(), parse_mode=ParseMode.HTML)
    await state.set_state(Current.current_test)




@router.callback_query(Current.setting_time2, Choose_timeer.filter(F.cb=="ikb_time"))
async def add_test2(query: CallbackQuery, state: FSMContext, callback_data: Choose_timeer):
    await state.update_data(setting_time=callback_data.id)
    data = await state.get_data()
    id_ev = data.get("event_id")
    test_id = data.get("current_test")
    current_test = await tests.get_current(1, test_id)
    await tests.update_lifetime(id_event=id_ev, id_test=test_id, new_time=callback_data.id)
    await query.message.answer(f"✅Время существования теста успешно установлено {decode_lifetime(callback_data.id)}", parse_mode=ParseMode.MARKDOWN_V2)
    await query.message.answer(f"""📝<b>Название теста:</b> {current_test.name if current_test.name else "⛔Пока не определен"}  
🕒<b>Время на выполнение</b> теста: {current_test.bound_time if current_test.bound_time else "⛔Пока не определен"} минут
🕒<b>Время существования</b> теста: {decode_lifetime(callback_data.id)}""", reply_markup=ikb_rebuild(), parse_mode=ParseMode.HTML)
    await state.set_state(Current.current_test)




@router.callback_query(F.data == "ikb_add_to_current", Current.current_test)
async def second(query: CallbackQuery, state: FSMContext):
    await state.set_state(Current.event)
    await query.message.answer("""✏️Выберите тип вопроса:
1️⃣1 тип \- вопрос с единственным правильным ответом
🔢2 тип \- вопрос с множественным выбором""", reply_markup=ikb_types_of_questions(), parse_mode=ParseMode.MARKDOWN_V2)


@router.callback_query(Choose_quest.filter(F.cb=="ikb_pickquestion"), Current.current_test)
async def rebuild_current_quest(querry: CallbackQuery, state: FSMContext, callback_data: Choose_quest):
    id_quest = callback_data.id
    curr_quest = await questions.get_current(id_quest)
    await state.update_data(current_quest=id_quest)
    await state.set_state(Current.rebuild_quest)
    if curr_quest: #todo Нужна новая клавиатура которая позволит удалять вопрос, очищать данные вопроса по отдельности, запись данных напрямую в бд без создания нового вопроса
        varss = curr_quest.variants
        vars = None
        if varss:
            vars = list(map(str, varss.split(".*.")))
            vars = "\n".join(f"{index}. {element}" for index, element in enumerate(vars, start=1))
        if curr_quest.type == 2:
            correct = list(map(str, curr_quest.correct_answer.split(".*.")))
            correct = "\n".join(f"{index}. {element}" for index, element in enumerate(correct, start=1))
            await querry.message.answer(f"""🛠️Вы в редакторе вопроса с выбором <b>{"единственного правильно ответа" if curr_quest.type == 1 else " множественного правильного ответа "}</b> 
Выберите что бы вы хотели изменить:

<b>Текст вопроса</b>
{curr_quest.text if curr_quest.text else "❌Не заполненно"}

<b>Варианты ответа</b>
{vars if vars else "❌Не заполненно"}

<b>Правильный ответ</b>
{correct if correct else "❌Не заполненно"}""", reply_markup=ikb_actions_rebuild_qustion(), parse_mode=ParseMode.HTML)#parse_mode_был
            await state.update_data(question=curr_quest.text)
            await state.update_data(type=2)
            await state.update_data(variants=vars)
            await state.update_data(correct=correct)
        elif curr_quest.type == 1:
            correct = curr_quest.correct_answer
            await querry.message.answer(f"""🛠️Вы в редакторе вопроса с выбором <b>{" единственного правильно ответа" if curr_quest.type == 1 else " множественного правильного ответа "}</b>
Выберите что бы вы хотели изменить:

<b>Текст вопроса</b>
{curr_quest.text if curr_quest.text else "❌Не заполненно"}

<b>Варианты ответа</b>
{vars if vars else "❌Не заполненно"}

<b>Правильный ответ</b>
{correct if correct else "❌Не заполненно"}""", reply_markup=ikb_actions_rebuild_qustion(), parse_mode=ParseMode.HTML)#parse_mode_был
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
    id_quest = data.get("current_quest")
    id_test = data.get("current_test")
    typee = data.get("type")
    try:
        await query.message.answer("✔️Данные успешно сохранены")
        kb = await ikb_all_questions(id_test)
        await query.message.answer("⚡Выберите действие⚡", reply_markup=kb)
        await state.set_state(Current.current_test)
        await state.update_data(text=None)
        await state.update_data(variants=None)
        await state.update_data(correct=None)
        await state.update_data(type=None)
    except Exception as err:
        await log_exceptions1("change_quest", "ERROR", "commands_for_tests.py", 285, err, query.from_user.id)
        await query.message.answer("❌Произошла ошибка")
        await query.message.answer(f"""🛠️Вы в редакторе вопроса с выбором <b>{" единственного правильно ответа" if typee == 1 else " множественного правильного ответа "}</b>
Выберите что бы вы хотели изменить:

<b>Текст вопроса</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа</b>
{variants if variants else "❌Не заполненно"}

<b>Правильный ответ</b>
{correct if correct else "❌Не заполненно"}""", reply_markup=ikb_actions_rebuild_qustion(), parse_mode=ParseMode.HTML)#parse_mode_был

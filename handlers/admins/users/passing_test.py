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
from keyboard.users_kb.ikb_pass_test import ikb_pass_test, answer
from keyboard.users_kb.ikb_choose_quests import ikb_get_all_quests, Take_quest
from utils.db_api.quck_commands import tests, questions
from keyboard.users_kb.ikb_start_test import ikb_start_test
from keyboard.users_kb.ikb_back_code import ikb_back_code
from utils.db_api.quck_commands import users
router = Router()


def array_to_string(input_array):
    output_string = ""

    for i, element in enumerate(input_array, start=1):
        output_string += "\n{}. {}".format(i, element)

    return output_string


def deserialize_datetime(serialized_dt):
    return pickle.loads(bytes.fromhex(serialized_dt))


@router.callback_query(Take_quest.filter(F.cb=="ikb_quest"), User.choose_quest, Old_user())
async def take_quest(query: CallbackQuery, state: FSMContext, callback_data: Take_quest):

    id_quest = callback_data.id
    current_quest = await questions.get_current(id_quest)
    await state.update_data(current_quest=id_quest)
    text = current_quest.text
    variants = list(map(str, current_quest.variants.split(".*.")))
    variants = array_to_string(variants)
    type_quest = current_quest.type

    data = await state.get_data()
    end_time_not_serialized = data.get("time")
    end_time = deserialize_datetime(end_time_not_serialized)
    current_time = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    if end_time > current_time:
        differ = (end_time-current_time).replace(microsecond=0)
        if type_quest == 1:
            kb = await ikb_pass_test(id_quest)
            await query.message.answer(f"""Вопрос с единственным выбором ответа.
    Время до заврешения теста - {differ}
    
    {text}
    {variants}""", reply_markup=kb)
        elif type_quest == 2:
            kb = await ikb_pass_test(id_quest)

            await query.message.answer(f"""Вопрос со множественным выбором ответа.
            Время до заврешения теста - {differ}
            
            {text}
            {variants}""", reply_markup=kb)
        else:
            await query.message.answer("Еще какой то тип вопроса")
        await state.set_state(User.answer)
    else:
        await query.message.answer("Время на выполнение теста вышло")
        await state.clear()

#todo слишком примитивно
@router.callback_query(answer.filter(F.cb=="ikb_answer"), User.answer, Old_user())
async def take_quest(query: CallbackQuery, state: FSMContext, callback_data: answer):
    current_ans = callback_data.id
    data = await state.get_data()
    id_quest = data.get("current_quest")
    current_quest = await questions.get_current(id_quest)
    variants = list(map(str, current_quest.variants.split(".*.")))
    result = data.get("result")
    type_quest = current_quest.type
    if type_quest == 1:
        correct = current_quest.correct_answer
        if correct == variants[current_ans]:
            if result:
                result += '+'
                await state.update_data(result=result)
            else:
                await state.update_data(result="+")
        else:
            if result:
                result += '-'
                await state.update_data(result=result)
            else:
                await state.update_data(result="-")


    if type_quest == 2:

        correct = list(map(str, current_quest.correct_answer.split(".*.")))
        if variants[current_ans] in correct:
            if result:
                result += '+'
                await state.update_data(result=result)
            else:
                await state.update_data(result="+")
        else:
            if result:
                result += '-'
                await state.update_data(result=result)
            else:
                await state.update_data(result="-")


@router.callback_query(User.answer, F.data=="ikb_save_answer", Old_user())
async def save(query: CallbackQuery, state: FSMContext):
    await state.set_state(User.choose_quest)
    data = await state.get_data()
    id_test = data.get("current_test")
    kb = await ikb_get_all_quests(id_test)
    await query.message.answer(f"Выберите вопрос", reply_markup=kb)


@router.callback_query(User.choose_quest, F.data=="ikb_finish", Old_user())
async def save(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    res = data.get("result")
    minuses = res.count("-")
    pluses = res.count("+")
    await query.message.answer(f"Ваш результат - {pluses-1} правильных ответов, {minuses} - неправильных ответов")
    await state.clear()

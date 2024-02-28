from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram import types
from aiogram.filters import Command
from filters.is_admin import Admin
from keyboard.list_questions import ikb_all_questions
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
router = Router()

@router.message(
    Command("stadfgfhdfgrt"),
    Admin()
)
async def first(message: Message):
    await message.answer("Приветствую, админ, выбери действие", reply_markup=ikb_main_menu())


@router.callback_query(Current.event, F.data =="ikb_1st_type")
async def second(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.update_data(type=1)
    text = data.get("text")
    variants = data.get("variants")
    correct = data.get("correct")
    await query.message.answer(f"""Вы в конструктуоре вопроса выберите действие
Предпросмотр вопроса - 
Текст вопроса:
{text if text else "Пока не заполненно"}
------------------------------------------------------
Варианты ответа:
{variants if variants else "Пока не заполненно"}
------------------------------------------------------
Правильный ответ:
{correct if correct else "Пока не заполненно"}""", reply_markup=ikb_actions_qustion())



@router.callback_query(Current.event, F.data =="ikb_text_quest")
async def second(query: CallbackQuery, state: FSMContext):
    await query.message.answer("Введите текст вопроса", reply_markup=ikb_back())
    await state.set_state(Current.question)


@router.callback_query(Current.event, F.data =="ikb_add_variant")
async def second(query: CallbackQuery, state: FSMContext):
    await query.message.answer("Введите вариант ответа", reply_markup=ikb_back())
    await state.set_state(Current.variants)


@router.callback_query(Current.event, F.data =="ikb_correct_one")
async def second(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    variants = data.get("variants")
    if variants:
        lst_vars = list(map(str, variants.split(".*.")))
        response = "Варианты ответа: \n" + "\n".join(lst_vars)
        await query.message.answer(response)
    else:
        await query.message.answer("Вы пока не ввели правильный вариант ответа")
    await query.message.answer("Выберите ответ, который будет считаться правильным", reply_markup=ikb_back())
    await state.set_state(Current.correct)


#todo  бэки прописать для этой хуеты
@router.message(Current.question, Admin())
async def question(message: Message, state:FSMContext):
    text = message.text
    await state.update_data(question=text)
    data = await state.get_data()
    text = data.get("question")
    variants = data.get("variants")
    correct = data.get("correct")
    await message.answer(f"""Предпросмотр вопроса - 
Текст вопроса:
{text if text else "Пока не заполненно"}
------------------------------------------------------
Варианты ответа:
{variants if variants else "Пока не заполненно"}
------------------------------------------------------
Правильный ответ:
{correct if correct else "Пока не заполненно"}""", reply_markup=ikb_actions_qustion())
    await state.set_state(Current.event)


@router.message(Current.variants, Admin())
async def question(message: Message, state:FSMContext):
    data = await state.get_data()

    text = message.text
    var_old = (data.get("variants"))
    if var_old:
        vars = var_old + ".*." + text
        await state.update_data(variants=vars)
    else:
        await state.update_data(variants=text)
    data_new = await state.get_data()
    variants = data_new.get("variants")
    list_variants = list(map(str, variants.split(".*.")))
    text = data_new.get("question")
    correct = data_new.get("correct")
    await message.answer(f"""Вы в конструкторе вопроса с единственным выбором правильного ответа
Предпросмотр вопроса - 
Текст вопроса:
{text if text else "Пока не заполненно"}
------------------------------------------------------
Варианты ответа:
{list_variants if list_variants else "Пока не заполненно"}
------------------------------------------------------
Правильный ответ:
{correct if correct else "Пока не заполненно"}""", reply_markup=ikb_actions_qustion())
    await state.set_state(Current.event)


@router.message(Current.correct, Admin())
async def question(message: Message, state:FSMContext):
    text = message.text
    data = await state.get_data()
    vars = data.get("variants")
    qest = data.get("question")
    try:
        text = int(text)
        if vars:
            vars = list(map(str, vars.split(".*.")))
            if text > 0 and text <= len(vars):
                await state.update_data(correct=vars[text-1])
                await message.answer(f"Успешно установлен вариант ответа {text}: {vars[text-1]}")
                await message.answer(f"""Вы в конструкторе вопроса с единственным выбором правильного ответа

Предпросмотр вопроса -
Текст вопроса:
{qest if qest else "Пока не заполненно"}
------------------------------------------------------
Варианты ответа:
{vars if vars else "Пока не заполненно"}
------------------------------------------------------
Правильный ответ:
{vars[text-1] if vars[text-1] else "Пока не заполненно"}""", reply_markup=ikb_actions_qustion())
                await state.set_state(Current.event)
            else:
                await message.answer(f"Выберите вариант ответа от 1 до {len(vars)}", reply_markup=ikb_back()) #todo прописать бэк для Current.corect
        else:
            await message.answer("Ваианты еще не заполнены. Сперва заполните варианты ответа", ikb_actions_qustion())
            await state.set_state(Current.event)
    except:
        await message.answer(f"Выберите вариант ответа от 1 до {len(vars)}", reply_markup=ikb_back())

async def get_unique_value(values):
    for i in range(10000):
        if i not in values:
            return i

    return None


@router.callback_query(Current.event, F.data =="ikb_add_question_test")
async def second(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    quest = data.get("question")
    vars = data.get("variants")
    correct = data.get("correct")
    test_id = data.get("current_test")
    types = data.get("type")

    all_quests = await questions.get_all_quest()
    print(test_id)
    print(all_quests)
    print(correct)
    print(types)
    if quest and vars and correct:
        try:
            await questions.add_test(id_test=test_id, id_quest=len(all_quests)+1, correct_answer=correct, quest_type=types, variants=vars, text=quest)
            await query.message.answer("Вопрос успешно добавлен")
            kb = await ikb_all_questions(test_id)
            await query.message.answer("Выберите действие для вопросов", reply_markup=kb)
            await state.update_data(question='')
            await state.update_data(variants='')
            await state.update_data(correct='')
            await state.update_data(type='')
            await state.set_state(Current.current_test)
        except:
            await query.message.answer("Произошла ошибка")
            kb = await ikb_all_questions(test_id)
            await query.message.answer("Выберите действие для вопросов", reply_markup=kb)
    else:
        await query.message.answer(f"""Вы не заполнили одно из полей:
Текст вопроса - {quest if quest else "Не заполненно"}
Варианты ответа - {quest if quest else "Не заполнены"}
Правильный вариант ответа - {quest if quest else "Не заполнен"}""",  reply_markup=ikb_actions_qustion())
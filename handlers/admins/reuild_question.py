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
from keyboard.ikb_actions_question import ikb_actions_qustion, ikb_actions_rebuild_qustion

router = Router()




@router.callback_query(Current.rebuild_quest, F.data =="ikb_text_quest")
async def second(query: CallbackQuery, state: FSMContext):
    await query.message.answer("Введите текст вопроса", reply_markup=ikb_back())
    await state.set_state(Current.rebuild_question)


@router.callback_query(Current.rebuild_quest, F.data =="ikb_add_variant")
async def second(query: CallbackQuery, state: FSMContext):
    await query.message.answer("Введите вариант ответа", reply_markup=ikb_back())
    await state.set_state(Current.rebuild_variants)


@router.callback_query(Current.rebuild_quest, F.data =="ikb_correct_one")
async def second(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    id_quest = data.get("current_quest")
    current_quest = await questions.get_current(id_quest)
    variants = current_quest.variants
    if variants:
        lst_vars = list(map(str, variants.split(".*.")))
        response = "Варианты ответа: \n" + "\n".join(lst_vars)
        await query.message.answer(response)
    else:
        await query.message.answer("Вы пока не ввели правильный вариант ответа")

    await query.message.answer("Выберите ответ, который будет считаться правильным", reply_markup=ikb_back())
    await state.set_state(Current.rebuild_correct)


@router.message(Current.rebuild_question, Admin())
async def question(message: Message, state:FSMContext):
    text = message.text
    data = await state.get_data()
    id_quest = data.get("current_quest")
    current_test = await questions.get_current(id_quest)
    print("changing text")
    await questions.change_text(id_quest, text)
    variants = list(map(str, current_test.variants.split(".*.")))
    if current_test.type == 1:
        correct = current_test.correct_answer
    elif current_test.type == 2:
        correct = list(map(str, current_test.correct_answer.split(".*.")))
    else:
        correct = current_test.coorect_answer
    await message.answer(f"""Предпросмотр вопроса - 
Текст вопроса:
{text if text else "Пока не заполненно"}
------------------------------------------------------
Варианты ответа:
{variants if variants else "Пока не заполненно"} 
------------------------------------------------------
Правильный ответ:
{correct if correct else "Пока не заполненно"}""", reply_markup=ikb_actions_rebuild_qustion())
    await state.set_state(Current.rebuild_quest)


@router.message(Current.rebuild_variants, Admin())
async def question(message: Message, state:FSMContext):
    data = await state.get_data()

    id_quest = data.get("current_quest")
    current_test = await questions.get_current(id_quest)
    if current_test.type == 1:
        correct = current_test.correct_answer
    elif current_test.type == 2:
        correct = list(map(str, current_test.correct_answer.split(".*.")))
    else:
        correct = current_test.corect_answer

    text = message.text
    var_old = current_test.variants
    if var_old:
        vars = var_old + ".*." + text
        await questions.change_vars(id_quest=id_quest, new_vars=vars)
    else:
        await questions.change_vars(id_quest=id_quest, new_vars=text)

    current_test = await questions.get_current(id_quest)


    list_variants = list(map(str, current_test.variants.split(".*.")))
    text = current_test.text
    await message.answer(f"""Вы в конструкторе вопроса с единственным выбором правильного ответа
Предпросмотр вопроса - 
Текст вопроса:
{text if text else "Пока не заполненно"}
------------------------------------------------------
Варианты ответа:
{list_variants if list_variants else "Пока не заполненно"}
------------------------------------------------------
Правильный ответ:
{correct if correct else "Пока не заполненно"}""", reply_markup=ikb_actions_rebuild_qustion())
    await state.set_state(Current.rebuild_quest)


@router.message(Current.rebuild_correct, Admin())
async def question(message: Message, state:FSMContext):
    text = message.text
    data = await state.get_data()
    id_quest = data.get("current_quest")
    current_quest = await questions.get_current(id_quest)
    question = current_quest.text
    variants = current_quest.variants




    try:
        text = int(text)
        if variants:
            vars = list(map(str, variants.split(".*.")))
            if text > 0 and text <= len(vars):
                if current_quest.type == 1:
                    await questions.change_correct(id_quest, vars[text-1])
                    await message.answer(f"Успешно установлен вариант ответа {text}: {vars[text-1]}")
                    await message.answer(f"""Вы в конструкторе вопроса с единственным выбором правильного ответа

Предпросмотр вопроса -
Текст вопроса:
{question if question else "Пока не заполненно"}
------------------------------------------------------
Варианты ответа:
{vars if vars else "Пока не заполненно"}
------------------------------------------------------
Правильный ответ:
{vars[text - 1] if vars[text - 1] else "Пока не заполненно"}""", reply_markup=ikb_actions_rebuild_qustion())

                    # long long await query
                    await state.set_state(Current.rebuild_quest)
                elif current_quest.type == 2:
                    correct_old = current_quest.correct_answer
                    if correct_old:
                        corrects = correct_old + ".*." + vars[text - 1]
                        await questions.change_correct(id_quest, corrects)
                    else:
                        await questions.change_correct(id_quest, vars[text - 1])
                    await message.answer(f"Успешно установлен вариант ответа {text}: {vars[text - 1]}")
                    current_quest = await questions.get_current(id_quest)
                    corrects_new = current_quest.correct_answer
                    list_corrects = list(map(str, corrects_new.split(".*.")))
                    await message.answer(f"""Вы в конструкторе вопроса с множественным выбором правильного ответа
                
Предпросмотр вопроса -
Текст вопроса:
{question if question else "Пока не заполненно"}
------------------------------------------------------
Варианты ответа:
{vars if vars else "Пока не заполненно"}
------------------------------------------------------
Правильный ответ:
{list_corrects if list_corrects else "Пока не заполненно"}""", reply_markup=ikb_actions_rebuild_qustion())
                else:
                    pass
            else:
                await message.answer(f"Выберите вариант ответа от 1 до {len(variants)}", reply_markup=ikb_back()) #todo прописать бэк для Current.corect
        else:
            await message.answer("Ваианты еще не заполнены. Сперва заполните варианты ответа", ikb_actions_rebuild_qustion())
            await state.set_state(Current.rebuild_quest)
    except:
        await message.answer(f"Выберите вариант ответа от 1 до {len(variants)}", reply_markup=ikb_back())



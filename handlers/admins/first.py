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


@router.callback_query(Current.event, F.data =="ikb_1st_type")
async def second(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.update_data(type=1)
    text = data.get("text")
    variants = data.get("variants")
    correct = data.get("correct")
    if variants:
        list_vars = list(map(str, variants.split(".*.")))
        variants = "\n".join(f"{index}. {element}" for index, element in enumerate(list_vars, start=1))
        await query.message.answer(f"""🛠️Вы в конструкторе вопроса c <b>единственным правильным ответом</b>
Предпросмотр вопроса: 

<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants if variants else "❌Не заполненно"}

<b>Правильный ответ:</b>
{correct if correct else "❌Не заполненно"}""", reply_markup=ikb_actions_qustion(), parse_mode=ParseMode.HTML)  # p
    else:
        await query.message.answer(f"""🛠️Вы в конструкторе вопроса c <b>единственным правильным ответом</b>
Предпросмотр вопроса: 
    
<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}
    
<b>Варианты ответа:</b>
{variants if variants else "❌Не заполненно"}
    
<b>Правильный ответ:</b>
{correct if correct else "❌Не заполненно"}""", reply_markup=ikb_actions_qustion(), parse_mode=ParseMode.HTML)#parse_mode_был



@router.callback_query(Current.event, F.data =="ikb_text_quest")
async def second(query: CallbackQuery, state: FSMContext):
    await query.message.answer("❔Введите текст вопроса", reply_markup=ikb_back())
    await state.set_state(Current.question)

#------------------------------ Изменение вариантов ответа -----------------------------------
@router.callback_query(Current.event, F.data =="ikb_change_quest_variant")
async def second(query: CallbackQuery, state: FSMContext):
    await query.message.answer("🔠Выберите действие для вариантов ответа", reply_markup=ikb_change_variants_question())


@router.callback_query(Current.event, F.data == "ikb_add_new_variant")
async def second(query: CallbackQuery, state: FSMContext):
    await query.message.answer("🔠Введите новый вариант ответа") # todo бэк
    await state.set_state(Current.variants_new)


@router.callback_query(Current.event, F.data == "ikb_clear_all_vars")
async def second(query: CallbackQuery, state: FSMContext):
    await state.update_data(variants=None)
    await state.update_data(correct=None)
    data = await state.get_data()
    text = data.get("question")
    correct = data.get("correct")
    await query.message.answer(f"""✔️Варианты ответов успешно удалены""")
    await query.message.answer(f"""🛠️Вы в конструкторе вопроса c <b>единственным правильным ответом</b>
Предпросмотр вопроса: 

<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
❌Не заполненно

<b>Правильный ответ:</b>
{correct if correct else "❌Не заполненно"}""", reply_markup=ikb_actions_qustion(), parse_mode=ParseMode.HTML)


@router.callback_query(Current.event, F.data == "ikb_delete_one_var")
async def question(query: CallbackQuery, state:FSMContext):
    data = await state.get_data()
    variants = (data.get("variants"))
    if variants:
        list_variants = list(map(str, variants.split(".*.")))
        variants = "\n".join(f"{index}. {element}" for index, element in enumerate(list_variants, start=1))
        await query.message.answer(f"""🔠Текущие установленные варианты:
{variants}
🎯Введите вариант ответа, который хотите удалить от 1 до {len(list_variants)}""") # todo можно бэк
        await state.set_state(Current.variants_del)
    else:
        text = data.get("question")
        correct = data.get("correct")
        await query.message.answer(f"""⛔Варианты ответов еще не установлены""")
        await query.message.answer(f"""🛠️Вы в конструкторе вопроса c <b>единственным правильным ответом</b>
Предпросмотр вопроса: 

<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants if variants else "❌Не заполненно"}

<b>Правильный ответ:</b>
{correct if correct else "❌Не заполненно"}""", reply_markup=ikb_actions_qustion(), parse_mode=ParseMode.HTML)
        await state.set_state(Current.event)


@router.message(Current.variants_del, Admin())
async def question(message: Message, state:FSMContext):
    data = await state.get_data()
    num = message.text
    try:
        num = int(num)
        variants = data.get("variants")
        list_vars = list(map(str, variants.split(".*.")))
        deleted_var = list_vars.pop(num-1)
        new_vars = ".*.".join(list_vars)
        text = data.get('question')
        correct = data.get("correct")

        variants_str = "\n".join(f"{index}. {element}" for index, element in enumerate(list_vars, start=1))
        await state.update_data(variants=new_vars)

        await message.answer(f"""✅Варианты ответов были успешно обновлены. {deleted_var} Был успешно удален
Текущий список ответов:
{variants_str if len(list_vars) > 0 else "❌Не заполненно"}""")
        await message.answer(f"""🛠️Вы в конструкторе вопроса c <b>единственным правильным ответом</b>
Предпросмотр вопроса: 

<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants_str if variants else "❌Не заполненно"}

<b>Правильный ответ:</b>
{correct if correct else "❌Не заполненно"}""", reply_markup=ikb_actions_qustion(),
                             parse_mode=ParseMode.HTML)  # p
        await state.set_state(Current.event)

    except:
        await message.answer(f"""❌Вы ввели некорректный вариант ответа для удаления, 
Введите еще раз вариант ответа, который хотите удалить или вернитесь назад↩️""", reply_markup=ikb_back()) #todo БЭК


@router.message(Current.variants_new, Admin())
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
    text = data_new.get("question")
    correct = data_new.get("correct")
    if variants:
        list_variants = list(map(str, variants.split(".*.")))
        variants = "\n".join(f"{index}. {element}" for index, element in enumerate(list_variants, start=1))

    await message.answer(f"""🛠️Вы в конструкторе вопроса c <b>единственным правильным ответом</b>
Предпросмотр вопроса: 

<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants if variants else "❌Не заполненно"}

<b>Правильный ответ:</b>
{correct if correct else "❌Не заполненно"}""", reply_markup=ikb_actions_qustion(), parse_mode=ParseMode.HTML)  # p
    await state.set_state(Current.event)

#------------------------------------------------------------------------------------------------------------------


@router.callback_query(Current.event, F.data =="ikb_correct_one")
async def second(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    variants = data.get("variants")
    if variants:
        lst_vars = list(map(str, variants.split(".*.")))
        vars = "\n".join(f"{index}. {element}" for index, element in enumerate(lst_vars, start=1))
        response = f"🎯Варианты ответа: {vars}"
        await query.message.answer(response)
    else:
        await query.message.answer("❌Вы пока не ввели правильный вариант ответа")
    await query.message.answer("🎯Выберите ответ, который будет считаться правильным", reply_markup=ikb_back())
    await state.set_state(Current.correct)


@router.message(Current.question, Admin())
async def question(message: Message, state:FSMContext):
    text = message.text
    await state.update_data(question=text)
    data = await state.get_data()
    text = data.get("question")
    variants = data.get("variants")
    correct = data.get("correct")
    if variants:
        list_vars = list(map(str, variants.split(".*.")))
        variants = "\n".join(f"{index}. {element}" for index, element in enumerate(list_vars, start=1))
        await message.answer(f"""🛠️Вы в конструкторе вопроса c <b>единственным правильным ответом</b>
Предпросмотр вопроса: 

<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants if variants else "❌Не заполненно"}

<b>Правильный ответ:</b>
{correct if correct else "❌Не заполненно"}""", reply_markup=ikb_actions_qustion(), parse_mode=ParseMode.HTML)  # p
    else:
        await message.answer(f"""🛠️Вы в конструкторе вопроса c <b>единственным правильным ответом</b>
Предпросмотр вопроса: 

<b>Текст вопроса:</b>
    {text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants if variants else "❌Не заполненно"}

<b>Правильный ответ:</b>
{correct if correct else "❌Не заполненно"}""", reply_markup=ikb_actions_qustion(), parse_mode=ParseMode.HTML)  # parse_mode_был
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
                variants = "\n".join(f"{index}. {element}" for index, element in enumerate(vars, start=1))

                await message.answer(f"✅Успешно установлен вариант ответа <b>{text}: {vars[text-1]}</b>", parse_mode=ParseMode.HTML)
                await message.answer(f"""️🛠️Вы в конструкторе вопроса c <b>единственным правильным ответом</b>
Предпросмотр вопроса: 

<b>Текст вопроса:</b>
{qest if qest else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants if variants else "❌Не заполненно"}

<b>Правильный ответ:</b>
{vars[text-1] if vars[text-1] else "❌Не заполненно"}""", reply_markup=ikb_actions_qustion(), parse_mode=ParseMode.HTML)#parse_mode_был
                await state.set_state(Current.event)
            else:
                await message.answer(f"☑️Выберите вариант ответа <b>от 1 до {len(vars)}</b>", reply_markup=ikb_back(), parse_mode=ParseMode.HTML) #todo прописать бэк для Current.corect
        else:
            await message.answer("❌Варианты еще не заполнены. Сперва заполните варианты ответа", ikb_actions_qustion())
            await state.set_state(Current.event)
    except:
        await message.answer(f"☑️Выберите вариант ответа <b>от 1 до {len(vars)}</b>", reply_markup=ikb_back(), parse_mode=ParseMode.HTML)

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

    if quest and vars and correct:
        try:
            await questions.add_test(id_test=test_id, id_quest=len(all_quests)+1, correct_answer=correct, quest_type=types, variants=vars, text=quest)
            await query.message.answer("✅Вопрос успешно добавлен")
            kb = await ikb_all_questions(test_id)
            await query.message.answer("⚡Выберите действие для вопросов", reply_markup=kb)
            await state.update_data(question='')
            await state.update_data(variants='')
            await state.update_data(correct='')
            await state.update_data(type='')
            await state.set_state(Current.current_test)
        except Exception as err:
            await log_exceptions1("create_quest_1", "ERROR", "first.py", 230, err, query.from_user.id)

            await query.message.answer("❌Произошла ошибка")
            kb = await ikb_all_questions(test_id)
            await query.message.answer("⚡Выберите действие для вопросов⚡", reply_markup=kb)
    else:
        await query.message.answer(f"""⛔Вы не заполнили одно из полей:
Текст вопроса - {quest if quest else "❌Не заполненно"}
Варианты ответа - {vars if vars else "❌Не заполнены"}
Правильный вариант ответа - {correct if correct else "❌Не заполнено"}""",  reply_markup=ikb_actions_qustion())
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram import types
from aiogram.filters import Command
from filters.is_admin import Admin
from keyboard.ikb_change_variants_question import ikb_change_variants_question
from keyboard.list_questions import ikb_all_questions
from set_logs1.logger_all1 import log_exceptions1
from utils.db_api.quck_commands import event, tests, questions
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from states.fsm import Creation, Current, Current2

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


@router.callback_query(Current.event, F.data =="ikb_2nd_type")
async def second(query: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await state.update_data(type=2)
        text = data.get("text")
        variants = data.get("variants")
        correct = data.get("correct")
        if variants:
            list_variants = list(map(str, variants.split(".*.")))
            variants = "\n".join(f"{index}) {element}" for index, element in enumerate(list_variants, start=1))
        if correct:
            list_corrects = list(map(str, correct.split(".*.")))
            correct = "\n".join(f"{index}) {element}" for index, element in enumerate(list_corrects, start=1))
        await query.message.answer(f"""🛠️Вы в конструкторе вопроса c <b>множественным правильным ответом</b>
Предпросмотр вопроса: 

<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants if variants else "❌Не заполненно"}

<b>Правильные ответы:</b>
{correct if correct else "❌Не заполненно"}""", reply_markup=ikb_actions_qustion(),parse_mode=ParseMode.HTML)
        await state.set_state(Current2.event)
    except Exception as err:
        await log_exceptions1("create_2nd_type_quest", "ERROR", "second.py", 57, err, query.from_user.id)


@router.callback_query(Current2.event, F.data =="ikb_text_quest")
async def second(query: CallbackQuery, state: FSMContext):
    await query.message.answer("❔Введите текст вопроса", reply_markup=ikb_back())
    await state.set_state(Current2.question)

#-------------------------------------Изменение вариантов ответа -------------------------------------------

@router.callback_query(Current2.event, F.data =="ikb_change_quest_variant")
async def second(query: CallbackQuery, state: FSMContext):
    await query.message.answer("🔠Выберите действие для вариантов ответа", reply_markup=ikb_change_variants_question())


@router.callback_query(Current2.event, F.data == "ikb_add_new_variant")
async def second(query: CallbackQuery, state: FSMContext):
    await query.message.answer("🔠Введите новый вариант ответа") # todo бэк
    await state.set_state(Current2.variants_new)


@router.callback_query(Current2.event, F.data == "ikb_clear_all_vars")
async def second(query: CallbackQuery, state: FSMContext):
    await state.update_data(variants=None)
    await state.update_data(correct=None)

    data = await state.get_data()
    text = data.get("question")
    await query.message.answer(f"""✔️Варианты ответов успешно удалены""")
    await query.message.answer(f"""🛠️Вы в конструкторе вопроса c <b>множественным правильным ответом</b>
Предпросмотр вопроса: 

<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
❌Не заполненно

<b>Правильный ответ:</b>
❌Не заполненно""", reply_markup=ikb_actions_qustion(), parse_mode=ParseMode.HTML)


@router.callback_query(Current2.event, F.data == "ikb_delete_one_var")
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
        if correct:
            list_corrects = list(map(str, correct.split(".*.")))
            correct = "\n".join(f"{index}. {element}" for index, element in enumerate(list_corrects, start=1))
        await query.message.answer(f"""⛔Варианты ответов еще не установлены""")
        await query.message.answer(f"""🛠️Вы в конструкторе вопроса c <b>множественным правильным ответом</b>
Предпросмотр вопроса: 

<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants if variants else "❌Не заполненно"}

<b>Правильный ответ:</b>
{correct if correct else "❌Не заполненно"}""", reply_markup=ikb_actions_qustion(), parse_mode=ParseMode.HTML)
        await state.set_state(Current2.event)


@router.message(Current2.variants_del, Admin())
async def question(message: Message, state:FSMContext):
    data = await state.get_data()
    num = message.text
    try:
        num = int(num) -1
        variants = data.get("variants")
        list_vars = list(map(str, variants.split(".*.")))
        deleted_var = list_vars.pop(num)
        new_vars = ".*.".join(list_vars)
        text = data.get('question')
        correct = data.get("correct")
        variants_str = "\n".join(f"{index}. {element}" for index, element in enumerate(list_vars, start=1))
        await state.update_data(variants=new_vars)
        list_corrects = None
        if correct:
            print(list_corrects)
            list_corrects = list(map(str, correct.split(".*.")))
            if deleted_var in list_corrects:
                i = list_corrects.index(deleted_var)
                list_corrects.pop(i)
            print(list_corrects)
            new_corrects = ".*.".join(list_corrects)
            await state.update_data(correct=new_corrects)
            correct = "\n".join(f"{index}. {element}" for index, element in enumerate(list_corrects, start=1))
        await message.answer(f"""✅Варианты ответов были успешно обновлены. <b>{deleted_var} </b>Был успешно удален
Текущий список ответов:
{variants_str if len(list_vars) > 0 else "❌Не заполненно"}""")
        await message.answer(f"""🛠️Вы в конструкторе вопроса c <b>множественным правильным ответом</b>
Предпросмотр вопроса: 

<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants_str if len(list_vars)>0 else "❌Не заполненно"}

<b>Правильный ответ:</b>
{correct if len(list_corrects) else "❌Не заполненно"}""", reply_markup=ikb_actions_qustion(),
                             parse_mode=ParseMode.HTML)  # p
        await state.set_state(Current2.event)

    except:
        await message.answer(f"""❌Вы ввели некорректный вариант ответа для удаления, 
Введите еще раз вариант ответа, который хотите удалить или вернитесь назад↩️""", reply_markup=ikb_back()) #todo БЭК


@router.message(Current2.variants_new, Admin())
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
    if correct:
        list_corrects = list(map(str, correct.split(".*.")))
        correct = "\n".join(f"{index}. {element}" for index, element in enumerate(list_corrects, start=1))
    await message.answer(f"""🛠️Вы в конструкторе вопроса c <b>множественным правильным ответом</b>
Предпросмотр вопроса: 

<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants if variants else "❌Не заполненно"}

<b>Правильный ответ:</b>
{correct if correct else "❌Не заполненно"}""", reply_markup=ikb_actions_qustion(), parse_mode=ParseMode.HTML)  # p
    await state.set_state(Current2.event)

#----------------------------------------------------------------------------------------------------------
@router.callback_query(Current2.event, F.data =="ikb_correct_one")
async def second(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    variants = data.get("variants")

    if variants:
        lst_vars = list(map(str, variants.split(".*.")))
        vars = "\n".join(f"{index}. {element}" for index, element in enumerate(lst_vars, start=1))
        await query.message.answer("🎯Выберите ответ, который будет считаться правильным", reply_markup=ikb_back())
        response = f"🎯Варианты ответа: \n{vars}"
        await query.message.answer(response)
    else:
        await query.message.answer("❌Вы пока не ввели правильный вариант ответа", reply_markup=ikb_back())
    await state.set_state(Current2.correct)


@router.message(Current2.question, Admin())
async def question(message: Message, state:FSMContext):
    try:
        text = message.text
        await state.update_data(question=text)
        data = await state.get_data()
        text = data.get("question")
        variants = data.get("variants")
        correct = data.get("correct")

        if variants:
            list_vars = list(map(str, variants.split(".*.")))
            variants = "\n".join(f"{index}. {element}" for index, element in enumerate(list_vars, start=1))
        if correct:
            list_corrects = list(map(str, correct.split(".*.")))
            correct = "\n".join(f"{index}. {element}" for index, element in enumerate(list_corrects, start=1))
        await message.answer(f"""🛠️Вы в конструкторе вопроса с <b>множественным выбором правильного ответа</b>
    
Предпросмотр вопроса - 
<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}
    
<b>Варианты ответа:</b>
{variants if variants else "❌Не заполненно"}
    
<b>Правильные ответы:</b>
{correct if correct else "❌Не заполненно"}""", reply_markup=ikb_actions_qustion(), parse_mode=ParseMode.HTML)
        await state.set_state(Current2.event)
    except Exception as err:
        await log_exceptions1("question", "ERROR", "second.py", 117, err, message.from_user.id)


@router.message(Current2.variants, Admin())
async def question(message: Message, state:FSMContext):
    try:
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
        variants = "\n".join(f"{index}. {element}" for index, element in enumerate(list_variants, start=1))
        text = data_new.get("question")
        correct = data_new.get("correct")
        if correct:
            list_corrects = list(map(str, correct.split(".*.")))
            correct = "\n".join(f"{index}. {element}" for index, element in enumerate(list_corrects, start=1))
        await message.answer(f"""🛠️Вы в конструкторе вопроса с <b>множественным выбором правильного ответа</b>
    
Предпросмотр вопроса - 
<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}
    
<b>Варианты ответа:</b>
{variants if list_variants else "❌Не заполненно"}
    
<b>Правильные ответы:</b>
{correct if list_corrects else "❌Не заполненно"}""", reply_markup=ikb_actions_qustion(), parse_mode=ParseMode.HTML)
        await state.set_state(Current2.event)
    except Exception as err:
        await message.answer(f"❌Возникла ошибка")
        await log_exceptions1("question", "ERROR", "second.py", 150, err, message.from_user.id)


@router.message(Current2.correct, Admin())
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
                correct_old = (data.get("correct"))
                if correct_old:
                    corrects = correct_old + ".*." + vars[text-1]
                    await state.update_data(correct=corrects)
                else:
                    await state.update_data(correct=vars[text-1])
                await message.answer(f"✅Успешно установлен вариант ответа <b>{text}: {vars[text-1]}</b>", parse_mode=ParseMode.HTML)
                data_new = await state.get_data()
                correct = data_new.get("correct")
                list_corrects = list(map(str, correct.split(".*.")))
                list_corrects = "\n".join(f"{index}. {element}" for index, element in enumerate(list_corrects, start=1))
                variants_str = "\n".join(f"{index}. {element}" for index, element in enumerate(vars, start=1))
                await message.answer(f"""🛠️Вы в конструкторе вопроса с <b>множественным выбором правильного ответа</b>

Предпросмотр вопроса - 
<b>Текст вопроса:</b>
{qest if qest else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants_str if variants_str else "❌Не заполненно"}

<b>Правильный ответ:</b>
{list_corrects if list_corrects else "❌Не заполненно"}""", reply_markup=ikb_actions_qustion(), parse_mode=ParseMode.HTML)
                await state.set_state(Current2.event)
            else:
                await message.answer(f"☑️Выберите вариант ответа от 1 до {len(vars)}", reply_markup=ikb_back()) #todo прописать бэк для Current.corect

        else:
            await message.answer("❌Ваианты еще не заполнены. Сперва заполните варианты ответа", ikb_actions_qustion())
            await state.set_state(Current2.event)
    except Exception as err:
        print(err)
        await message.answer(f"☑️Выберите вариант ответа от 1 до {len(vars)}", reply_markup=ikb_back())


@router.callback_query(Current2.event, F.data =="ikb_add_question_test")
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
            await query.message.answer("⚡Выберите действие для вопросов⚡", reply_markup=kb)
            await state.update_data(question='')
            await state.update_data(variants='')
            await state.update_data(correct='')
            await state.update_data(type='')
            await state.set_state(Current.current_test)
        except Exception as err:
            await log_exceptions1("add_question_to_db", "ERROR", "second.py", 222, err, query.from_user.id)
            await query.message.answer("❌Произошла ошибка")
            kb = await ikb_all_questions(test_id)
            await query.message.answer("⚡Выберите действие для вопросов⚡", reply_markup=kb)
    else:
        variants_str = None
        corrects_str = None
        if vars:
            vars = list(map(str, vars.split(".*.")))
            variants_str = "\n".join(f"{index}. {element}" for index, element in enumerate(vars, start=1))
        if correct:
            correct = list(map(str, correct.split(".*.")))
            corrects_str = "\n".join(f"{index}. {element}" for index, element in enumerate(correct, start=1))


        await query.message.answer(f"""⛔Вы не заполнили одно из полей:
Текст вопроса - {quest if quest else "❌Не заполненно"}

Варианты ответа - {variants_str if vars else "❌Не заполненно"}

Правильный вариант ответа - {corrects_str if correct else "❌Не заполненно"}""", reply_markup=ikb_actions_qustion())

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
from utils.db_api.quck_commands import event, tests, questions, quiz
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from states.fsm import Creation, Current, Current2

from keyboard.inline_main_menu import ikb_main_menu
from keyboard.ikb_back import ikb_back, ikb_back_quiz
from keyboard.save_event import ikb_save
from keyboard.ikb_all_events import ikb_all_events
from keyboard.ikb_all_events import ikb_all_events, Choose_event
from keyboard.ikb_current_test import ikb_current_test
from keyboard.ikb_settings_test import ikb_settings_test
from keyboard.ikb_timer import ikb_timer
from keyboard.ikb_adding_questions import ikb_adding_questions
from keyboard.ikb_types_questions import ikb_types_of_questions
from keyboard.ikb_actions_question import ikb_actions_qustion, ikb_question_quiz_menu
from keyboard.ikb_change_variants_question import ikb_change_variants_question, ikb_change_variants_question_quiz

router = Router()


@router.callback_query(Current.event, F.data == "ikb_1st_type_quiz")
async def second(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.update_data(type=3)
    text = data.get("question_quiz")
    variants = data.get("variants_quiz")
    if variants:
        list_vars = list(map(str, variants.split(".*.")))
        variants = "\n".join(f"{index}. {element}" for index, element in enumerate(list_vars, start=1))
        await query.message.answer(f"""🛠️Вы в конструкторе вопроса c <b>единственным правильным ответом</b>
Предпросмотр вопроса: 

<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants if variants else "❌Не заполненно"}""", reply_markup=ikb_question_quiz_menu(), parse_mode=ParseMode.HTML)  # p
    else:
        await query.message.answer(f"""🛠️Вы в конструкторе вопроса c <b>единственным правильным ответом</b>
Предпросмотр вопроса: 

<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants if variants else "❌Не заполненно"}""", reply_markup=ikb_question_quiz_menu(), parse_mode=ParseMode.HTML)  # parse_mode_был


@router.callback_query(Current.event, F.data == "ikb_text_quest_quiz")
async def second(query: CallbackQuery, state: FSMContext):
    await query.message.answer("❔Введите текст вопроса", reply_markup=ikb_back_quiz())
    await state.set_state(Current.question_quiz)


# ------------------------------ Изменение вариантов ответа -----------------------------------
@router.callback_query(Current.event, F.data == "ikb_change_quest_variant_quiz")
async def second(query: CallbackQuery, state: FSMContext):
    await query.message.answer("🔠Выберите действие для вариантов ответа", reply_markup=ikb_change_variants_question_quiz())


@router.callback_query(Current.event, F.data == "ikb_add_new_variant_quiz")
async def second(query: CallbackQuery, state: FSMContext):
    await query.message.answer("🔠Введите новый вариант ответа")  # todo бэк
    await state.set_state(Current.variants_new_quiz)


@router.callback_query(Current.event, F.data == "ikb_clear_all_vars_quiz")
async def second(query: CallbackQuery, state: FSMContext):
    await state.update_data(variants_quiz=None)
    data = await state.get_data()
    text = data.get("question_quiz")
    await query.message.answer(f"""✔️Варианты ответов успешно удалены""")
    await query.message.answer(f"""🛠️Вы в конструкторе вопроса c <b>единственным правильным ответом</b>
Предпросмотр вопроса: 

<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
❌Не заполненно""", reply_markup=ikb_question_quiz_menu(), parse_mode=ParseMode.HTML)


@router.callback_query(Current.event, F.data == "ikb_delete_one_var_quiz")
async def question(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    variants = (data.get("variants_quiz"))
    if variants:
        list_variants = list(map(str, variants.split(".*.")))
        variants = "\n".join(f"{index}. {element}" for index, element in enumerate(list_variants, start=1))
        await query.message.answer(f"""🔠Текущие установленные варианты:
{variants}
🎯Введите вариант ответа, который хотите удалить от 1 до {len(list_variants)}""")  # todo можно бэк
        await state.set_state(Current.variants_del_quiz)
    else:
        text = data.get("question_quiz")
        await query.message.answer(f"""⛔Варианты ответов еще не установлены""")
        await query.message.answer(f"""🛠️Вы в конструкторе вопроса c <b>единственным правильным ответом</b>
Предпросмотр вопроса: 

<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants if variants else "❌Не заполненно"}""", reply_markup=ikb_question_quiz_menu(), parse_mode=ParseMode.HTML)
        await state.set_state(Current.event)


@router.message(Current.variants_del_quiz, Admin())
async def question(message: Message, state: FSMContext):
    data = await state.get_data()
    num = message.text
    try:
        num = int(num)
        variants = data.get("variants_quiz")
        list_vars = list(map(str, variants.split(".*.")))
        deleted_var = list_vars.pop(num - 1)
        new_vars = ".*.".join(list_vars)
        text = data.get('question_quiz')
        variants_str = "\n".join(f"{index}. {element}" for index, element in enumerate(list_vars, start=1))
        await state.update_data(variants_quiz=new_vars)
        await message.answer(f"""✅Варианты ответов были успешно обновлены. {deleted_var} Был успешно удален
Текущий список ответов:
{variants_str if len(list_vars) > 0 else "❌Не заполненно"}""")
        await message.answer(f"""🛠️Вы в конструкторе вопроса c <b>единственным правильным ответом</b>
Предпросмотр вопроса: 

<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants_str if list_vars else "❌Не заполненно"}""", reply_markup=ikb_question_quiz_menu(), parse_mode=ParseMode.HTML)
        await state.set_state(Current.event)

    except:
        await message.answer(f"""❌Вы ввели некорректный вариант ответа для удаления, 
Введите еще раз вариант ответа, который хотите удалить или вернитесь назад↩️""", reply_markup=ikb_back())  # todo БЭК


@router.message(Current.variants_new_quiz, Admin())
async def question(message: Message, state: FSMContext):
    data = await state.get_data()

    text = message.text
    var_old = (data.get("variants_quiz"))
    if var_old:
        vars = var_old + ".*." + text
        await state.update_data(variants_quiz=vars)
    else:
        await state.update_data(variants_quiz=text)
    data_new = await state.get_data()
    variants = data_new.get("variants_quiz")
    text = data_new.get("question_quiz")
    if variants:
        list_variants = list(map(str, variants.split(".*.")))
        variants = "\n".join(f"{index}. {element}" for index, element in enumerate(list_variants, start=1))

    await message.answer(f"""🛠️Вы в конструкторе вопроса c <b>единственным правильным ответом</b>
Предпросмотр вопроса: 

<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants if variants else "❌Не заполненно"}""", reply_markup=ikb_question_quiz_menu(), parse_mode=ParseMode.HTML)  # p
    await state.set_state(Current.event)


# ------------------------------------------------------------------------------------------------------------------


@router.message(Current.question_quiz, Admin())
async def question(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(question_quiz=text)
    data = await state.get_data()
    text = data.get("question_quiz")
    variants = data.get("variants_quiz")
    if variants:
        list_vars = list(map(str, variants.split(".*.")))
        variants = "\n".join(f"{index}. {element}" for index, element in enumerate(list_vars, start=1))
        await message.answer(f"""🛠️Вы в конструкторе вопроса c <b>единственным правильным ответом</b>
Предпросмотр вопроса: 

<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants if variants else "❌Не заполненно"}""", reply_markup=ikb_question_quiz_menu(), parse_mode=ParseMode.HTML)  # p
    else:
        await message.answer(f"""🛠️Вы в конструкторе вопроса c <b>единственным правильным ответом</b>
Предпросмотр вопроса: 

<b>Текст вопроса:</b>
    {text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants if variants else "❌Не заполненно"}""", reply_markup=ikb_question_quiz_menu(),
                             parse_mode=ParseMode.HTML)  # parse_mode_был
    await state.set_state(Current.event)


def get_uniq_key(quests):
    keys = list()
    for q in quests:
        keys.append(q.id_quest)
    for i in range(100000):
        if i not in keys:
            return i
    return 100000 + 1


@router.callback_query(Current.event, F.data == "ikb_add_question_test_quiz")
async def second(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    quest = data.get("question_quiz")
    vars = data.get("variants_quiz")
    test_id = data.get("current_test_quiz")
    types = data.get("type")
    print("INFO TYPE - ", types, type(types))
    print("INFO", type(vars), type(quest))
    all_quests = await questions.get_all_quest()
    id_key = get_uniq_key(all_quests)
    if quest and vars:
        try:
            await questions.add_test(id_test=test_id, id_quest=id_key, quest_type=types,
                                     variants=vars, text=quest, correct_answer=None)
            await query.message.answer("✅Вопрос успешно добавлен")
            kb = await ikb_all_questions(test_id)
            await query.message.answer("⚡Выберите действие для вопросов", reply_markup=kb)
            await state.update_data(question_quiz='')
            await state.update_data(variants_quiz='')
            await state.update_data(type='')
            await state.set_state(Current.current_test)
        except Exception as err:
            await log_exceptions1("create_quiz_quest_1", "ERROR", "quiz_questions.py", 240, err, query.from_user.id)

            await query.message.answer("❌Произошла ошибка")
            kb = await ikb_all_questions(test_id)
            await query.message.answer("⚡Выберите действие для вопросов⚡", reply_markup=kb)
    else:
        await query.message.answer(f"""⛔Вы не заполнили одно из полей:
Текст вопроса - {quest if quest else "❌Не заполненно"}
Варианты ответа - {vars if vars else "❌Не заполнены"}""", reply_markup=ikb_actions_qustion())


#------------------------------------- 2 ТИП ВОПРОСОВ -----------------------------------------------------


@router.callback_query(Current.event, F.data == "ikb_2nd_type_quiz")
async def second(query: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        await state.update_data(type=4)
        text = data.get("text_quiz")
        variants = data.get("variants_quiz")
        if variants:
            list_variants = list(map(str, variants.split(".*.")))
            variants = "\n".join(f"{index}) {element}" for index, element in enumerate(list_variants, start=1))
        await query.message.answer(f"""🛠️Вы в конструкторе вопроса c <b>множественным правильным ответом</b>
Предпросмотр вопроса: 

<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants if variants else "❌Не заполненно"}""", reply_markup=ikb_question_quiz_menu(), parse_mode=ParseMode.HTML)
        await state.set_state(Current2.event)
    except Exception as err:
        await log_exceptions1("quiz_questions_second", "ERROR", "quiz_questions.py.py", 280, err, query.from_user.id)


@router.callback_query(Current2.event, F.data == "ikb_text_quest_quiz")
async def second(query: CallbackQuery, state: FSMContext):
    await query.message.answer("❔Введите текст вопроса", reply_markup=ikb_back())
    await state.set_state(Current2.question_quiz)


# -------------------------------------Изменение вариантов ответа -------------------------------------------

@router.callback_query(Current2.event, F.data == "ikb_change_quest_variant_quiz")
async def second(query: CallbackQuery, state: FSMContext):
    await query.message.answer("🔠Выберите действие для вариантов ответа", reply_markup=ikb_change_variants_question_quiz())


@router.callback_query(Current2.event, F.data == "ikb_add_new_variant_quiz")
async def second(query: CallbackQuery, state: FSMContext):
    await query.message.answer("🔠Введите новый вариант ответа")  # todo бэк
    await state.set_state(Current2.variants_new_quiz)


@router.callback_query(Current2.event, F.data == "ikb_clear_all_vars_quiz")
async def second(query: CallbackQuery, state: FSMContext):
    await state.update_data(variants_quiz=None)
    await state.update_data(correct_quiz=None)

    data = await state.get_data()
    text = data.get("question")
    await query.message.answer(f"""✔️Варианты ответов успешно удалены""")
    await query.message.answer(f"""🛠️Вы в конструкторе вопроса c <b>множественным правильным ответом</b>
Предпросмотр вопроса: 

<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
❌Не заполненно""", reply_markup=ikb_question_quiz_menu(), parse_mode=ParseMode.HTML)


@router.callback_query(Current2.event, F.data == "ikb_delete_one_var_quiz")
async def question(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    variants = (data.get("variants_quiz"))
    if variants:
        list_variants = list(map(str, variants.split(".*.")))
        variants = "\n".join(f"{index}. {element}" for index, element in enumerate(list_variants, start=1))
        await query.message.answer(f"""🔠Текущие установленные варианты:
{variants}
🎯Введите вариант ответа, который хотите удалить от 1 до {len(list_variants)}""")  # todo можно бэк
        await state.set_state(Current.variants_del_quiz)
    else:
        text = data.get("question_quiz")
        await query.message.answer(f"""⛔Варианты ответов еще не установлены""")
        await query.message.answer(f"""🛠️Вы в конструкторе вопроса c <b>множественным правильным ответом</b>
Предпросмотр вопроса: 

<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants if variants else "❌Не заполненно"}""", reply_markup=ikb_question_quiz_menu(), parse_mode=ParseMode.HTML)
        await state.set_state(Current2.event)


@router.message(Current2.variants_del_quiz, Admin())
async def question(message: Message, state: FSMContext):
    data = await state.get_data()
    num = message.text
    try:
        num = int(num) - 1
        variants = data.get("variants_quiz")
        list_vars = list(map(str, variants.split(".*.")))
        deleted_var = list_vars.pop(num)
        new_vars = ".*.".join(list_vars)
        text = data.get('question_quiz')
        variants_str = "\n".join(f"{index}. {element}" for index, element in enumerate(list_vars, start=1))
        await state.update_data(variants_quiz=new_vars)
        await message.answer(f"""✅Варианты ответов были успешно обновлены. <b>{deleted_var} </b>Был успешно удален
Текущий список ответов:
{variants_str if len(list_vars) > 0 else "❌Не заполненно"}""")
        await message.answer(f"""🛠️Вы в конструкторе вопроса c <b>множественным правильным ответом</b>
Предпросмотр вопроса: 

<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants_str if len(list_vars) > 0 else "❌Не заполненно"}""", reply_markup=ikb_question_quiz_menu(), parse_mode=ParseMode.HTML)  # p
        await state.set_state(Current2.event)

    except:
        await message.answer(f"""❌Вы ввели некорректный вариант ответа для удаления, 
Введите еще раз вариант ответа, который хотите удалить или вернитесь назад↩️""", reply_markup=ikb_back())  # todo БЭК


@router.message(Current2.variants_new_quiz, Admin())
async def question(message: Message, state: FSMContext):
    data = await state.get_data()

    text = message.text
    var_old = (data.get("variants_quiz"))
    if var_old:
        vars = var_old + ".*." + text
        await state.update_data(variants_quiz=vars)
    else:
        await state.update_data(variants_quiz=text)
    data_new = await state.get_data()
    variants = data_new.get("variants_quiz")
    text = data_new.get("question_quiz")
    if variants:
        list_variants = list(map(str, variants.split(".*.")))
        variants = "\n".join(f"{index}. {element}" for index, element in enumerate(list_variants, start=1))
    await message.answer(f"""🛠️Вы в конструкторе вопроса c <b>множественным правильным ответом</b>
Предпросмотр вопроса: 

<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants if variants else "❌Не заполненно"}""", reply_markup=ikb_question_quiz_menu(), parse_mode=ParseMode.HTML)  # p
    await state.set_state(Current2.event)


# ----------------------------------------------------------------------------------------------------------


@router.message(Current2.question, Admin())
async def question(message: Message, state: FSMContext):
    try:
        text = message.text
        await state.update_data(question_quiz=text)
        data = await state.get_data()
        text = data.get("question_quiz")
        variants = data.get("variants_quiz")

        if variants:
            list_vars = list(map(str, variants.split(".*.")))
            variants = "\n".join(f"{index}. {element}" for index, element in enumerate(list_vars, start=1))
        await message.answer(f"""🛠️Вы в конструкторе вопроса с <b>множественным выбором правильного ответа</b>

Предпросмотр вопроса - 
<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants if variants else "❌Не заполненно"}""", reply_markup=ikb_question_quiz_menu(), parse_mode=ParseMode.HTML)
        await state.set_state(Current2.event)
    except Exception as err:
        await log_exceptions1("question_quiz_second", "ERROR", "quiz_questions.py.py", 429, err, message.from_user.id)


@router.message(Current2.variants_quiz, Admin())
async def question(message: Message, state: FSMContext):
    try:
        data = await state.get_data()

        text = message.text
        var_old = (data.get("variants_quiz"))
        if var_old:
            vars = var_old + ".*." + text
            await state.update_data(variants_quiz=vars)
        else:
            await state.update_data(variants_quiz=text)
        data_new = await state.get_data()
        variants = data_new.get("variants_quiz")
        list_variants = list(map(str, variants.split(".*.")))
        variants = "\n".join(f"{index}. {element}" for index, element in enumerate(list_variants, start=1))
        text = data_new.get("question_quiz")
        await message.answer(f"""🛠️Вы в конструкторе вопроса с <b>множественным выбором правильного ответа</b>

Предпросмотр вопроса - 
<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants if list_variants else "❌Не заполненно"}""", reply_markup=ikb_question_quiz_menu(), parse_mode=ParseMode.HTML)
        await state.set_state(Current2.event)
    except Exception as err:
        await message.answer(f"❌Возникла ошибка")
        await log_exceptions1("variants_second_quiz", "ERROR", "quiz_questions.py", 460, err, message.from_user.id)


def get_uniq_key(quests):
    keys = list()
    for q in quests:
        keys.append(q.id_quest)
    for i in range(100000):
        if i not in keys:
            return i
    return 100000 + 1


@router.callback_query(Current2.event, F.data == "ikb_add_question_test_quiz") #todo Проверить корректность
async def second(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    quest = data.get("question_quiz")
    vars = data.get("variants_quiz")
    test_id = data.get("current_test_quiz")
    types = data.get("type_quiz")
    all_quests = await questions.get_all_quest()
    id_key = get_uniq_key(all_quests)
    if quest and vars:
        try:
            await questions.add_test(id_test=test_id, id_quest=id_key, correct_answer=None, quest_type=types,
                                     variants=vars, text=quest)
            await query.message.answer("✅Вопрос успешно добавлен")
            kb = await ikb_all_questions(test_id)
            await query.message.answer("⚡Выберите действие для вопросов⚡", reply_markup=kb)
            await state.update_data(question_quiz='')
            await state.update_data(variants_quiz='')
            await state.update_data(correct_quiz=None)
            await state.update_data(type_quiz='')
            await state.set_state(Current.current_test)
        except Exception as err:
            await log_exceptions1("add_to_db_question_quiz", "ERROR", "quiz_questions.py", 495, err, query.from_user.id)
            await query.message.answer("❌Произошла ошибка")
            kb = await ikb_all_questions(test_id)
            await query.message.answer("⚡Выберите действие для вопросов⚡", reply_markup=kb)
    else:
        variants_str = None
        if vars:
            vars = list(map(str, vars.split(".*.")))
            variants_str = "\n".join(f"{index}. {element}" for index, element in enumerate(vars, start=1))
        await query.message.answer(f"""⛔Вы не заполнили одно из полей:
Текст вопроса - {quest if quest else "❌Не заполненно"}

Варианты ответа - {variants_str if vars else "❌Не заполненно"}""", reply_markup=ikb_question_quiz_menu())

from aiogram.enums import ParseMode
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



@router.callback_query(F.data == "ikb_back", Current.event)
async def second(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("👋Приветствую, дорогой админ, выберите действие", reply_markup=ikb_main_menu())


@router.callback_query(F.data == "ikb_back_list_events", Current.event)
async def second(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    ikb = await ikb_all_events(callback.from_user.id)
    await callback.message.answer('📅Список доступных мероприятий', reply_markup=ikb)



@router.callback_query(F.data == "ikb_back_choose_type", Current.event)
async def second(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("""✏️Выберите тип вопроса:
1️⃣1 тип \- вопрос с единственным правильным ответом
🔢2 тип \- вопрос с множественным выбором""", reply_markup=ikb_types_of_questions(),parse_mode=ParseMode.MARKDOWN_V2)


@router.callback_query(F.data == "ikb_back_choose_type", Current2.event)
async def second(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("""✏️Выберите тип вопроса:
1️⃣1 тип \- вопрос с единственным правильным ответом
🔢2 тип \- вопрос с множественным выбором""", reply_markup=ikb_types_of_questions(), parse_mode=ParseMode.MARKDOWN_V2)
    await state.update_data(text=None)
    await state.update_data(variants=None)
    await state.update_data(correct=None)
    await state.update_data(type=None)
    await state.set_state(Current.event)


#-------------------------------------------------------------------------------

@router.callback_query(Current.setting_code, F.data == "ikb_back_actions_event")
async def add_test2(query: types.CallbackQuery, state: FSMContext):
    data_state = await state.get_data()
    name = data_state.get("event")
    await state.set_state(Current.event)
    ev = await event.get_event(data_state.get("event_id"))

    await query.message.answer(f"""⚡Выберите действие для мероприятия {name}
    
⚡Текущий код доуступа <code>{ev.password if ev.password else "⛔Пока не определен"}</code>""", reply_markup=ikb_current_test(), parse_mode=ParseMode.HTML)


@router.callback_query(F.data == "ikb_back_actions", Current.event)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get("event")
    ev = await event.get_event(data.get("event_id"))

    await callback.message.answer(f"""⚡Выберите действие для мероприятия {name}
    
⚡Текущий код доуступа <code>{ev.password if ev.password else "⛔Пока не определен"}</code>""", reply_markup=ikb_current_test(), parse_mode=ParseMode.HTML)


@router.callback_query(F.data == "ikb_back_to_notifications", Current.event)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get("event_name")
    ev = await event.get_event(data.get("event_id"))
    await callback.message.answer(f"""⚡ Выберите действие для мероприятия <b>{name}</b>
⚡Текущий код доуступа <code>{ev.password if ev.password else "⛔Пока не определен"}</code>""", reply_markup=ikb_current_test(), parse_mode=ParseMode.HTML)


@router.callback_query(F.data == "ikb_back_tochoose_opros", Current.event)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get("event")
    ev = await event.get_event(data.get("event_id"))
    await callback.message.answer(f"""⚡Выберите действие для мероприятия <b>{name}</b>
    
⚡Текущий код доуступа <code>{ev.password if ev.password else "⛔Пока не определен"}</code>""", reply_markup=ikb_current_test(), parse_mode=ParseMode.HTML)


#-------------------------------------------------------------------------------
@router.callback_query(F.data == "ikb_back_choose_questionnn", Current.event)
async def second(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Current.current_test)
    data = await state.get_data()
    id = data.get("current_test")
    kb = await ikb_all_questions(id)
    await callback.message.answer("⚡Выберите действие⚡", reply_markup=kb)


@router.callback_query(F.data == "ikb_back_choose_type", Current.rebuild_quest)
async def second(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Current.current_test)
    data = await state.get_data()
    id = data.get("current_test")
    kb = await ikb_all_questions(id)
    await callback.message.answer("⚡Выберите действие⚡", reply_markup=kb)
    await state.update_data(text=None)
    await state.update_data(variants=None)
    await state.update_data(correct=None)
    await state.update_data(type=None)


@router.callback_query(F.data == "ikb_back", Current2.correct)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("question")
    variants = data.get("variants")
    correct = data.get("correct")
    await callback.message.answer(f"""🛠️Вы в конструктуоре вопроса с <b>множественным выбором правильного ответа</b>

Предпросмотр вопроса - 
<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants if variants else "❌Не заполненно"}

<b>Правильные ответы:</b>
{correct if correct else "❌Не заполненно"}""", reply_markup=ikb_actions_qustion(), parse_mode=ParseMode.HTML)
    await state.set_state(Current2.event)


@router.callback_query(F.data == "ikb_back", Current2.question)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("question")
    variants = data.get("variants")
    correct = data.get("correct")
    await callback.message.answer(f"""🛠️Вы в конструктуоре вопроса с <b>множественным выбором правильного ответа</b>

Предпросмотр вопроса - 
<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants if variants else "❌Не заполненно"}

<b>Правильные ответы:</b>
{correct if correct else "❌Не заполненно"}""", reply_markup=ikb_actions_qustion(), parse_mode=ParseMode.HTML)
    await state.set_state(Current2.event)


@router.callback_query(F.data == "ikb_back", Current2.variants)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("question")
    variants = data.get("variants")
    correct = data.get("correct")
    await callback.message.answer(f"""🛠️Вы в конструктуоре вопроса с <b>множественным выбором правильного ответа</b>

Предпросмотр вопроса - 
<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants if variants else "❌Не заполненно"}

<b>Правильные ответы:</b>
{correct if correct else "❌Не заполненно"}""", reply_markup=ikb_actions_qustion(), parse_mode=ParseMode.HTML)
    await state.set_state(Current2.event)


@router.callback_query(F.data == "ikb_back", Current.correct)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("question")
    variants = data.get("variants")
    correct = data.get("correct")
    await callback.message.answer(f"""🛠️Вы в конструктуоре вопроса с <b>выбором единственного правильного ответа</b>

Предпросмотр вопроса - 
<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants if variants else "❌Не заполненно"}

<b>Правильные ответы:</b>
{correct if correct else "❌Не заполненно"}""", reply_markup=ikb_actions_qustion(), parse_mode=ParseMode.HTML)
    await state.set_state(Current.event)


@router.callback_query(F.data == "ikb_back", Current.question)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("question")
    variants = data.get("variants")
    correct = data.get("correct")
    await callback.message.answer(f"""🛠️Вы в конструктуоре вопроса с <b>выбором единственного правильного ответа</b>

Предпросмотр вопроса - 
<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants if variants else "❌Не заполненно"}

<b>Правильные ответы:</b>
{correct if correct else "❌Не заполненно"}""", reply_markup=ikb_actions_qustion(),parse_mode=ParseMode.HTML)
    await state.set_state(Current.event)


@router.callback_query(F.data == "ikb_back", Current.variants)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("question")
    variants = data.get("variants")
    correct = data.get("correct")
    await callback.message.answer(f"""🛠️Вы в конструктуоре вопроса с <b>выбором единственного правильного ответа</b>

Предпросмотр вопроса - 
<b>Текст вопроса:</b>
{text if text else "❌Не заполненно"}

<b>Варианты ответа:</b>
{variants if variants else "❌Не заполненно"}

<b>Правильные ответы:</b>
{correct if correct else "❌Не заполненно"}""", reply_markup=ikb_actions_qustion(), parse_mode=ParseMode.HTML)
    await state.set_state(Current.event)


#-----------------------------------------------------


@router.callback_query(F.data == "ikb_back", Current.setting_time2)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data_state = await state.get_data()
    num = data_state.get("setting_name")
    name = data_state.get("event")
    await callback.message.answer(f"⚡Выберите действие для теста <b>{num}</b> в мероприятии <b>{name}</b>", reply_markup=ikb_rebuild(), parse_mode=ParseMode.HTML)
    await state.set_state(Current.current_test)


@router.callback_query(F.data == "ikb_back", Current.setting_passing2)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data_state = await state.get_data()
    num = data_state.get("setting_name")
    name = data_state.get("event")
    await callback.message.answer(f"⚡Выберите действие для теста <b>{num}</b> в мероприятии <b>{name}</b>", reply_markup=ikb_rebuild(), parse_mode=ParseMode.HTML)
    await state.set_state(Current.current_test)


@router.callback_query(F.data == "ikb_back", Current.setting_code2)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data_state = await state.get_data()
    num = data_state.get("setting_name")
    name = data_state.get("event")
    await callback.message.answer(f"⚡Выберите действие для теста <b>{num}</b> в мероприятии <b>{name}</b>", reply_markup=ikb_rebuild(), parse_mode=ParseMode.HTML)
    await state.set_state(Current.current_test)


@router.callback_query(F.data == "back_to_rebuild_test", Current.event)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data_state = await state.get_data()
    num = data_state.get("setting_name")
    name = data_state.get("event")
    await callback.message.answer(f"⚡Выберите действие для теста <b>{num}</b> в мероприятии <b>{name}</b>", reply_markup=ikb_rebuild(), parse_mode=ParseMode.HTML)
    await state.set_state(Current.current_test)

#-----------------------------------------------------------------


@router.callback_query(F.data == "ikb_back", Current.setting_time)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data_state = await state.get_data()
    num = data_state.get("current_test")
    name = data_state.get("event")
    await callback.message.answer("""⚙️Выберите настройки опроса:
📝Имя теста в котором вы можете отразить тему теста 
🕒Время на прохождение теста
🕒Время через которое тест перестанет быть действительным""", reply_markup=ikb_settings_test())
    await state.set_state(Current.event)


@router.callback_query(F.data == "ikb_back", Current.setting_passing)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data_state = await state.get_data()
    num = data_state.get("current_test")
    name = data_state.get("event")
    await callback.message.answer("""⚙️Выберите настройки опроса:
📝Имя теста в котором вы можете отразить тему теста 
🕒Время на прохождение теста
🕒Время через которое тест перестанет быть действительным""", reply_markup=ikb_settings_test())
    await state.set_state(Current.event)


@router.callback_query(F.data == "ikb_back", Current.setting_code)
async def second(callback: types.CallbackQuery, state: FSMContext):
    data_state = await state.get_data()
    num = data_state.get("current_test")
    name = data_state.get("event")
    await callback.message.answer("""⚙️Выберите настройки опроса:
📝Имя теста в котором вы можете отразить тему теста 
🕒Время на прохождение теста
🕒Время через которое тест перестанет быть действительным""", reply_markup=ikb_settings_test())
    await state.set_state(Current.event)

#------------------------------------------------------


@router.callback_query(F.data == "ikb_back_actions", Current.current_test)
async def second(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Current.event)
    data = await state.get_data()
    id = data.get("event_id")
    print("id ", id)
    kb = await ikb_all_tests(id)
    await callback.message.answer("📋Список тестов", reply_markup=kb)



@router.callback_query(Current.current_test, F.data == "ikb_back_all_questions")
async def add_test2(query: types.CallbackQuery, state: FSMContext):
    data_state = await state.get_data()
    name = data_state.get("event")
    num = data_state.get("current_test")
    await state.update_data(current_test=num)
    await query.message.answer(f"⚡Выберите действие для теста номер <b>{num}</b> в мероприятии <b>{name}</b>", reply_markup=ikb_rebuild(), parse_mode=ParseMode.HTML)


@router.callback_query(Current.event, F.data == "ikb_back_all_questions")
async def add_test2(query: types.CallbackQuery, state: FSMContext):
    data_state = await state.get_data()
    name = data_state.get("event")
    num = data_state.get("current_test")
    await state.update_data(current_test=num)
    await query.message.answer(f"⚡Выберите действие для теста номер <b>{num}</b> в мероприятии <b>{name}</b>", reply_markup=ikb_rebuild(), parse_mode=ParseMode.HTML)


@router.callback_query(F.data == "ikb_back")
async def second(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("👋Приветствую, дорогой админ, выберите действие", reply_markup=ikb_main_menu())
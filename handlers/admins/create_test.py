from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram import types
from aiogram.filters import Command

from loader import bot
from keyboard.inline_main_menu import ikb_main_menu
from keyboard.ikb_back import ikb_back
from keyboard.save_event import ikb_save
from keyboard.ikb_all_events import ikb_all_events
from filters.is_admin import Admin
from set_logs1.logger_all1 import log_exceptions1

from utils.db_api.quck_commands import event
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from states.fsm import Creation, Current
from keyboard.ikb_all_events import ikb_all_events, Choose_event
from keyboard.ikb_current_test import ikb_current_test
from keyboard.ikb_settings_test import ikb_settings_test
from keyboard.ikb_timer import ikb_timer, Choose_timeer
from keyboard.ikb_adding_questions import ikb_adding_questions
from keyboard.ikb_types_questions import ikb_types_of_questions
from keyboard.list_tests import ikb_all_tests
from keyboard.ikb_delete_event import ikb_delete_event
from keyboard.ikb_notifications_test import ikb_notifications
from keyboard.ikb_notifications_choose import ikb_notifications_choose
from keyboard.ikb_notifications_test import Notifications_test
from keyboard.ikb_back import ikb_back_actions_event
from utils.db_api.quck_commands import tests, results, users
router = Router()




@router.callback_query(Choose_event.filter(F.cb=="ikb_choose"))
async def second(query: CallbackQuery, callback_data: Choose_event, state: FSMContext):
    data = await event.get_event(callback_data.id)
    name = data.event_name
    ev = await event.get_event(callback_data.id)
    await query.message.answer(f"""⚡ Выберите действие для мероприятия <b>{name}</b>

⚡Текущий код доуступа <code>{ev.password if ev.password else "⛔Пока не определен"}</code>""", reply_markup=ikb_current_test(), parse_mode=ParseMode.HTML)
    await state.set_state(Current.event)
    await state.update_data(event_id=callback_data.id)
    await state.update_data(event=name)

#---------------------------- Access Code ------------------------------------------------------


@router.callback_query(Current.event, F.data == "set_password")
async def add_test2(query: CallbackQuery, state: FSMContext):
    await state.set_state(Current.setting_code)
    data = await state.get_data()
    ev = await event.get_event(data.get("event_id"))

    await query.message.answer(f"""🔓Напишите код по которому будет осуществлен доступ к тестам вашего мероприятия, <b>код должен быть пятизначным числом</b>

⚡Текущий код доуступа <code>{ev.password if ev.password else "⛔Пока не определен"}</code>""", reply_markup=ikb_back_actions_event(), parse_mode=ParseMode.HTML)


@router.message(Current.setting_code, Admin())
async def add_test3(message: Message, state: FSMContext):
    code = message.text
    data = await state.get_data()
    name = data.get("event")
    event_id = data.get("event_id")
    ev = await event.get_event(data.get("event_id"))
    try:
        code = int(code)
        if code > 9999 and code < 100000:
            is_unique = True
            data_events = await event.get_all_events()
            for ev in data_events:
                if ev.password == code:
                    is_unique = False
                    break
            if is_unique:
                code = int(code)
                await event.update_code(event_id=event_id, code=code)
                await message.answer(f"""✅Код доступа к мероприятию *успешно* установлен {code}""", parse_mode=ParseMode.MARKDOWN_V2)
                ev = await event.get_event(event_id)
                await message.answer(f"""⚡ Выберите действие для мероприятия <b>{name}</b>

⚡Текущий код доуступа <code>{ev.password if ev.password else "⛔Пока не определен"}</code>""", reply_markup=ikb_current_test(), parse_mode=ParseMode.HTML)
                await state.set_state(Current.event)
            else:
                await message.answer("❌Данный код доступа *уже используется* в другом мероприятии\. Придумайте другой код", parse_mode=ParseMode.MARKDOWN_V2 )
                await message.answer(f"""⚡ Выберите действие для мероприятия <b>{name}</b>
                
⚡Текущий код доуступа <code>{ev.password if ev.password else "⛔Пока не определен"}</code>""", reply_markup=ikb_current_test(), parse_mode=ParseMode.HTML)
                await state.set_state(Current.event)
        else:
            await message.answer("❌Код доступа должен быть *пятизначным числом*", parse_mode=ParseMode.MARKDOWN_V2)
            await message.answer(f"""⚡ Выберите действие для мероприятия <b>{name}</b>
            
⚡Текущий код доуступа <code>{ev.password if ev.password else "⛔Пока не определен"}</code>""", reply_markup=ikb_current_test(), parse_mode=ParseMode.HTML)
            await state.set_state(Current.event)
    except Exception as err:
        await state.set_state(Current.event)
        print(err)
        await message.answer("❌Код может быть только *численнного формата*", parse_mode=ParseMode.MARKDOWN_V2)
        await message.answer(f"""⚡ Выберите действие для мероприятия <b>{name}</b>
        
⚡Текущий код доуступа <code>{ev.password if ev.password else "⛔Пока не определен"}</code>""", reply_markup=ikb_current_test(), parse_mode=ParseMode.HTML)
        await state.set_state(Current.event)


#---------------------------- Notifications ---------------------------------------------------

@router.callback_query(F.data == "get_stat", Current.event)
async def second(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    id_event = data.get("event_id")
    kb = await ikb_notifications(id_event=id_event)
    await query.message.answer(f"""🔔Вы в панели настройки уведомлений о прохождении тестов
Выберите тест для настройки получения уведомлений от бота при прохождении теста.
<b>По умолчанию уведомления выключены</b> и все результаты просматриваются по нажатию на кнопку с названием теста""", reply_markup=kb, parse_mode=ParseMode.HTML)


@router.callback_query(Notifications_test.filter(F.cb=="ikb_notifications"), Current.event)
async def second(query: CallbackQuery, callback_data: Notifications_test, state: FSMContext):
    test = await tests.get_current(id_test=callback_data.id, id_event=0)
    await state.update_data(current_test=callback_data.id)
    kb = await ikb_notifications_choose(query.from_user.id, callback_data.id)
    await query.message.answer(f"""🔔Выберите настройку уведомлений о прохождении теста {test.name}""", reply_markup=kb)


@router.callback_query(F.data == "ikb_check_results_admin", Current.event)
async def check_reuslts_admin(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    id_test = data.get("current_test")
    current_test = await tests.get_current(id_test=id_test, id_event=1)
    res = await results.get_all_results_id_test(id_test)
    if not res:
        await query.message.answer("❌Тест пока не был никем пройден")

    for result in res:
        current = [m for m in result.result]
        print(current)
        pluses = current.count("1")
        minuses = current.count("0")
        user = await users.get_current_user(result.id_user)
        name = user.first_name
        username = "@" + user.username
        await query.message.answer(f"""📊Результат пользователя <b>{username if username else "Неопознанно"}</b>

Имя <b>{name}</b>

Тест <b>{current_test.name}</b>:

✅ Правильных ответов - {pluses}
    
❌ Неправильных ответов - {minuses}
    
🎯 Выполнение - {(pluses / len(current) * 100) // 1} %
    
    
#results""", parse_mode=ParseMode.HTML)


@router.callback_query(F.data == "ikb_send", Current.event)
async def check_reuslts_admin(query: CallbackQuery, state: FSMContext):
    admin_id = query.from_user.id
    data = await state.get_data()
    id_test = data.get("current_test")
    await tests.add_notifications(id_test,admin_id)
    new_kb = await ikb_notifications_choose(query.from_user.id, id_test)
    await bot.edit_message_reply_markup(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        reply_markup=new_kb,
        inline_message_id=query.inline_message_id
    )


@router.callback_query(F.data == "ikb_dont_send", Current.event)
async def check_reuslts_admin(query: CallbackQuery, state: FSMContext):
    admin_id = query.from_user.id
    data = await state.get_data()
    id_test = data.get("current_test")
    await tests.delete_notifications(id_test, admin_id)
    new_kb = await ikb_notifications_choose(query.from_user.id, id_test)
    await bot.edit_message_reply_markup(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        reply_markup=new_kb,
        inline_message_id=query.inline_message_id
    )

#-------------------------------------- Удаляем мероприятие -------------------------------

@router.callback_query(Current.event, F.data == "delete_event")
async def add_test(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get("event")
    await query.message.answer(f"""🗑️Вы действительно хотите <b>удалить</b> меропириятие <b>{name}</b>?""", reply_markup=ikb_delete_event(), parse_mode=ParseMode.HTML)#parse_mode_был


@router.callback_query(Current.event, F.data == "ikb_delete_forever_event")
async def add_test(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get("event")
    event_id = data.get("event_id")
    try:
        await event.delete_event(event_id)
        await query.message.answer(f"""🗑️Мероприятие <b>{name}</b> было успешно удалено""", parse_mode=ParseMode.HTML)
        await query.message.answer("👋Приветствую, админ, выбери действие", reply_markup=ikb_main_menu())
        await state.clear()
    except Exception as err:
        await log_exceptions1("delete_event", "ERROR", "create_test.py", 214, err, query.from_user.id)

        await query.message.answer("❌Произошла ошибка, обратитесь к тех поддержке")


@router.callback_query(Current.event, F.data == "ikb_back_from_delete")
async def add_test(query: CallbackQuery, state: FSMContext):
    await query.message.answer("👋Приветствую, админ, выбери действие", reply_markup=ikb_main_menu())
    await state.clear()


#----------------------------- Основные настройки тестов ---------------------------------------------

@router.callback_query(Current.event, F.data == "create_test")
async def add_test(query: CallbackQuery, state: FSMContext):
    await query.message.answer("""🛠️Выберите настройки опроса:
📝*Название теста* 
🕒*Время на прохождение* теста
🕒*Время существования* теста""", reply_markup=ikb_settings_test(), parse_mode=ParseMode.MARKDOWN_V2)

@router.callback_query(Current.event, F.data == "ikb_name_for_test")
async def add_test2(query: CallbackQuery, state: FSMContext):
    await state.set_state(Current.setting_name)
    await query.message.answer("📝Напишите имя теста, *имя может содержать любые символы*", reply_markup=ikb_back(), parse_mode=ParseMode.MARKDOWN_V2)


@router.callback_query(Current.event, F.data == "time_to_answer")
async def add_test2(query: CallbackQuery, state: FSMContext):
    await state.set_state(Current.setting_passing)
    await query.message.answer("🕒Выберите ограничение по времени выполнения теста, *выразите в минутах*", reply_markup=ikb_back(),  parse_mode=ParseMode.MARKDOWN_V2)


@router.callback_query(Current.event, F.data == "time_of_test")
async def add_test2(query: CallbackQuery, state: FSMContext):
    await state.set_state(Current.setting_time)
    await query.message.answer("🕒Выберите ограничение по времени существования теста, *выразите в минутах*", reply_markup=ikb_timer(), parse_mode=ParseMode.MARKDOWN_V2)


@router.message(Current.setting_name, Admin())
async def add_test3(message: Message, state: FSMContext):
    code = message.text
    await state.update_data(setting_name=code)
    data = await state.get_data()
    setting_passing = data.get("setting_passing")
    setting_time = data.get("setting_time")
    await message.answer(f"✅Название теста успешно установлено <b>{code}</b>", parse_mode=ParseMode.HTML)
    await message.answer(f"""📝Название теста <b>{code}</b>
🕒Время на прохождение теста <b>{setting_passing if setting_passing else "❌Пока не указано"}</b>
🕒Время существования теста <b>{setting_time if setting_time else "❌Пока не указано"}</b>""", reply_markup=ikb_settings_test(), parse_mode=ParseMode.HTML)
    await state.set_state(Current.event)



@router.message(Current.setting_passing, Admin())
async def add_test3(message: Message, state: FSMContext):
    code = message.text
    data = await state.get_data()
    setting_name = data.get('setting_name')
    setting_time = data.get("setting_time")
    setting_passing = data.get("setting_passing")

    try:
        code = int(code)
        if code > 0:
            code = int(code)
            await state.update_data(setting_passing=code)
            await message.answer(f"✅Время на прохождение теста *успешно* установлено *{code}*", parse_mode=ParseMode.MARKDOWN_V2)
            await message.answer(f"""📝Название теста <b>{setting_name if setting_name else "❌Пока не указано"}</b>
🕒Время на прохождение теста <b>{code} минут</b>
🕒Время существования теста <b>{setting_time if setting_time else "❌Пока не указано"}</b>""", reply_markup=ikb_settings_test(), parse_mode=ParseMode.MARKDOWN_V2)
        else:
            await message.answer("❌Время должно быть *натуральным числом*", parse_mode=ParseMode.MARKDOWN_V2)
            await message.answer(f"""📝Название теста <b>{setting_name if setting_name else "❌Пока не указано"}</b>
🕒Время на прохождение теста <b>{setting_passing if setting_passing else "❌Пока не указано"}</b>
🕒Время существования теста <b>{setting_time if setting_time else "❌Пока не указано"}</b>""", reply_markup=ikb_settings_test(), parse_mode=ParseMode.MARKDOWN_V2)
        await state.set_state(Current.event)
    except:
        await state.set_state(Current.event)
        await message.answer("❌Время может быть только *численнного формата*")
        await message.answer(f"""📝Название теста <b>{setting_name if setting_name else "❌Пока не указано"}</b>
🕒Время на прохождение теста <b>{setting_passing if setting_passing else "❌Пока не указано"}</b>
🕒Время существования теста <b>{setting_time if setting_time else "❌Пока не указано"}</b>""", reply_markup=ikb_settings_test(), parse_mode=ParseMode.MARKDOWN_V2)


@router.callback_query(Current.setting_time, Choose_timeer.filter(F.cb=="ikb_time"))
async def add_test2(query: CallbackQuery, state: FSMContext, callback_data: Choose_timeer):
    await state.update_data(setting_time=callback_data.id)

    await query.message.answer(f"✅Время существования теста успешно установленно *{callback_data.id}*", parse_mode=ParseMode.MARKDOWN_V2)
    await query.message.answer("""📝*Название теста* 
🕒*Время на прохождение* теста
🕒*Время существования* теста""", reply_markup=ikb_settings_test(), parse_mode=ParseMode.MARKDOWN_V2)
    await state.set_state(Current.event)

#---------------------------------- Создание теста и добавление в бд --------------------------------------
async def get_unique_key(keys):
    for i in range(1000):
        if i not in keys:
            return i
    else: return None


@router.callback_query(Current.event, F.data == "ikb_create_questions")
async def add_test2(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    id = data.get("event_id")
    passing = data.get("setting_passing")
    time = data.get("setting_time")
    test_name = data.get("setting_name")

    if passing and time and test_name:
        try:
            all_test = await tests.get_all_tests()
            values = list()
            for t in all_test:
                values.append(int(t.id_test))
            id_test = await get_unique_key(values)
            await state.update_data(current_test=id_test)
            await tests.add_test(id_event=id, setting_time=time, setting_passing=passing, id_test=id_test, name=test_name)
            await query.message.answer("❔Можете приступить к заполнению вопросами", reply_markup=ikb_adding_questions())
            await state.update_data(setting_passing="")
            await state.update_data(setting_time="")
            await state.update_data(setting_name="")
        except Exception as err:
            await query.message.answer("❌При создании теста возникла ошибка", reply_markup=ikb_back())
            await log_exceptions1("create_test_final", "ERROR", "create_test.py", 339, err, query.from_user.id)
    else:
        await query.message.answer(f"""📝Название теста - <b>{test_name if test_name else "❌Пропущенно"}</b> 
🕘Время на прохождение теста - <b>{time if time else "❌Пропущенно"}</b>
🕘Время существования теста - <b>{passing if passing else "❌Пропущенно"}</b>

✍️Пожалуйста, заполните недостающие настройки теста""", reply_markup=ikb_settings_test(), parse_mode=ParseMode.HTML)




@router.callback_query(Current.event, F.data == "create_question")
async def add_test2(query: CallbackQuery, state: FSMContext):
    await query.message.answer("""✏️Выберите тип вопроса:
1️⃣1 тип \- вопрос с единственным правильным ответом
🔢2 тип \- вопрос с множественным выбором""", reply_markup=ikb_types_of_questions(), parse_mode=ParseMode.MARKDOWN_V2)


@router.callback_query(Current.event, F.data == "list_tests")
async def add_test2(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    id = data.get("event_id")
    kb = await ikb_all_tests(id)
    await query.message.answer("📋Список тестов", reply_markup=kb)



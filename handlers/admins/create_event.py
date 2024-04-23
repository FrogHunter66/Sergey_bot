from aiogram.enums import ParseMode
import datetime
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.types import Message, InlineKeyboardButton
from aiogram import types
from aiogram.filters import Command
from keyboard.inline_main_menu import ikb_main_menu
from keyboard.ikb_back import ikb_back
from keyboard.save_event import ikb_save
from keyboard.ikb_all_events import ikb_all_events, Choose_event
from filters.is_admin import Admin
from set_logs1.logger_all1 import log_exceptions1
from utils.db_api.quck_commands import event, users, admins, tests
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from states.fsm import Creation
router = Router()

@router.message(
    Command("start"),
    Admin()
)
async def first(message: Message):
    await message.answer("👋Приветствую, админ, выбери действие", reply_markup=ikb_main_menu(), parse_mode=ParseMode.HTML)


@router.callback_query(F.data == "tariff_info")
async def second(callback: types.CallbackQuery):
    admin = await users.get_current_user(callback.from_user.id)
    ev = admin.c_events
    tests = admin.c_tests
    date = (admin.data_end).strftime('%Y-%m-%d')
    await callback.message.answer(f"""ℹ️Остатки по пакету - 
🌟Мероприятий осталось - <b>{ev}</b>
🌟Тестов осталось - <b>{tests}</b>
⏳Время действия тарифа до - <b>{date}</b>

Для продления подписки вы можете оплатить новый пакет с помощью команды /buy""", parse_mode=ParseMode.HTML, reply_markup=ikb_back())




@router.callback_query(F.data == "create_event")
async def second(callback: types.CallbackQuery, state: FSMContext):
    admin = await users.get_current_user(callback.from_user.id)
    if admin.c_events > 0:
        await callback.message.answer(f"📝укажите название мероприятия. Доступно <b>{admin.c_events}</b> мероприятий для создания", reply_markup=ikb_back(), parse_mode=ParseMode.HTML)
        await state.set_state(Creation.name_event)
    else:
        await callback.message.answer(f"⛔ У вас закончились доступные мероприятия", reply_markup=ikb_back())


@router.callback_query(F.data == "get_events")
async def second(callback: types.CallbackQuery):
    ikb = await ikb_all_events(callback.from_user.id)
    await callback.message.answer('📅Доступные мероприятия', reply_markup=ikb)


@router.message(Creation.name_event, Admin())
async def name_event(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name_event=name)
    await message.answer(f"💾Сохранить мероприятие с названием <b>{name}</b>?", reply_markup=ikb_save(), parse_mode=ParseMode.HTML)


async def get_unique_key(keys):
    for i in range(1000):
        if i not in keys:
            return i
    else: return None

@router.callback_query(Creation.name_event, F.data == "ikb_save_event")
async def second(callback: types.CallbackQuery, state:FSMContext):
    data = await state.get_data()
    all_events = await event.get_all_events()
    keys = list()
    for e in all_events:
        keys.append(int(e.id_event))
    key = await get_unique_key(keys)
    admin = await users.get_current_user(callback.from_user.id)
    try:
        await event.add_event(id_event=key, name=str(data.get('name_event')))
        await admins.add_event(callback.from_user.id, key)
        await state.clear()
        await admins.decrement_events(callback.from_user.id)
        await callback.message.answer(f"✅Успешно добавлено мероприятие. Осталось досутпных мероприятий <b>{admin.c_events - 1}</b>", reply_markup=ikb_back(), parse_mode=ParseMode.HTML)
    except Exception as err:
        await callback.message.answer("❌Ошибка сохранения", reply_markup=ikb_back())
        await state.clear()
        print(err)
        await log_exceptions1("create_event_final", "ERROR", "create_event.py", 94, err, callback.from_user.id)

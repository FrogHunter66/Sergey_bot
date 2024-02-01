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
from utils.db_api.quck_commands import event
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from states.fsm import Creation
router = Router()

@router.message(
    Command("start"),
    Admin()
)
async def first(message: Message):
    await message.answer("Приветствую, админ, выбери действие", reply_markup=ikb_main_menu())


@router.callback_query(F.data == "create_event")
async def second(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Напишите название мероприятия", reply_markup=ikb_back())
    await state.set_state(Creation.name_event)


@router.callback_query(F.data == "get_events")
async def second(callback: types.CallbackQuery):
    ikb = await ikb_all_events()
    await callback.message.answer('Вот они, крассучики', reply_markup=ikb)


@router.message(Creation.name_event, Admin())
async def name_event(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name_event=name)
    await message.answer(f"Сохранить мероприятие с названием '{name}' ?", reply_markup=ikb_save())


@router.callback_query(Creation.name_event, F.data == "ikb_save_event")
async def second(callback: types.CallbackQuery, state:FSMContext):
    events_len =len(await event.get_all_events())
    print("handled")
    data = await state.get_data()
    try:
        await event.add_event(id_event=events_len+1, name=str(data.get('name_event')))
        await state.clear()
        await callback.message.answer("Удачно добавлено мероприятие", ikb_back())
    except Exception as err:
        await callback.message.answer("Ошибка сохранения", ikb_back())
        await state.clear()
        print(err)


@router.callback_query(F.data == "ikb_delete_name")
async def second(callback: types.CallbackQuery):
    await callback.message.answer('get')

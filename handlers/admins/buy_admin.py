from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
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
from keyboard.ikb_buy_admin import ikb_buy_admin, Choose_price
router = Router()


@router.message(Command("buy"))
async def first(message: Message):
    await message.answer("""👋Приветствую дорогой пользователь, предлагаю вам приобрести возможность создавать тесты и мероприятия
    
Прайс лист:""", reply_markup=ikb_buy_admin(), parse_mode=ParseMode.HTML)


@router.callback_query(Choose_price.filter(F.cb=="ikb_buy"))
async def second(query: CallbackQuery, callback_data: Choose_price, state: FSMContext):



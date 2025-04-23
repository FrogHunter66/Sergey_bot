from aiogram.enums import ParseMode
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram import types
from aiogram.filters import Command

from filters.Old_User import Old_user
from filters.is_admin import Admin
from filters.is_new_user import New_User
from keyboard.users_kb.ikb_start import ikb_start
from loader import bot
from set_logs1.logger_all1 import log_exceptions1
from utils.db_api.quck_commands import event, admins
from aiogram.fsm.context import FSMContext
from keyboard.ikb_buy_admin import ikb_buy_admin, Choose_price
import config


router = Router()
packages = [[1], [4]]
PRICE1 = types.LabeledPrice(label="🌟 Подписка на бота с полным функционалом на 7 дней - 300 рублей (пакет 1)", amount=300*100)  # в копейках (руб)
PRICE2 = types.LabeledPrice(label="👑 Подписка на бота с полным функционалом на 28 дней - 1000 рублей (пакет 2)", amount=1000*100)  # в копейках (руб)
prices = list([PRICE1, PRICE2])

@router.message(Command("buy"), Old_user())
async def first(message: Message):
    await message.answer("""👋Приветствую дорогой пользователь, предлагаю вам приобрести возможность создавать тесты и мероприятия

🛒Прайс лист:
🌟 Подписка на бота с полным функционалом на 7 дней
👑 Подписка на бота с полным функционалом на 30 дней 
""", reply_markup=ikb_buy_admin(), parse_mode=ParseMode.HTML)


@router.message(Command("buy"), Admin())
async def first(message: Message):
    await message.answer("""👋Приветствую дорогой администратор, предлагаю вам продить подписку на наш сервис

🛒Прайс лист:
🌟 Подписка на бота с полным функционалом на 7 дней
👑 Подписка на бота с полным функционалом на 30 дней """, reply_markup=ikb_buy_admin(), parse_mode=ParseMode.HTML)



@router.message(Command("buy"), New_User())
async def first(message: Message):
    await message.answer("❌ Перед покупкой роли администратора, необходимо зарегестрироваться", reply_markup=ikb_start())


@router.callback_query(Choose_price.filter(F.cb=="ikb_buy"))
async def second(query: CallbackQuery, callback_data: Choose_price, state: FSMContext):
    if config.PAYMENTS_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(query.message.chat.id, "Тестовый платеж")
    await bot.send_invoice(query.message.chat.id,
                           title=f"""{str(packages[callback_data.id-1][0]) + " неделю" if packages[callback_data.id-1][0] == 1 else str(packages[callback_data.id-1][0]) + " недели"} подписки""",
                           description=f"Активация подписки на бота по {callback_data.id} - ому пакету",
                           provider_token=config.PAYMENTS_TOKEN,
                           currency="rub",
                           photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[prices[callback_data.id-1]],
                           start_parameter="one-month-subscription",
                           payload=f"{callback_data.id}",
                           disable_notification=False)


# pre checkout  (must be answered in 10 seconds)
@router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)
    print(pre_checkout_q)


# successful payment
@router.message(F.successful_payment)
async def successful_payment(message:Message):
    """
    Успешная покупка роли
    :param message:
    :return:
    """
    print("SUCCESSFUL PAYMENT")
    payment_info = message.successful_payment
    print("INFO - ", packages[int(payment_info.invoice_payload)])
    response = await admins.successful_pay(message=message, package=packages[int(payment_info.invoice_payload)]) #TODO респонсе отправляется но нихуя не меняется если ты уже админ
    if response:
        await bot.send_message(message.chat.id, f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно")
        resp = [payment_info.invoice_payload, message.successful_payment.total_amount // 100]
        await admins.mail_to_admins(resp)
        await log_exceptions1("sucessfull_pay", "INFO", "buy_admin.py", 125, "sucessful_pay", message.from_user.id)


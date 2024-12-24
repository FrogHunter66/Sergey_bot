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
packages = [[1, 5, 5, 215, 1], [5, 10, 10, 850, 1], [10, 15, 15, 1400, 1], [30, 20, 20, 3850, 1], [999, 10000, 10000, 12000, 1], [10, 5, 5, 1600, 12], [25, 10, 10, 3200, 12], [50, 15, 15, 6500, 12], [100, 20, 20, 12000, 12], [10000, 10000, 10000, 28000, 12]]
PRICE1 = types.LabeledPrice(label="🌟 1 мероприятие, 5 тестов - 215 рублей (пакет 1)", amount=215*100)  # в копейках (руб)
PRICE2 = types.LabeledPrice(label="🌟 5 мероприятий, 10 тестов - 850 рублей (пакет 2)", amount=850*100)  # в копейках (руб)
PRICE3 = types.LabeledPrice(label="🌟 10 мероприятий, 15 тестов - 1400 рублей (пакет 3)", amount=1400*100)  # в копейках (руб)
PRICE4 = types.LabeledPrice(label="🌟 30 мероприятий, 20 тестов - 3850 рублей (пакет 4)", amount=3850*100)  # в копейках (руб)
PRICE5 = types.LabeledPrice(label="👑 Безлимит - 12000 ", amount=12000*100)  # в копейках (руб)
PRICE6 = types.LabeledPrice(label="💎 10 мероприятий, 5 тестов - 1600 рублей (пакет 5)", amount=1600*100)  # в копейках (руб)
PRICE7 = types.LabeledPrice(label="💎 25 мероприятий, 10 тестов - 3200 рублей (пакет 6)", amount=3200*100)  # в копейках (руб)
PRICE8 = types.LabeledPrice(label="💎 50 мероприятий, 15 тестов - 6500 рублей (пакет 7)", amount=6500*100)  # в копейках (руб)
PRICE9 = types.LabeledPrice(label="💎 100 мероприятий, 20 тестов - 12000 рублей (пакет 8)", amount=12000*100)  # в копейках (руб)
PRICE10 = types.LabeledPrice(label="👑 Безлимит - 28000", amount=28000*100)  # в копейках (руб)
prices = list([PRICE1, PRICE2, PRICE3, PRICE4, PRICE5, PRICE6, PRICE7, PRICE8, PRICE9, PRICE10])

@router.message(Command("buy"), Old_user())
async def first(message: Message):
    await message.answer("""👋Приветствую дорогой пользователь, предлагаю вам приобрести возможность создавать тесты и мероприятия

🛒Прайс лист:

Пакеты на месяц - 

🌟 1 мероприятие, 5 тестов, 5 опросов - 215 рублей (пакет 1)
🌟 5 мероприятий, 10 тестов, 10 опросов - 850 рублей (пакет 2)
🌟 10 мероприятий, 15 тестов, 15 опросов - 1400 рублей (пакет 3)
🌟 30 мероприятий, 20 тестов, 20 опросов - 3850 рублей (пакет 4)
👑 Безлимит - 12000 

Пакеты на год - 

💎 10 мероприятие, 5 тестов, 5 опросов  - 1600 рублей (пакет 5)
💎 25 мероприятий, 10 тестов, 10 опросов  - 3200 рублей (пакет 6)
💎 50 мероприятий, 15 тестов, 15 опросов  - 6500 рублей (пакет 7)
💎 100 мероприятий, 20 тестов, 20 опросов  - 12000 рублей (пакет 8)
👑 Безлимит - 28000 
""", reply_markup=ikb_buy_admin(), parse_mode=ParseMode.HTML)


@router.message(Command("buy"), Admin())
async def first(message: Message):
    await message.answer("""👋Приветствую дорогой администратор, предлагаю вам продить подписку на наш сервис

🛒Прайс лист:

Пакеты на месяц - 

🌟 1 мероприятие, 5 тестов, 5 опросов - 215 рублей (пакет 1)
🌟 5 мероприятий, 10 тестов, 10 опросов - 850 рублей (пакет 2)
🌟 10 мероприятий, 15 тестов, 15 опросов - 1400 рублей (пакет 3)
🌟 30 мероприятий, 20 тестов, 20 опросов - 3850 рублей (пакет 4)
👑 Безлимит - 12000 

Пакеты на год - 

💎 10 мероприятие, 5 тестов, 5 опросов  - 1600 рублей (пакет 5)
💎 25 мероприятий, 10 тестов, 10 опросов  - 3200 рублей (пакет 6)
💎 50 мероприятий, 15 тестов, 15 опросов  - 6500 рублей (пакет 7)
💎 100 мероприятий, 20 тестов, 20 опросов  - 12000 рублей (пакет 8)
👑 Безлимит - 28000 
""", reply_markup=ikb_buy_admin(), parse_mode=ParseMode.HTML)



@router.message(Command("buy"), New_User())
async def first(message: Message):
    await message.answer("❌ Перед покупкой роли администратора, необходимо зарегестрироваться", reply_markup=ikb_start())


@router.callback_query(Choose_price.filter(F.cb=="ikb_buy"))
async def second(query: CallbackQuery, callback_data: Choose_price, state: FSMContext):
    if config.PAYMENTS_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(query.message.chat.id, "Тестовый платеж")
    await bot.send_invoice(query.message.chat.id,
                           title=f"""{str(packages[callback_data.id-1][-1]) + " месяц" if packages[callback_data.id-1][-1] == 1 else str(packages[callback_data.id-1][-1]) + " месяцев"} подписки, {packages[callback_data.id-1][0]} мероприятий и {packages[callback_data.id-1][1]} тестов""",
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
    print("SUCCESSFUL PAYMENT")
    payment_info = message.successful_payment
    print("INFO - ", packages[int(payment_info.invoice_payload)])
    response = await admins.successful_pay(message=message, package=packages[int(payment_info.invoice_payload)]) #TODO респонсе отправляется но нихуя не меняется если ты уже админ
    if response:
        await bot.send_message(message.chat.id, f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно")
        resp = [payment_info.invoice_payload, message.successful_payment.total_amount // 100]
        await admins.mail_to_admins(resp)
        await log_exceptions1("sucessfull_pay", "INFO", "buy_admin.py", 125, "sucessful_pay", message.from_user.id)


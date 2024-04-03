from aiogram.enums import ParseMode
from aiogram.types import Message
from logs.log_all import log_all
from utils.models import Event, db, User
from loader import bot
from asyncpg import UniqueViolationError
from utils.db_api.quck_commands import users
import datetime


async def notify_main_adm(response, level):
    await bot.send_message(984974593, f"""Уведомление об ошибке: {response}
at level: {level}""")



async def mail_to_admins(response):
    admins = await users.get_all_admins()
    for adm in admins:
        await bot.send_message(adm.id, f"""🔔Уведомление об успешной покупке тарифа по пакету: <b>{response[0]}</b>
На сумму <b>{response[1]}</b>""", parse_mode=ParseMode.HTML)



async def successful_pay(message: Message, package:list):
    try:
        user = await users.get_current_user(message.from_user.id)
    except Exception as err:
        await users.add_user(id=message.from_user.id, username=message.from_user.username, first_name=message.from_user.first_name, last_name=message.from_user.last_name, status="user")
        user = await users.get_current_user(message.from_user.id)
    if user.status == "admin":
        return True
    try:
        if user.data_end:
            end_time = (user.data_end + datetime.timedelta(days=package[3]*31)).replace(microsecond=0)
            await user.update(data_end=end_time).apply()
            events = user.c_events
            tests = user.c_tests
            await user.update(c_events=package[0] + events).apply()
            await user.update(c_tests=package[1] + tests).apply()
        else:
            current = datetime.datetime.utcnow() + datetime.timedelta(days=package[3]*31, hours=3)
            current = current.replace(tzinfo=datetime.timezone.utc, microsecond=0)
            await user.update(data_end=current).apply()
            await user.update(c_events=package[0]).apply()
            await user.update(c_tests=package[1]).apply()
        if user.status == "user":
            await user.update(status="admin_buy").apply()
        return True
    except Exception as err:
        await bot.send_message(message.from_user.id, f"⛔ К сожалению произошла ошибка, обратитесь к администрации")
        await log_all("sucessfull_pay", "ERROR", "admins.py", 52, err, message.from_user.id)
        return False


async def decrement_events(id_user):
    user = await users.get_current_user(id_user)
    ev = user.c_events
    await user.update(c_events=ev - 1).apply()


async def add_event(id_user, id_event):
    admin = await users.get_current_user(id_user)
    if admin.events:
        lst = list(map(int, admin.events.split()))
        lst.append(id_event)
        await admin.update(events=lst).apply()
    else:
        lst = [id_event]
        await admin.update(events=lst).apply()
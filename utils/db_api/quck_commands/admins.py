from aiogram.types import Message

from utils.models import Event, db, User
from loader import bot
from asyncpg import UniqueViolationError
from utils.db_api.quck_commands import users
import datetime
# etting_time = "15123123m"
# print(setting_time[:-1])
# current_time = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
# time = current_time.replace(tzinfo=datetime.timezone.utc)
# end_time = current_time + datetime.timedelta(hours=33)
# print(time, current_time)


#
# current_time = datetime.datetime.utcnow()
# current_time = current_time.replace(tzinfo=datetime.timezone.utc, microsecond=0)
# end_time = current_test.end_time.replace(microsecond=0)
# differ = end_time - current_time
# if current_time < end_time:


async def successful_pay(message: Message, package:list):
    try:
        user = await users.get_current_user(message.from_user.id)
    except Exception as err:
        await users.add_user(id=message.from_user.id, username=message.from_user.username, first_name=message.from_user.first_name, last_name=message.from_user.last_name, status="user")
        user = await users.get_current_user(message.from_user.id)
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
            print("none - ", current)
            await user.update(data_end=current).apply()
            await user.update(c_events=package[0]).apply()
            await user.update(c_tests=package[1]).apply()
        if user.status !='admin_b':
            await user.update(status="admin_b").apply()
        return True
    except Exception as err:
        await bot.send_message(message.from_user.id, f"⛔ К сожалению произошла ошибка, обратитесь к администрации")
        print(err) #todo Добавить объявление и информацию по поводу события
        return False


async def decrement_events(id_user):
    user = await users.get_current_user(id_user)
    ev = user.c_events
    await user.update(c_events=ev - 1).apply()
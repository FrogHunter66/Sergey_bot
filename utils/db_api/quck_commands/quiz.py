from utils.db_api.quck_commands import users
from utils.models import Quiz, db
import datetime
from loader import bot
from asyncpg import UniqueViolationError


async def add_test(id_test:int, setting_passing:int, setting_time:str, id_event:int, name:str):
    setting_time1 = setting_time
    current_time = datetime.datetime.utcnow() + datetime.timedelta(hours=3)

    if setting_time[-1] == "m":
        setting_time = setting_time[:-1]
        end_time = current_time + datetime.timedelta(minutes=int(setting_time))
    elif setting_time[-1] == "h":
        setting_time = setting_time[:-1]
        end_time = current_time + datetime.timedelta(hours=int(setting_time))
    elif setting_time[-1] == "d":
        setting_time = setting_time[:-1]
        end_time = current_time + datetime.timedelta(days=int(setting_time))
    else:
        end_time = datetime.datetime(2030, 1, 1, 0, 0, 0)

    test = Quiz(quiz_id=id_test, lifetime=setting_time1, bound_time=setting_passing, event_id=[id_event], end_time=end_time, name=name)
    await test.create()


async def get_current(id_event, id_test):
    events = await get_all_tests()
    for i, event in enumerate(events):
        if event.id_test == id_test:

            return event
    return 0

async def get_all_tests_in_event(id):
    lst = list()
    tests = await get_all_tests()
    for i, test in enumerate(tests):
        if test.id_event:
            if id in test.id_event:
                lst.append(test)
    return lst


async def get_all_tests():
    events = await Quiz.query.gino.all()

    return events


async def update_bound_time(id_test, id_event, new_time):
    user = await get_current(id_event=id_event, id_test=id_test)
    await user.update(bound_time=int(new_time)).apply()


async def update_lifetime(id_test, id_event, new_time):
    user = await get_current(id_event=id_event, id_test=id_test)
    await user.update(lifetime=new_time).apply()


async def update_name(id_test, id_event, new_name):
    user = await get_current(id_event=id_event, id_test=id_test)
    await user.update(name=new_name).apply()


async def add_notifications(id_test, id_admin):
    test = await get_current(id_test=id_test, id_event=1)
    try:
        notifications = list(test.notifications)
        notifications.index(id_admin)
    except:
        notifications = [id_admin]
    await test.update(notifications=notifications).apply()


async def delete_notifications(id_test, id_admin):
    test = await get_current(id_test=id_test, id_event=1)
    try:
        notifications = list(test.notifications)
        ind = notifications.index(id_admin)
        notifications.pop(ind)
        await test.update(notifications=notifications).apply()
    except:
        pass

async def decrement_tests(id_user):
    user = await users.get_current_user(id_user)
    ev = int(user.c_tests)
    await user.update(c_tests=ev - 1).apply()


async def add_event_test(event_id, id_test):
    test = await get_current(id_test=id_test, id_event=1)
    try:
        if test.id_event:
            current_events_test = list(test.id_event)
            current_events_test.append(int(event_id))
            await test.update(id_event=current_events_test).apply()
        else:
            await test.update(id_event=[event_id]).apply()
    except Exception as err:
        print("ERR", err)



async def delete_event_test(event_id, id_test):
    test = await get_current(id_test=id_test, id_event=1)
    try:
        current_events_test = list(test.id_event)
        ind = current_events_test.index(event_id)
        current_events_test.pop(ind)
    except:
        current_events_test = list(test.id_event)
    await test.update(id_event=current_events_test).apply()

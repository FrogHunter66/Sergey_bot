from utils.models import Test, db
import datetime
from loader import bot
from asyncpg import UniqueViolationError


async def add_test(id_test:int, setting_code:int, setting_passing:int, setting_time:str, id_event:int, name:str):
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

    test = Test(id_test=id_test, token=setting_code, lifetime=setting_time1, bound_time=setting_passing, id_event=id_event, end_time=end_time, name=name)
    await test.create()


async def get_current(id_event, id_test):
    events = await get_all_tests()
    for i, event in enumerate(events):
        if event.id_test == id_test:
            print("test - ", event)
            return event
    return 0

async def get_all_tests_in_event(id):
    lst = list()
    events = await get_all_tests()
    for i, event in enumerate(events):
        if event.id_event == id:
            lst.append(event)
    return lst


async def get_all_tests():
    events = await Test.query.gino.all()
    return events


async def update_code(id_test, id_event, new_code):
    user = await get_current(id_event=id_event, id_test=id_test)
    await user.update(token=int(new_code)).apply()


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
    print(notifications)
    await test.update(notifications=notifications).apply()


async def delete_notifications(id_test, id_admin):
    test = await get_current(id_test=id_test, id_event=1)
    try:
        notifications = list(test.notifications)
        ind = notifications.index(id_admin)
        notifications.pop(ind)
        print("Удалился")
        await test.update(notifications=notifications).apply()
    except:
        pass


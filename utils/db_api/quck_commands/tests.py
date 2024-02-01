from utils.models import Test, db
from loader import bot
from asyncpg import UniqueViolationError


async def add_test(id_test:int, setting_code:int, setting_passing:int, setting_time:int, id_event:int):

    test = Test(id_test=id_test, token=setting_code, lifetime=setting_time, bound_time=setting_passing, id_event=id_event)
    await test.create()


async def get_current(id_event, id_test):
    events = await get_all_tests()
    for i, event in enumerate(events):
        if event.id_event == id_event and event.id_test == id_test:
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
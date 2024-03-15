from utils.models import Results, db
import datetime
from loader import bot
from asyncpg import UniqueViolationError

async def get_uniq_id():
    results = await get_all_results()
    lst_result = list()
    for i, res in enumerate(results):
        lst_result.append(res.id)
    lst = [m for m in range(1, 10000)]
    for key in lst:
        if key not in lst_result:
            return key
    return None


async def add_result(id_test:int, id_user:int, result:list):
    id = get_uniq_id()
    res = ""
    for i in result:
        res += str(i)
    res = Results(id=id, id_test=id_test, id_user=id_user, result=res)
    await res.create()


# async def get_current(id_event, id_test):
#     events = await get_all_tests()
#     for i, event in enumerate(events):
#         if event.id_test == id_test:
#             print("test - ", event)
#             return event
#     return 0


async def get_all_results_id_test(id):
    lst = list()
    results = await get_all_results()
    for i, res in enumerate(results):
        if res.id_test == id:
            lst.append(res)
    return lst



async def get_all_results_id_user(id):
    lst = list()
    results = await get_all_results()
    for i, res in enumerate(results):
        if res.id_user == id:
            lst.append(res)
    return lst


async def get_all_results():
    events = await Results.query.gino.all()
    return events


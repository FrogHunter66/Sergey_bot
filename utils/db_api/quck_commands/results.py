from utils.models import Results, db
import datetime
from loader import bot
from asyncpg import UniqueViolationError

async def get_uniq_id():
    results = await get_all_results()
    lst_results = [res for res in results.id]
    lst = [m for m in range(1, 10000)]
    for key in lst:
        if key not in lst:
            return key
    return None


async def add_result(id_test:int, id_user:int, result:list):
    id = get_uniq_id()
    res = Results(id=id, id_test=id_test, id_user=id_user, result=result)
    await res.create()


# async def get_current(id_event, id_test):
#     events = await get_all_tests()
#     for i, event in enumerate(events):
#         if event.id_test == id_test:
#             print("test - ", event)
#             return event
#     return 0
#
async def get_all_results_id(id):
    lst = list()
    results = await get_all_results()
    for i, res in enumerate(results):
        if res.id_user == id:
            lst.append(res)
    return lst


async def get_all_results():
    events = await Results.query.gino.all()
    return events

#
# async def update_code(id_test, id_event, new_code):
#     user = await get_current(id_event=id_event, id_test=id_test)
#     await user.update(token=int(new_code)).apply()
#
#
# async def update_bound_time(id_test, id_event, new_time):
#     user = await get_current(id_event=id_event, id_test=id_test)
#     await user.update(bound_time=int(new_time)).apply()
#
#
# async def update_lifetime(id_test, id_event, new_time):
#     user = await get_current(id_event=id_event, id_test=id_test)
#     await user.update(lifetime=new_time).apply()
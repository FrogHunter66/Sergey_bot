from utils.models import Questions, db
from loader import bot
from asyncpg import UniqueViolationError


async def add_test(id_quest:int, id_test:int, type:int, variants:list, correct_answer:list):

    test = Questions(id_quest=id_quest, id_test=id_test, type=type, variants=variants, correct_answer=correct_answer)
    await test.create()


async def get_questions(id_test):
    events = await Questions.query.gino.all()
    lst = list()
    for i, event in enumerate(events):
        if event.id_test == id_test:
            lst.append(event)
    return lst


async def get_all_quest():
    events = await Questions.query.gino.all()
    return events
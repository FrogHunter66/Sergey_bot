from utils.models import Questions, db
from loader import bot
from asyncpg import UniqueViolationError


async def add_test(id_quest:int, id_test:int, quest_type:int, variants, correct_answer, text):
    try:
        if type(variants) == str:
            pass
        elif type(variants) == list:
            variants = ".*.".join(variants)
        else:
            pass

        if type(correct_answer) == str:
            pass
        elif type(correct_answer) == list:
            correct_answer = ".*.".join(correct_answer)
        else:
            pass

        test = Questions(id_quest=id_quest, id_test=id_test, type=quest_type, variants=variants, correct_answer=correct_answer, text=text)
        await test.create()
    except Exception as err:
        print(err)


async def get_questions(id_test):

    events = await Questions.query.gino.all()

    lst = list()

    for i, event in enumerate(events):
        if event.id_test == id_test:
            lst.append(event)
    return lst


async def get_current(id_quest):
    quests = await get_all_quest()
    for quest in quests:
        if quest.id_quest == id_quest:
            return quest
    else:
        return 0



async def change_vars(id_quest, new_vars):
    if type(new_vars) == str:
        pass
    elif type(new_vars) == list:
        new_vars = ".*.".join(new_vars)
    else:
        pass

    user = await get_current(id_quest=id_quest)
    await user.update(variants=new_vars).apply()

async def change_correct(id_quest, new_correct):
    if type(new_correct) == str:
        pass
    elif type(new_correct) == list:
        new_correct = ".*.".join(new_correct)
    else:
        pass

    user = await get_current(id_quest=id_quest)
    await user.update(correct_answer=new_correct).apply()


async def change_text(id_quest, new_text:str):
    user = await get_current(id_quest=id_quest)
    await user.update(text=new_text).apply()



async def get_all_quest():
    events = await Questions.query.gino.all()
    return events
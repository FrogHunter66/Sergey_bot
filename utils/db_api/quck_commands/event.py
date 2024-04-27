from utils.db_api.quck_commands import users, admins
from utils.models import Event, db
from loader import bot
from asyncpg import UniqueViolationError


async def add_event(id_event:int, name:str):
    ev = Event(id_event=id_event, event_name=name)
    await ev.create()
    # except Exception as err:
    #     print(err)

async def get_event(id):
    user = await Event.query.where(Event.id_event == id).gino.first()
    return user

async def get_all_events():
    events = await Event.query.gino.all()
    return events

async def select_event(event_id):
    event = await Event.query.where(Event.id_event == event_id).gino.first()
    return event

async def delete_event(event_id):
    admins_lst = await users.get_all_admins()
    for adm in admins_lst:
        await admins.delete_event(event_id, adm.id)
    info = await Event.query.where(Event.id_event == event_id).gino.first()
    await info.delete()


async def update_code(event_id, code):
    ev = await Event.query.where(Event.id_event == event_id).gino.first()
    await ev.update(password=code).apply()

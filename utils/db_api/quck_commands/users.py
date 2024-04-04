from utils.models import Event, db, User
from loader import bot
from asyncpg import UniqueViolationError

async def notify_main_adm(response, level):
    await bot.send_message(984974593, f"""Уведомление об ошибке: {response}
at level: {level}""")


async def get_all_admins():
    lst = []
    users = await User.query.gino.all()
    for user in users:
        if user.status == "admin":
           lst.append(user)
    return lst


async def get_all_users():
    users = await User.query.gino.all()
    return users


async def get_current_user(id):
    users = await get_all_users()
    for i, user in enumerate(users):
        if user.id == id:
            return user
    return 0


async def add_user(id:int, username, first_name, last_name, status):
    test = User(id=id, username=username, first_name=first_name, last_name=last_name, status=status)
    await test.create()

async def update_status(id_user, new_status):
    user = await get_current_user(id_user)
    lst = list(user.events)
    lst.append(new_status)
    await user.update(events=lst).apply()



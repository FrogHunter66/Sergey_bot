from utils.models import Event, db, User
from loader import bot
from asyncpg import UniqueViolationError

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





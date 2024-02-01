from utils.models import Event, db, User
from loader import bot
from asyncpg import UniqueViolationError


async def get_all_users():
    users = await User.query.gino.all()
    return users

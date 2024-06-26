from typing import Union, Dict, Any

from aiogram.filters import BaseFilter
from aiogram.types import Message
from utils.db_api.quck_commands import users

class Admin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        id = message.from_user.id
        all_users = (await users.get_all_users())
        for i in range(len(all_users)):
            if id == all_users[i].id and (all_users[i].status == "admin" or all_users[i].status == "admin_buy"):
                return True
        return False
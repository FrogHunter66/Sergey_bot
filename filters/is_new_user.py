from typing import Union, Dict, Any

from aiogram.filters import BaseFilter
from aiogram.types import Message
from utils.db_api.quck_commands import users


class New_User(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        id = message.from_user.id
        all_users = (await users.get_all_users())
        flag = True
        for i in range(len(all_users)):
            if id == all_users[i].id:
                flag = False
        return flag
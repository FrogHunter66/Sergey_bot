from logs.logging_loguru.logger import logger
from utils.db_api.quck_commands.admins import notify_main_adm
from loader import dp


async def log_all(func_name, level, file_name="", num=0, log_message='', user_id=''):
    try:
        if level == 'info':
            logger.info(f"in {func_name}, file: {file_name}, string: {num} :: id: {user_id} :: {log_message}")
            await notify_main_adm(f'⚙ℹ `Info`\nin `{func_name}`, file: {file_name}, string: {num} :: id: `{user_id}` :: `{log_message}`', level)
        if level == 'warning':
            logger.warning(f"in {func_name}, file: {file_name}, string: {num} :: id: {user_id},  :: {log_message}")
            await notify_main_adm(f'⚙⚠ `Warning`\nin `{func_name}`, file: {file_name}, string: {num} :: id: `{user_id}` :: `{log_message}`', level)
        if level == 'error':
            logger.error(f"in {func_name}, file: {file_name}, string: {num} :: id: {user_id} :: {log_message}")
            await notify_main_adm(f'⚙🚫 `Error`\nin `{func_name}`, file: {file_name}, string: {num} :: id: `{user_id}` :: `{log_message}`', level)
    except Exception as error:
        logger.error(f"in {log_all} :: id: {user_id}, file: {file_name}, string: {num} :: {error}")

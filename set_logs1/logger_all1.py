from set_logs1.logging_loguru.logger import logger
from utils.db_api.quck_commands.users import notify_main_adm
from loader import dp


async def log_exceptions1(func_name, level, file_name="", num=0, log_message='', user_id=''):
    try:
        print("")
        if level == 'INFO':
            logger.info(f"in {func_name}, file: {file_name}, string: {num} :: id: {user_id} :: {log_message}")
            await notify_main_adm(f'⚙ℹ `Info`\nin `{func_name}`, file: {file_name}, string: {num} :: id: `{user_id}` :: `{log_message}`', level)
        if level == 'WARNING':
            logger.warning(f"in {func_name}, file: {file_name}, string: {num} :: id: {user_id},  :: {log_message}")
            await notify_main_adm(f'⚙⚠ `Warning`\nin `{func_name}`, file: {file_name}, string: {num} :: id: `{user_id}` :: `{log_message}`', level)
        if level == 'ERROR':
            logger.error(f"in {func_name}, file: {file_name}, string: {num} :: id: {user_id} :: {log_message}")
            await notify_main_adm(f'⚙🚫 `Error`\nin `{func_name}`, file: {file_name}, string: {num} :: id: `{user_id}` :: `{log_message}`', level)
    except Exception as error:
        logger.error(f"in {log_exceptions1} :: id: {user_id}, file: {file_name}, string: {num} :: {error}")

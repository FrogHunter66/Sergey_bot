from loguru import logger

logger.add('set_logs1/logfile.log', format='{time} :: {level} :: {message}', level='INFO', rotation='1 week', compression='zip')

from loguru import logger

logger.add('logs/logfile.log', format='{time} :: {level} :: {message}', level='INFO', rotation='1 week', compression='zip')

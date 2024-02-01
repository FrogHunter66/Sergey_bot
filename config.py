import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TELEGRAM_TOKEN = str(os.getenv('TOKEN'))
PG_USER= str(os.getenv('PG_USER'))
PG_PASSWORD = str(os.getenv('PG_PASSWORD'))
IP = str(os.getenv('IP'))
DATABASE = str(os.getenv('DATABASE'))

POSTGRES_URI=f'postgresql://{PG_USER}:{PG_PASSWORD}@{IP}/{DATABASE}'
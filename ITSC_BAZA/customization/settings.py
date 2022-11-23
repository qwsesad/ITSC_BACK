import os
from distutils.util import strtobool
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


# Считываем настройки
BOT_TOKEN = os.getenv('BOT_TOKEN')
AUTH = strtobool(os.getenv('AUTH'))
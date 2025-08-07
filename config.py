import os
from dotenv import load_dotenv

load_dotenv()  # загрузка переменных из .env

API_KEY = {"X-API-KEY": os.getenv("KINOPOLISK_API_KEY")}
BASE_URL_API = os.getenv("KINOPOLISK_BASE_URL")
MAIN_PAGE_URL = os.getenv("KINOPOLISK_MAIN_PAGE_URL")

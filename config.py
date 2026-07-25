from dotenv import load_dotenv

import os

load_dotenv()

APP_NAME = os.getenv("APP_NAME")
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")
BACKUP_OUTPUT = os.getenv("BACKUP_OUTPUT", "backups")
TEST_BACKUP_PATH = os.getenv("TEST_BACKUP_PATH")

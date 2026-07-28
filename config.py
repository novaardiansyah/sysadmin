from dotenv import load_dotenv

import os

load_dotenv()

APP_NAME = os.getenv("APP_NAME")
API_URL  = os.getenv("API_URL")
API_KEY  = os.getenv("API_KEY")

BACKUP_OUTPUT    = os.getenv("BACKUP_OUTPUT", "backups")
TEST_BACKUP_PATH = os.getenv("TEST_BACKUP_PATH")

R2_ACCOUNT_ID        = os.getenv("R2_ACCOUNT_ID")
R2_ACCESS_KEY_ID    = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET_NAME       = os.getenv("R2_BUCKET_NAME")
R2_ENDPOINT_URL      = os.getenv("R2_ENDPOINT_URL")
R2_ENABLED           = os.getenv("R2_ENABLED", "false").lower() in ("true", "1", "yes")

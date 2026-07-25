import requests

from config import (
  API_URL,
  API_KEY
)

def send_backup(result):
  headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
  }

  response = requests.post(
    f"{API_URL}/backups",
    headers=headers,
    json=result.__dict__
  )

  response.raise_for_status()

  return response.json()
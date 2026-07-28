import requests

from config import (
  API_URL,
  API_KEY
)

def check_schedule():
  headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept":        "application/json"
  }

  response = requests.get(
    f"{API_URL}/backups/check-schedule",
    headers=headers
  )

  if response.status_code == 404:
    return []

  response.raise_for_status()
  data = response.json()

  if isinstance(data, dict):
    jobs = data.get("data")
    if jobs is None:
      return []
    if isinstance(jobs, list):
      return jobs
    if isinstance(jobs, dict):
      return [jobs]

  return []

def store_job_report(job_id, result):
  headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept":        "application/json",
    "Content-Type":  "application/json"
  }

  payload = result.__dict__ if hasattr(result, "__dict__") else result

  response = requests.post(
    f"{API_URL}/backups/jobs/{job_id}/report",
    headers=headers,
    json=payload
  )

  response.raise_for_status()

  return response.json()

def send_backup(result):
  headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept":        "application/json"
  }

  response = requests.post(
    f"{API_URL}/backups",
    headers=headers,
    json=result.__dict__
  )

  response.raise_for_status()

  return response.json()
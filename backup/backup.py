from datetime import datetime
from pathlib import Path

from backup.zip import create_zip
from models.backup_result import BackupResult
from utils.checksum import sha256
from api.report import send_backup, store_job_report
from config import BACKUP_OUTPUT

def run_backup_job(job: dict):
  job_id            = job["id"]
  source_path       = job["source_path"]
  dest_dir          = job.get("destination_path") or BACKUP_OUTPUT
  expected_filename = job.get("expected_filename")

  started = datetime.now()

  try:
    if expected_filename:
      filename = expected_filename[:-4] if expected_filename.endswith(".zip") else expected_filename
    else:
      filename = f"backup-{started.strftime('%Y%m%d-%H%M%S')}"

    destination = str(Path(dest_dir) / filename)
    zip_file    = create_zip(source_path, destination)
    completed   = datetime.now()
    duration    = int((completed - started).total_seconds())

    result = BackupResult(
      file_name=Path(zip_file).name,
      file_path=zip_file,
      file_size=Path(zip_file).stat().st_size,
      checksum=sha256(zip_file),
      started_at=started.isoformat(),
      completed_at=completed.isoformat(),
      finished_at=completed.isoformat(),
      duration=duration,
      status="success",
      type="files",
      message="Backup completed successfully"
    )
  except Exception as e:
    completed = datetime.now()
    duration  = int((completed - started).total_seconds())

    result = BackupResult(
      file_name="",
      file_path="",
      file_size=0,
      checksum="",
      started_at=started.isoformat(),
      completed_at=completed.isoformat(),
      finished_at=completed.isoformat(),
      duration=duration,
      status="failed",
      type="files",
      message=f"Backup failed: {str(e)}"
    )

  response = store_job_report(job_id, result)

  print(response)
  return response

def run_backup(source_path: str | dict):
  if isinstance(source_path, dict):
    return run_backup_job(source_path)

  started = datetime.now()

  try:
    filename = f"backup-{started.strftime('%Y%m%d-%H%M%S')}"

    destination = str(Path(BACKUP_OUTPUT) / filename)
    zip_file    = create_zip(source_path, destination)
    completed   = datetime.now()
    duration    = int((completed - started).total_seconds())

    result = BackupResult(
      file_name=Path(zip_file).name,
      file_path=zip_file,
      file_size=Path(zip_file).stat().st_size,
      checksum=sha256(zip_file),
      started_at=started.isoformat(),
      completed_at=completed.isoformat(),
      finished_at=completed.isoformat(),
      duration=duration,
      status="success",
      type="files",
      message="Backup completed successfully"
    )
  except Exception as e:
    completed = datetime.now()
    duration  = int((completed - started).total_seconds())

    result = BackupResult(
      file_name="",
      file_path="",
      file_size=0,
      checksum="",
      started_at=started.isoformat(),
      completed_at=completed.isoformat(),
      finished_at=completed.isoformat(),
      duration=duration,
      status="failed",
      type="files",
      message=f"Backup failed: {str(e)}"
    )

  response = send_backup(result)

  print(response)
  return response


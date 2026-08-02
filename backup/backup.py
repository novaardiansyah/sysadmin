from datetime import datetime
from pathlib import Path

from backup.zip import create_zip
from models.backup_result import BackupResult
from utils.checksum import sha256
from api.report import send_backup, store_job_report
from storage.r2 import upload_file
from config import BACKUP_OUTPUT

def run_backup_job(job: dict):
  job_id                 = job["id"]
  source_path            = job["source_path"]
  dest_dir               = job.get("destination_path") or BACKUP_OUTPUT
  expected_filename      = job.get("expected_filename")
  is_sync_cloud          = job.get("is_sync_cloud") if job.get("is_sync_cloud") is not None else True
  cloud_destination_path = job.get("cloud_destination_path")
  keep_local_raw         = job.get("keep_local_backup")
  keep_local_backup      = keep_local_raw.lower() not in ("false", "0") if isinstance(keep_local_raw, str) else (bool(keep_local_raw) if keep_local_raw is not None else True)

  started = datetime.now()

  try:
    dest_path = Path(dest_dir)
    dest_path.mkdir(parents=True, exist_ok=True)

    if expected_filename:
      filename = expected_filename[:-4] if expected_filename.endswith(".zip") else expected_filename
    else:
      filename = f"backup-{started.strftime('%Y%m%d-%H%M%S')}"

    destination = str(dest_path / filename)
    zip_file    = create_zip(source_path, destination)
    completed   = datetime.now()
    duration    = int((completed - started).total_seconds())
    file_size   = Path(zip_file).stat().st_size
    file_hash   = sha256(zip_file)

    if is_sync_cloud:
      file_name = Path(zip_file).name
      if cloud_destination_path:
        clean_path = cloud_destination_path.strip("/")
        object_key = f"{clean_path}/{file_name}" if clean_path else file_name
      else:
        object_key = file_name

      r2_status = upload_file(zip_file, object_key)
      if r2_status["success"]:
        message         = f"Backup completed successfully and uploaded to the cloud storage"
        cloud_file_path = object_key
        if not keep_local_backup:
          try:
            Path(zip_file).unlink(missing_ok=True)
          except Exception as e:
            print(f"Warning: Failed to delete local backup file: {e}")
      else:
        message         = f"Backup completed locally. (Cloud: {r2_status['message']})"
        cloud_file_path = None
    else:
      message         = "Backup completed locally. (Cloud sync disabled)"
      cloud_file_path = None

    result = BackupResult(
      file_name=Path(zip_file).name,
      file_path=zip_file,
      backup_job_id=job_id,
      cloud_file_path=cloud_file_path,
      file_size=file_size,
      checksum=file_hash,
      started_at=started.isoformat(),
      completed_at=completed.isoformat(),
      finished_at=completed.isoformat(),
      duration=duration,
      status="success",
      type="files",
      message=message
    )
  except Exception as e:
    completed = datetime.now()
    duration  = int((completed - started).total_seconds())

    result = BackupResult(
      file_name="",
      file_path="",
      backup_job_id=job_id,
      cloud_file_path=None,
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
    dest_path = Path(BACKUP_OUTPUT)
    dest_path.mkdir(parents=True, exist_ok=True)

    filename = f"backup-{started.strftime('%Y%m%d-%H%M%S')}"

    destination = str(dest_path / filename)
    zip_file    = create_zip(source_path, destination)
    completed   = datetime.now()
    duration    = int((completed - started).total_seconds())

    r2_status = upload_file(zip_file, Path(zip_file).name)
    if r2_status["success"]:
      message         = f"Backup completed successfully and uploaded to the cloud storage"
      cloud_file_path = Path(zip_file).name
    else:
      message         = f"Backup completed locally. (Cloud: {r2_status['message']})"
      cloud_file_path = None

    result = BackupResult(
      file_name=Path(zip_file).name,
      file_path=zip_file,
      cloud_file_path=cloud_file_path,
      file_size=Path(zip_file).stat().st_size,
      checksum=sha256(zip_file),
      started_at=started.isoformat(),
      completed_at=completed.isoformat(),
      finished_at=completed.isoformat(),
      duration=duration,
      status="success",
      type="files",
      message=message
    )
  except Exception as e:
    completed = datetime.now()
    duration  = int((completed - started).total_seconds())

    result = BackupResult(
      file_name="",
      file_path="",
      cloud_file_path=None,
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


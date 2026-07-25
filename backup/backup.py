from datetime import datetime
from pathlib import Path

from backup.zip import create_zip
from models.backup_result import BackupResult
from utils.checksum import sha256
from api.report import send_backup
from config import BACKUP_OUTPUT

def run_backup(source_path: str):
  started = datetime.now()

  try:
    filename = f"backup-{started.strftime('%Y%m%d-%H%M%S')}"

    destination = str(Path(BACKUP_OUTPUT) / filename)
    zip_file = create_zip(source_path, destination)
    completed = datetime.now()
    duration = int((completed - started).total_seconds())

    result = BackupResult(
      file_name=Path(zip_file).name,
      file_path=zip_file,
      file_size=Path(zip_file).stat().st_size,
      checksum=sha256(zip_file),
      started_at=started.isoformat(),
      completed_at=completed.isoformat(),
      duration=duration,
      status="success",
      type="files",
      message="Backup completed successfully"
    )
  except Exception as e:
    completed = datetime.now()
    duration = int((completed - started).total_seconds())

    result = BackupResult(
      file_name="",
      file_path="",
      file_size=0,
      checksum="",
      started_at=started.isoformat(),
      completed_at=completed.isoformat(),
      duration=duration,
      status="failed",
      type="files",
      message=f"Backup failed: {str(e)}"
    )

  response = send_backup(result)

  print(response)
  return response


from datetime import datetime
from pathlib import Path

from backup.zip import create_zip
from models.backup_result import BackupResult
from utils.checksum import sha256
from api.report import send_backup
from config import BACKUP_OUTPUT

def run_backup(source_path: str):
  started = datetime.now()
  filename = f"backup-{started.strftime('%Y%m%d-%H%M%S')}"

  destination = str(Path(BACKUP_OUTPUT) / filename)
  zip_file = create_zip(source_path, destination)
  completed = datetime.now()

  result = BackupResult(
    file_name=Path(zip_file).name,
    file_path=zip_file,
    file_size=Path(zip_file).stat().st_size,
    checksum=sha256(zip_file),
    started_at=started.isoformat(),
    completed_at=completed.isoformat(),
    duration=int((completed - started).total_seconds()),
    status="success",
    type="files",
    message=None
  )

  response = send_backup(result)

  print(response)

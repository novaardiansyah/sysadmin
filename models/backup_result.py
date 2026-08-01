from dataclasses import dataclass

@dataclass
class BackupResult:
  file_name: str
  file_path: str
  file_size: int
  checksum: str
  started_at: str
  completed_at: str
  duration: int
  status: str
  type: str
  backup_job_id: int | None = None
  cloud_file_path: str | None = None
  server_name: str | None = None
  message: str | None = None
  finished_at: str | None = None

  
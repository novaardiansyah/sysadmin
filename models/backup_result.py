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
  message: str | None = None
  finished_at: str | None = None
  
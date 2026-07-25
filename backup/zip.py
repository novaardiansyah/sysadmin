import shutil
from pathlib import Path

def create_zip(source_path: str, destination: str) -> str:
    dest_path = Path(destination)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    archive_path = shutil.make_archive(destination, "zip", source_path)
    return archive_path

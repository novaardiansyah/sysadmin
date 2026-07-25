import shutil
from datetime import datetime

shutil.make_archive(
  "backup-" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
  "zip",
  "./"
)

print("Backup created successfully!")

from api.report import check_schedule
from backup.backup import run_backup_job

def main():
  jobs = check_schedule()

  if not jobs:
    print("No backup schedules are due.")
    return

  for job in jobs:
    run_backup_job(job)

if __name__ == "__main__":
  main()

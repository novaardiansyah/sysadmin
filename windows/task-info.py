import subprocess

result = subprocess.run(["tasklist"], capture_output=True, text=True)

print(result.stdout)

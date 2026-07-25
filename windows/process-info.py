import psutil

for process in psutil.process_iter(["pid", "name"]):
    print(process.info)
    
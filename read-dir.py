from pathlib import Path

folder = Path("./")

for file in folder.iterdir():
    print(file.name)
import shutil
from pathlib import Path

source = Path("../example.txt")  # если запускаешь из папки directory_management
destination = Path("../folder1/example.txt")

if source.exists():
    shutil.move(str(source), str(destination))
    print("File moved.")
else:
    print("Source file does not exist.")
import shutil
import os
from pathlib import Path

source = Path("example.txt")
copy_file = Path("copy_example.txt")

# копирование
if source.exists():
    shutil.copy(source, copy_file)
    print("File copied.")

# удаление
if copy_file.exists():
    os.remove(copy_file)
    print("Copied file deleted.")
else:
    print("File not found.")
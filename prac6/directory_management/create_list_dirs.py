import os
from pathlib import Path

# os.mkdir()
if not os.path.exists("folder1"):
    os.mkdir("folder1")

# os.makedirs()
Path("folder1/subfolder").mkdir(parents=True, exist_ok=True)

print("Directories created.")

# текущая директория
print("Current directory:", os.getcwd())

# смена директории
os.chdir("folder1")
print("Changed directory:", os.getcwd())

# список файлов
print("Directory contents:", os.listdir())
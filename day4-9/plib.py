from pathlib import Path

# file_path = Path("data.txt")

# print(file_path.exists())
# print(file_path.name)
# print(file_path.suffix)
# print(file_path.parent)

folder = Path("hamza")
folder.mkdir(exist_ok=True)

file_path = folder / "employee.csv"

print(file_path)

file_path.write_text("Python")

print(file_path.read_text())

for file in folder.glob("*.csv"):
    print(file.name)
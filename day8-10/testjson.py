import json

with open("employee.json", "r") as file:
    data = json.load(file)


# print(data[0]["Name"])
# print(data[0]["Age"])
# print(data[0]["Designation"])

print(json.dumps(data, indent=4))
### CSV writer
# import csv

# employees = [
#     ["Patrick Jane", 40, "Consultant"],
#     ["Teressa Lisbon", 35, "CBI Agent"],
#     ["Kimbal Cho", 30, "CBI Agent"]
# ]

# with open("output.csv", "w", newline="") as file:
#     writer = csv.writer(file)
#     writer.writerow(["Name", "Age", "Designation"])
#     writer.writerows(employees)

### CSV with Pandas
import pandas as pd

df = pd.read_csv("output.csv")

print(df)

df.to_csv("employees.csv", index=False)
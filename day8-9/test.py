import json
import pandas as pd
from pathlib import Path

folder = Path("output")
folder.mkdir(exist_ok=True)

try:
    with open("employee.json", "r") as file:
        data = json.load(file)


    df = pd.DataFrame(data)
    high_sal = df[df["Salary"] > 30000]
    avg_sal = high_sal["Salary"].mean()

    df["Annual Salary"] = high_sal["Salary"] * 12

    print(high_sal)
    print(avg_sal)
    print(df["Annual Salary"])

    df.to_csv("output/high_sal_employee.csv", na_rep="NULL")
    df.to_json("output/high_sal_employee.json", orient="records", indent=4)

except FileNotFoundError:
    print("File not found")
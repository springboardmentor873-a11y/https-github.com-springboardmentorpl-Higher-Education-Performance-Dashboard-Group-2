import pandas as pd

QS_FILE = "2026_QS_World University_Rankings-selected-columns(1).csv"
WORLD_FILE = "2026_World University_Rankings(1).csv"

qs = pd.read_csv(QS_FILE)
world = pd.read_csv(WORLD_FILE)

qs["Data_Source"] = "QS"
world["Data_Source"] = "World"

raw = pd.concat([qs, world], ignore_index=True, sort=False)
raw.to_csv("university_raw_data.csv", index=False)

print("university_raw_data.csv created successfully")
print("Rows:", len(raw))
print("Columns:", len(raw.columns))

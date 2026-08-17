import pandas as pd

# Load QS and THE datasets
qs_data = pd.read_csv("Data/2026_QS.csv")
the_data = pd.read_csv("Data/2026_THE.csv")

# Display basic information
print("QS Dataset:")
print("Rows:", qs_data.shape[0])
print("Columns:", qs_data.shape[1])

print("\nTHE Dataset:")
print("Rows:", the_data.shape[0])
print("Columns:", the_data.shape[1])

# Display all column names of the QS dataset
# This helps us understand the structure of the QS data
print("\nQS Columns:")
print(qs_data.columns.tolist())


# Display all column names of the THE dataset
# This helps us identify common and different columns
# between QS and THE datasets
print("\nTHE Columns:")
print(the_data.columns.tolist())

# --------------------------------------------------
# Step 2: Merge QS and THE datasets
# --------------------------------------------------

# Rename common columns so both datasets have a similar structure
qs_data = qs_data.rename(columns={
    "Name": "University",
    "Country/Territory": "Country"
})

the_data = the_data.rename(columns={
    "Name": "University"
})

# Add a column to identify the ranking source
qs_data["Ranking_Source"] = "QS"
the_data["Ranking_Source"] = "THE"

# Combine both datasets row-wise
raw_data = pd.concat(
    [qs_data, the_data],
    ignore_index=True,
    sort=False
)

# Display the merged dataset information
print("\nMerged Dataset:")
print("Rows:", raw_data.shape[0])
print("Columns:", raw_data.shape[1])

# --------------------------------------------------
# Step 3: Save the merged raw dataset
# --------------------------------------------------

# Save the combined QS + THE dataset as a CSV file
# This file will be used later for data cleaning

raw_data.to_csv(
    "Output/university_raw_data.csv",
    index=False
)

print("\nRaw dataset saved successfully!")
print("File: Output/university_raw_data.csv")
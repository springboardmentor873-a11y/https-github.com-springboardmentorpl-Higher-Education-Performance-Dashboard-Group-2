import pandas as pd

# ---------------------------------------------------------
# MODULE 3: EDUCATION KPI ENGINEERING
# ---------------------------------------------------------
# This script loads the cleaned university dataset
# prepared in Module 2 and will be used to calculate
# education-related KPIs for Tableau analysis.
# ---------------------------------------------------------

# Load the cleaned dataset generated in Module 2
input_file = "Output/university_cleaned.csv"

data = pd.read_csv(input_file)

# Display basic information about the dataset
print("Dataset loaded successfully!")
print("Dataset Shape:", data.shape)

# Display all available columns
print("\nAvailable Columns:")
for column in data.columns:
    print(column)


    # ---------------------------------------------------------
# KPI 1: GLOBAL RANKING SCORE
# ---------------------------------------------------------
# QS and THE use different ranking systems.
# Both provide an overall score on a comparable 0-100 scale.
#
# If both scores are available, their average is used.
# If only one score is available, that score is used.
# ---------------------------------------------------------

data["Global_Ranking_Score"] = data[
    ["QS_Overall_Score", "THE_Overall_Score"]
].mean(axis=1, skipna=True)

# Display sample values for verification
print("\nGlobal Ranking Score calculated successfully!")

print(
    data[
        [
            "University",
            "QS_Overall_Score",
            "THE_Overall_Score",
            "Global_Ranking_Score"
        ]
    ].head(10)
)



# ---------------------------------------------------------
# KPI 2: RESEARCH IMPACT SCORE
# ---------------------------------------------------------
# Research impact is estimated using research-related
# indicators from both QS and THE.
#
# QS uses Citations per Faculty Score.
# THE uses Research Quality.
#
# If both values are available, their average is used.
# If only one value is available, that value is used.
# ---------------------------------------------------------

data["Research_Impact_Score"] = data[
    [
        "QS_Citations_per_Faculty_Score",
        "THE_Research_Quality"
    ]
].mean(axis=1, skipna=True)

# Display sample values for verification
print("\nResearch Impact Score calculated successfully!")

print(
    data[
        [
            "University",
            "QS_Citations_per_Faculty_Score",
            "THE_Research_Quality",
            "Research_Impact_Score"
        ]
    ].head(10)
)



# ---------------------------------------------------------
# CHECK: FACULTY-TO-STUDENT RATIO
# ---------------------------------------------------------
# THE provides the Students-to-Staff Ratio.
# We first inspect its values before creating the KPI,
# because this is a ratio and should not be directly
# averaged with the QS score.
# ---------------------------------------------------------

print("\nTHE Students-to-Staff Ratio:")
print(data["THE_Students_to_Staff_Ratio"].describe())

print("\nSample Faculty-to-Student Ratio Data:")

print(
    data[
        [
            "University",
            "THE_Students_to_Staff_Ratio"
        ]
    ].dropna().head(10)
)



# ---------------------------------------------------------
# KPI 3: FACULTY-TO-STUDENT RATIO
# ---------------------------------------------------------
# THE provides the Students-to-Staff Ratio.
# We convert it into a Faculty-to-Student Ratio by
# taking its reciprocal.
#
# Formula:
# Faculty-to-Student Ratio = 1 / Students-to-Staff Ratio
#
# A higher value indicates relatively more staff
# availability per student.
# ---------------------------------------------------------

data["Faculty_to_Student_Ratio"] = (
    1 / data["THE_Students_to_Staff_Ratio"]
)

# Display sample values for verification
print("\nFaculty-to-Student Ratio calculated successfully!")

print(
    data[
        [
            "University",
            "THE_Students_to_Staff_Ratio",
            "Faculty_to_Student_Ratio"
        ]
    ].dropna().head(10)
)




# ---------------------------------------------------------
# KPI 4: INTERNATIONAL STUDENT PERCENTAGE
# ---------------------------------------------------------
# THE provides the percentage of international students.
# We use this value directly as the KPI.
# ---------------------------------------------------------

data["International_Student_Percentage"] = (
    data["THE_International_Students_Percentage"]
)

print("\nInternational Student Percentage calculated successfully!")

print(
    data[
        [
            "University",
            "THE_International_Students_Percentage",
            "International_Student_Percentage"
        ]
    ].dropna().head(10)
)




# ---------------------------------------------------------
# KPI 5: ACADEMIC REPUTATION SCORE
# ---------------------------------------------------------
# QS provides the Academic Reputation Score directly.
# We use this score as the KPI.
# ---------------------------------------------------------

data["Academic_Reputation_Score"] = (
    data["QS_Academic_Reputation_Score"]
)

print("\nAcademic Reputation Score calculated successfully!")

print(
    data[
        [
            "University",
            "QS_Academic_Reputation_Score",
            "Academic_Reputation_Score"
        ]
    ].dropna().head(10)
)






# ---------------------------------------------------------
# KPI 6: RESEARCH PRODUCTIVITY INDEX
# ---------------------------------------------------------
# Research productivity is calculated using:
# 1. Research Environment
# 2. Research Quality
#
# If both values are available, their average is used.
# If only one value is available, that value is used.
# ---------------------------------------------------------

research_columns = [
    "THE_Research_Environment",
    "THE_Research_Quality"
]

data["Research_Productivity_Index"] = data[
    research_columns
].mean(axis=1, skipna=True)

# Display sample values for verification
print("\nResearch Productivity Index calculated successfully!")

print(
    data[
        [
            "University",
            "THE_Research_Environment",
            "THE_Research_Quality",
            "Research_Productivity_Index"
        ]
    ].dropna(
        subset=["Research_Productivity_Index"]
    ).head(10)
)


# ---------------------------------------------------------
# SAVE FINAL KPI DATASET
# ---------------------------------------------------------

output_file = "Output/university_final_dataset.xlsx"

data.to_excel(output_file, index=False)

print("\nFinal KPI dataset generated successfully!")
print("File:", output_file)
print("Final Dataset Shape:", data.shape)
print("\nKPI columns created:")
print([
    "Global_Ranking_Score",
    "Research_Impact_Score",
    "Faculty_to_Student_Ratio",
    "International_Student_Percentage",
    "Academic_Reputation_Score",
    "Research_Productivity_Index"
])

# & "C:\Program Files\Python314\python.exe" "generate_education_kpis.py"
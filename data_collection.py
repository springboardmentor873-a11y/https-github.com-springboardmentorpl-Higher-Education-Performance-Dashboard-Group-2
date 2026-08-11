import pandas as pd
import numpy as np
qs = pd.read_csv(r"C:\Users\pujit\Downloads\EduVision\data\QS_Rankings.csv")

the = pd.read_csv(r"C:\Users\pujit\Downloads\EduVision\data\THE_Rankings.csv")
print(qs.head())

print(the.head())
print(qs.columns)

print(the.columns)
qs.info()

the.info()
qs_columns = [
    "Name",
    "Country/Territory",
    "Region",
    "Rank",
    "Overall SCORE",
    "Academic Reputation SCORE",
    "Employer Reputation SCORE",
    "Faculty Student Ratio SCORE",
    "Citations per Faculty SCORE",
    "International Faculty  SCORE",
    "International Student SCORE",
    "International Students Diversity SCORE",
    "International Research Network SCORE",
    "Employment Outcomes SCORE",
    "Sustainability SCORE"
]
the_columns = [
    "Name",
    "Country",
    "Rank",
    "Overall Score",
    "Student Population",
    "Students to Staff Ratio",
    "International Students",
    "Female to Male Ratio",
    "Teaching",
    "Research Environment",
    "Research Quality",
    "Industry Impact",
    "International Outlook",
    "Year"
]
print(qs.columns.tolist())
print(the.columns.tolist())
qs_common = qs[qs_columns].rename(columns={
    "Country/Territory": "Country",
    "Rank": "QS Rank",
    "Overall SCORE": "QS Overall Score",
    "Academic Reputation SCORE": "QS Academic Reputation",
    "Employer Reputation SCORE": "QS Employer Reputation",
    "Faculty Student Ratio SCORE": "QS Faculty Student Ratio",
    "Citations per Faculty SCORE": "QS Citations per Faculty",
    "International Faculty  SCORE": "QS International Faculty",
    "International Student SCORE": "QS International Students",
    "International Students Diversity SCORE": "QS Student Diversity",
    "International Research Network SCORE": "QS Research Network",
    "Employment Outcomes SCORE": "QS Employment Outcomes",
    "Sustainability SCORE": "QS Sustainability"
})
the_common = the[the_columns].rename(columns={
    "Rank": "THE Rank",
    "Overall Score": "THE Overall Score",
    "Student Population": "THE Student Population",
    "Students to Staff Ratio": "THE Student Staff Ratio",
    "International Students": "THE International Students",
    "Female to Male Ratio": "THE Female Male Ratio",
    "Teaching": "THE Teaching",
    "Research Environment": "THE Research Environment",
    "Research Quality": "THE Research Quality",
    "Industry Impact": "THE Industry Impact",
    "International Outlook": "THE International Outlook"
})
qs_common["Name"] = qs_common["Name"].str.strip().str.lower()
the_common["Name"] = the_common["Name"].str.strip().str.lower()

qs_common["Country"] = qs_common["Country"].str.strip().str.lower()
the_common["Country"] = the_common["Country"].str.strip().str.lower()
merged = pd.merge(
    qs_common,
    the_common,
    on=["Name", "Country"],
    how="inner"
)
merged.head()
merged.to_csv(r"C:\Users\pujit\Downloads\EduVision\output\university_raw_data.csv", index=False)
merged.info()
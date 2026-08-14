import pandas as pd

# 1. Data Ingestion
df = pd.read_csv('data/interim/university_cleaned.csv')

# 2. Global Ranking Score
df['Global_Ranking_Score'] = (df['QS_Overall_Score'] + df['THE_Overall_Score']) / 2

# 3. Research Impact Score
df['Research_Impact_Score'] = (df['Citations_per_Faculty_Score'] + df['Research_Quality']) / 2

# 4. Faculty-to-Student Ratio
df['Faculty_to_Student_Ratio'] = df['Students_to_Staff_Ratio']

# 5. International Student Percentage
df['International_Student_Percentage'] = df['International_Student_Score']

# 6. Academic Reputation Score
df['Normalized_Academic_Reputation_Score'] = (df['Academic_Reputation_Score'] + df['Teaching']) / 2

# 7. Research Productivity Index
df['Research_Productivity_Index'] = (df['Research_Environment'] + df['Citations_per_Faculty_Score']) / 2

df.to_excel('data/final/university_final_dataset.xlsx', index=False)

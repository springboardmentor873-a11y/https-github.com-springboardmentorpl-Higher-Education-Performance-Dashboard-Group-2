import pandas as pd

df = pd.read_excel('data/merged_QS_THE_2026.xlsx')

cols_to_fix = ['Overall Score', 'Overall SCORE', 'Research Quality', 'Citations per Faculty SCORE',
               'Students to Staff Ratio', 'Faculty Student Ratio SCORE', 'International Students',
               'International Student SCORE', 'Academic Reputation SCORE', 'Employer Reputation SCORE',
               'Research Environment', 'Industry Impact']

for col in cols_to_fix:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df['Global_Ranking_Score'] = df[['Overall Score', 'Overall SCORE']].mean(axis=1)

df['Research_Impact_Score'] = df[['Research Quality', 'Citations per Faculty SCORE']].mean(axis=1)

df['Faculty_to_Student_Ratio'] = df[['Students to Staff Ratio', 'Faculty Student Ratio SCORE']].mean(axis=1)

df['International_Student_Percentage'] = df[['International Students', 'International Student SCORE']].mean(axis=1)

df['Academic_Reputation_Score'] = df[['Academic Reputation SCORE', 'Employer Reputation SCORE']].mean(axis=1)

df['Research_Productivity_Index'] = df[['Research Environment', 'Industry Impact']].mean(axis=1)

df.to_excel('data/university_final_dataset.xlsx', index=False)

print(df[['Global_Ranking_Score', 'Research_Impact_Score', 'Faculty_to_Student_Ratio', 'International_Student_Percentage', 'Academic_Reputation_Score', 'Research_Productivity_Index']].head())

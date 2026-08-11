import pandas as pd

# 1. Data Ingestion
qs = pd.read_csv('2026 QS World University Rankings.csv')
the = pd.read_csv('THE World University Rankings 2016-2026.csv')

# 2. Year Pre-filtering
the = the[the['Year'] == 2026]

# 3. Target Schema Alignment (Renaming)
qs = qs.rename(columns={
    '2026 Rank': 'Rank_QS',
    'Previous Rank': 'Previous_Rank',
    'Institution Name': 'Name',
    'Region': 'Region',
    'Size': 'Size',
    'Focus': 'Focus',
    'Research': 'Research',
    'Status': 'Status',
    'AR SCORE': 'Academic_Reputation_Score',
    'AR RANK': 'Academic_Reputation_Rank',
    'ER SCORE': 'Employer_Reputation_Score',
    'ER RANK': 'Employer_Reputation_Rank',
    'FSR SCORE': 'Faculty_Student_Ratio_Score',
    'FSR RANK': 'Faculty_Student_Ratio_Rank',
    'CPF SCORE': 'Citations_per_Faculty_Score',
    'CPF RANK': 'Citations_per_Faculty_Rank',
    'IFR SCORE': 'International_Faculty_Score',
    'IFR RANK': 'International_Faculty_Rank',
    'ISR SCORE': 'International_Student_Score',
    'ISR RANK': 'International_Student_Rank',
    'ISD SCORE': 'International_Students_Diversity_Score',
    'ISD RANK': 'International_Students_Diversity_Rank',
    'IRN SCORE': 'International_Research_Network_Score',
    'IRN RANK': 'International_Research_Network_Rank',
    'EO SCORE': 'Employment_Outcomes_Score',
    'EO RANK': 'Employment_Outcomes_Rank',
    'SUS SCORE': 'Sustainability_Score',
    'SUS RANK': 'Sustainability_Rank',
    'Overall SCORE': 'QS_Overall_Score'
})

the = the.rename(columns={
    'Rank': 'Rank_THE',
    'Name': 'Name',
    'Country': 'Country',
    'Student Population': 'Student_Population',
    'Students to Staff Ratio': 'Students_to_Staff_Ratio',
    'International Students': 'International_Students',
    'Female to Male Ratio': 'Female_to_Male_Ratio',
    'Overall Score': 'THE_Overall_Score',
    'Teaching': 'Teaching',
    'Research Environment': 'Research_Environment',
    'Research Quality': 'Research_Quality',
    'Industry Impact': 'Industry_Impact',
    'International Outlook': 'International_Outlook',
    'Year': 'Year'
})

# 4. Basic university name standardizing for merging
qs['Name'] = qs['Name'].str.lower().str.strip()
the['Name'] = the['Name'].str.lower().str.strip()

# 5. Dataset Integration (Merge)
merged_data = pd.merge(qs, the, on='Name', how='inner')

# 6. Export to CSV (Retain all raw attributes)
merged_data.to_csv('university_raw_data.csv', index=False)

# 7. Completeness Check
completeness = (merged_data.notnull().sum().sum() / merged_data.size) * 100
print("Dataset completeness: " + str(round(completeness, 2)) + "%")

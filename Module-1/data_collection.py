import pandas as pd

qs=pd.read_csv("2026_QS_World University_Rankings.csv")
the=pd.read_excel("THE World University Rankings 2026.xlsx")

qs["Name"]=qs["Name"].str.strip()
the["Name"]=the["Name"].str.strip()
qs["Country/Territory"]=qs["Country/Territory"].str.strip()
the["Country"]=the["Country"].str.strip()

merge_df=pd.merge(qs, the, left_on=["Name", "Country/Territory"], right_on=["Name", "Country"], how="left", suffixes=["_QS", "_THE"])
merge_df.to_csv("merged_university_rankings.csv", index=False)

print("merged successfully")
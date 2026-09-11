import pandas as pd

df=pd.read_csv("cleaned_university_rankings.csv")

df["Global_Ranking_Score"]=((df["QS_Overall_Score"]+df["THE_Overall_Score"])/2).round(2)

df["Research_Impact_Score"]=((df["Citations_per_Faculty_Score"]+df["Research_Environment"]+
                             df["Research_Quality"]+df["International_Research_Network_Score"])/4).round(2)

df["Faculty_to_Student_Ratio"]=df["Faculty_Student_Ratio_Score"]

df["International_Student_Percentage"]=(df["International_Students"]*100).round(2)

df["Academic_Reputation_Score"]=df["Academic_reputation_score"]

df["Research_Productivity_Index"]=((df["Research_Environment"]+df["Research_Quality"])/2).round(2)

df.drop(columns=["Faculty_Student_Ratio_Score","Academic_reputation_score"],inplace=True)

df.to_csv("university_final_dataset.csv", index=False)

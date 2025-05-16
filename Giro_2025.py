# Giro d'Italia 2025 - Teams and Riders
# Data analysis - Python Pandas training exercise

# Original data source: https://en.wikipedia.org/wiki/List_of_teams_and_cyclists_in_the_2025_Giro_d%27Italia
# The tables were copied from Wikipedia webpage into Excel files, formatted and then saved as CSV files.

# This Python code should be run in interactive mode (VS Code - Jupyter Interactive Window / Jupyter Notebook / ...).

import pandas as pd

df = pd.read_csv(r"M:\Pandas\Giro_2025.csv", delimiter=";")
df_teams = pd.read_csv(r"M:\Pandas\Giro_2025_Teams.csv", delimiter=";")

df
df_teams


# 1. Total number of the riders (rows)
print(f"Total number of the riders: {df.shape[0]}")  # Result: 184


# 2. Average age of all riders
print(f"Average age of all riders: {df['Age'].mean().round(2)}")  # Result: 28.17


# 3. Number of riders by Nationality
# a) Table
df_gr1a = (
    df.groupby(by="Nationality")
    .size()
    .to_frame("Nationality_Count")
    .sort_values(by=["Nationality_Count", "Nationality"], ascending=[False, True])
    .reset_index()
)
df_gr1a

# b) Graph (needs reverse order of the table above)
df_gr1b = df_gr1a.sort_values(by=["Nationality_Count", "Nationality"], ascending=[True, False]).reset_index(drop=True)
df_gr1b
df_gr1b.plot(kind="barh", x="Nationality", y="Nationality_Count", title="Giro d'Italia 2025 - Number of riders by Nationality")


# 4. Average age by the Teams
# a) Table
df_gr2a = df.groupby(by="Team")["Age"].mean().round(2).to_frame("Average_Age").sort_values(by=["Average_Age", "Team"]).reset_index()
df_gr2a

# b) Graph (needs reverse order of the table above)
df_gr2b = df_gr2a.sort_values(by=["Average_Age", "Team"], ascending=[False, False]).reset_index(drop=True)
df_gr2b
df_gr2b.plot(kind="barh", x="Team", y="Average_Age", xlim=(24, 32), title="Giro d'Italia 2025 - Average age by the Teams")


# 5. Count of the Riders by Age groups
# a) Table
df_gr3a = df.groupby(by="Age").size().to_frame("Count_of_Riders").reset_index()
df_gr3a

# Fill the missing Age groups with 0
age_list = range(df_gr3a["Age"].min(), df_gr3a["Age"].max() + 1)
df_gr3a = df_gr3a.set_index("Age").reindex(age_list).fillna(0).reset_index()
df_gr3a["Count_of_Riders"] = df_gr3a["Count_of_Riders"].astype(int)
df_gr3a

# b) Graph
df_gr3a.plot(kind="bar", x="Age", y="Count_of_Riders", ylim=(0, 25), title="Giro d'Italia 2025 - Count of the Riders by Age groups")


# 6. Team Leaders
# The Start numbers of the Team Leaders are ending with 1 - i.e. 1, 11, 21, ..., 221
# a) Table - Team Leaders by Start numbers
df_ldr = df[df["Nr"].isin(range(1, int(df.shape[0] / 8 * 10), 10))].sort_values(by="Nr").reset_index(drop=True)
df_ldr

df_ldr["Age"].median()
df_ldr["Age"].mode()

df_ldr = df_ldr.merge(df_teams, on="Team")
df_ldr = df_ldr.assign(Nr_Name_Code=df_ldr["Nr"].astype(str) + " " + df_ldr["Name"] + " (" + df_ldr["Code"] + ")")

# b) Table - Team Leaders by Age and Start numbers
df_ldr_age_asc = df_ldr.sort_values(by=["Age", "Nr"]).reset_index(drop=True)
df_ldr_age_asc[["Nr", "Name", "Nationality", "Team", "Age"]]

# c) Graph - Team Leaders by Age and Start numbers
df_ldr_age_desc = df_ldr.sort_values(by=["Age", "Nr"], ascending=[False, False]).reset_index(drop=True)
df_ldr_age_desc
df_ldr_age_desc.plot(kind="barh", x="Nr_Name_Code", y="Age", xlim=(20, 36), title="Giro d'Italia 2025 - Team Leaders by Age and Start numbers")

# d) Table - Team Leaders - Count by Age groups
df_ldr_age_gr = df_ldr.groupby(by="Age").size().to_frame("Team_Leaders_Count").reset_index()
df_ldr_age_gr

# Fill the missing Age groups with 0
age_list_ldr = range(df_ldr_age_gr["Age"].min(), df_ldr_age_gr["Age"].max() + 1)
df_ldr_age_gr = df_ldr_age_gr.set_index("Age").reindex(age_list_ldr).fillna(0).reset_index()
df_ldr_age_gr["Team_Leaders_Count"] = df_ldr_age_gr["Team_Leaders_Count"].astype(int)
df_ldr_age_gr

# e) Graph - Team Leaders - Count by Age groups
df_ldr_age_gr.plot(kind="bar", x="Age", y="Team_Leaders_Count", ylim=(0, 6), title="Giro d'Italia 2025 - Team Leaders - Count by Age groups")

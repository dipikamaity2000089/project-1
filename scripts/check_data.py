import pandas as pd
df = pd.read_csv("data/cleaned_hospital_events.csv")
print("Dataset loaded successfully!")
print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])
print("\nColumn names:")
print(df.columns.tolist())
print("\nMissing values in each column:")
print(df.isnull().sum())
print("\nFirst 5 rows:")
print(df.head())
print("\nDataset Summary:")
print("Total cases:", df["Case_ID"].nunique())
print("Total activities:", df["Activity_Name"].nunique())
print("\nActivity frequency:")
print(df["Activity_Name"].value_counts())
print("\nCases per activity:")
print(df.groupby("Activity_Name")["Case_ID"].nunique())
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df = df.sort_values(["Case_ID", "Timestamp"])
df["Time_Difference_Minutes"] = (
    df.groupby("Case_ID")["Timestamp"]
    .diff()
    .dt.total_seconds() / 60
)
print("\nTime between activities (minutes):")
print(df[["Case_ID", "Activity_Name", "Time_Difference_Minutes"]].head(15))
print("\nAverage time between activities:")
average_time = df.groupby("Activity_Name")[
    "Time_Difference_Minutes"
].mean()
print(average_time.round(2))
import pandas as pd
from pathlib import Path
data_path = Path("Data/clinical_transition_analysis.csv")
output_path = Path("Data/clinical_key_findings.txt")
df = pd.read_csv(data_path)
df = df.sort_values(
    "Average_Interval_Minutes",
    ascending=False
)
findings = []
findings.append("CAREFLOW - CLINICAL PERFORMANCE FINDINGS")
findings.append("=" * 45)
findings.append("")
findings.append(
    f"Total activity transitions analysed: {len(df)}"
)
findings.append(
    f"Total observed transitions: {df['Transition_Frequency'].sum()}"
)
if not df.empty:
    highest = df.iloc[0]

    findings.append("")
    findings.append("TRANSITION WITH THE HIGHEST AVERAGE INTERVAL")
    findings.append(
        f"Transition: {highest['Activity_Name']} -> "
        f"{highest['Next_Activity']}"
    )
    findings.append(
        f"Average interval: "
        f"{highest['Average_Interval_Minutes']:.2f} minutes"
    )
    findings.append(
        f"Observed frequency: "
        f"{int(highest['Transition_Frequency'])}"
    )
    most_common = df.loc[
        df["Transition_Frequency"].idxmax()
    ]
    findings.append("")
    findings.append("MOST FREQUENT TRANSITION")
    findings.append(
        f"Transition: {most_common['Activity_Name']} -> "
        f"{most_common['Next_Activity']}"
    )
    findings.append(
        f"Frequency: {int(most_common['Transition_Frequency'])}"
    )
findings.append("")
findings.append("INTERPRETATION")
findings.append(
    "These results describe intervals between consecutive events."
)
findings.append(
    "They do not independently confirm actual patient waiting times "
    "or clinical bottlenecks."
)
output_path.write_text("\n".join(findings), encoding="utf-8")
print("\n".join(findings))
print(f"\nFindings saved to: {output_path}")
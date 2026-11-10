"""
CareFlow: large simulated ER event log generator.
Usage: python generate_event_log.py [n_cases] [seed]    -> data/careflow_event_log_large.csv
Planted inefficiencies (so process mining has something real to find):
  * ~40% of patients are sent back to Triage after the doctor (rework loop)
  * Doctor D04 sends back far more patients (~65%)
  * Longer waits during the 10:00-13:00 rush
  * X-Ray and Lab Test have slow handoffs to Treatment
"""
import sys, random, os
import pandas as pd
from datetime import datetime, timedelta

N    = int(sys.argv[1]) if len(sys.argv) > 1 else 500
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 42
random.seed(SEED)

DOCTORS = ["D01", "D02", "D03", "D04", "D05", "D06"]
AGES    = ["0-17", "18-39", "40-59", "60+"]
AGE_W   = [0.15, 0.30, 0.30, 0.25]
START   = datetime(2026, 10, 1)
DAYS    = 14

def dur(lo, hi):                       # service time in minutes
    return random.randint(lo, hi)

def wait(lo, hi, rush):                # waiting time, inflated during rush hour
    w = random.randint(lo, hi)
    return int(w * 1.5) if rush else w

rows = []
for i in range(1, N + 1):
    cid  = f"P{i:04d}"
    doc  = random.choice(DOCTORS)
    age  = random.choices(AGES, AGE_W)[0]
    tri  = random.choices([1, 2, 3, 4, 5], [0.05, 0.15, 0.40, 0.28, 0.12])[0]
    day  = START + timedelta(days=random.randrange(DAYS))
    t    = day + timedelta(hours=8, minutes=random.randint(0, 11 * 60))   # arrivals 08:00-19:00
    loop_p = 0.65 if doc == "D04" else 0.35
    loop   = random.random() < loop_p
    diag   = random.choices(["Lab Test", "X-Ray"], [0.55, 0.45])[0]

    def add(act, lo, hi, wlo, whi):
        global t
        rush = 10 <= t.hour < 13
        t += timedelta(minutes=wait(wlo, whi, rush)) if rows and rows[-1][0] == cid else timedelta(0)
        s = t; t = s + timedelta(minutes=dur(lo, hi))
        rows.append((cid, act, s, s, t, doc, age, tri))

    add("Registration", 5, 10, 0, 0)
    add("Triage", 6, 15, 5, 25)
    add("Doctor Consultation", 12, 25, 8, 35)
    if loop:
        add("Triage", 6, 14, 5, 25)
    if diag == "X-Ray":
        add("X-Ray", 10, 20, 5, 30)
        add("Treatment", 15, 30, 12, 30)
    else:
        add("Lab Test", 15, 30, 8, 25)
        add("Treatment", 15, 30, 12, 28)
    add("Discharge", 5, 10, 5, 28)

df = pd.DataFrame(rows, columns=["Case_ID", "Activity_Name", "Timestamp", "Activity_Start_Time",
                                 "Activity_End_Time", "Doctor_ID", "Age_Group", "Triage_Level"])
df = df.sort_values(["Case_ID", "Activity_Start_Time"])
os.makedirs("data", exist_ok=True)
df.to_csv("data/careflow_event_log_large.csv", index=False, date_format="%Y-%m-%d %H:%M:%S")
print(f"{df.Case_ID.nunique()} cases, {len(df)} events -> data/careflow_event_log_large.csv")

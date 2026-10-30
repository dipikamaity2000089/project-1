"""
CareFlow - Process Discovery, Bottleneck Analysis, Conformance Checking.
Run:  pip install pandas pm4py graphviz matplotlib   (and install Graphviz binary)
      python careflow_analysis.py event_log.csv
PM4Py is used when installed; otherwise a pandas fallback produces identical numbers.
"""
import sys, os
import pandas as pd
import graphviz

SRC = sys.argv[1] if len(sys.argv) > 1 else "event_log.csv"
OUT = "output"
os.makedirs(OUT, exist_ok=True)

# ---------- 1. Load + validate ----------
df = pd.read_csv(SRC, parse_dates=["Timestamp", "Activity_Start_Time", "Activity_End_Time"])
assert df.isna().sum().sum() == 0, "Missing values found"
assert (df.Activity_End_Time >= df.Activity_Start_Time).all(), "End before start"
df = df.sort_values(["Case_ID", "Activity_Start_Time"]).reset_index(drop=True)
df["step"] = df.groupby("Case_ID").cumcount() + 1
df["duration_min"] = (df.Activity_End_Time - df.Activity_Start_Time).dt.total_seconds() / 60

# ---------- 2. Process discovery (As-Is map) ----------
try:
    import pm4py
    log = pm4py.format_dataframe(df, case_id="Case_ID", activity_key="Activity_Name",
                                 timestamp_key="Activity_Start_Time")
    dfg, start_acts, end_acts = pm4py.discover_dfg(log)
    pm4py.save_vis_dfg(dfg, start_acts, end_acts, f"{OUT}/pm4py_dfg.png")
    net, im, fm = pm4py.discover_petri_net_inductive(log)
    pm4py.save_vis_petri_net(net, im, fm, f"{OUT}/pm4py_petri_net.png")
    print("PM4Py discovery done")
except ImportError:
    print("pm4py not installed -> using pandas fallback for discovery")

# ---------- 3. Transitions (directly-follows) + bottlenecks ----------
nxt = df.groupby("Case_ID").shift(-1)
tr = pd.DataFrame({
    "case": df.Case_ID,
    "from": df.Activity_Name,
    "to": nxt.Activity_Name,
    "wait_min": (nxt.Activity_Start_Time - df.Activity_End_Time).dt.total_seconds() / 60,
}).dropna()

edges = (tr.groupby(["from", "to"])
           .agg(cases=("case", "nunique"), freq=("case", "size"),
                avg_wait_min=("wait_min", "mean"), max_wait_min=("wait_min", "max"))
           .round(1).reset_index().sort_values("avg_wait_min", ascending=False))
edges.to_csv(f"{OUT}/transition_bottlenecks.csv", index=False)

acts = (df.groupby("Activity_Name")
          .agg(events=("Case_ID", "size"), avg_service_min=("duration_min", "mean"))
          .round(1).reset_index())
inbound_wait = tr.groupby("to").wait_min.mean().round(1).rename("avg_wait_before_min")
acts = acts.merge(inbound_wait, left_on="Activity_Name", right_index=True, how="left")
acts.to_csv(f"{OUT}/activity_stats.csv", index=False)

# ---------- 4. Conformance checking ----------
# Ideal (mandated) journey: Registration > Triage > Doctor Consultation >
# (Lab Test | X-Ray) > Treatment > Discharge
IDEAL = ["Registration", "Triage", "Doctor Consultation", None, "Treatment", "Discharge"]
DIAG = {"Lab Test", "X-Ray"}

def check(seq):
    issues = []
    expected = [a if a else "<Lab Test|X-Ray>" for a in IDEAL]
    core = [a for a in seq]
    if core.count("Triage") > 1:
        issues.append("Rework: returned to Triage")
    cleaned, seen_triage = [], False
    for a in core:           # remove repeated triage for the ideal-order check
        if a == "Triage" and seen_triage and "Doctor Consultation" in cleaned:
            continue
        if a == "Triage": seen_triage = True
        cleaned.append(a)
    ok = (len(cleaned) == 6 and cleaned[:3] == IDEAL[:3] and cleaned[3] in DIAG
          and cleaned[4:] == IDEAL[4:])
    if not ok:
        issues.append("Deviates from ideal sequence")
    return issues

variants = df.groupby("Case_ID").Activity_Name.apply(list)
conf = pd.DataFrame({"case": variants.index,
                     "path": [" > ".join(v) for v in variants],
                     "issues": [check(v) for v in variants]})
conf["compliant"] = conf.issues.apply(len) == 0
conf["issues"] = conf.issues.apply("; ".join)

case_t = df.groupby("Case_ID").agg(start=("Activity_Start_Time", "min"), end=("Activity_End_Time", "max"))
conf = conf.merge(((case_t.end - case_t.start).dt.total_seconds() / 60).round(0).rename("total_los_min"),
                  left_on="case", right_index=True)
conf.to_csv(f"{OUT}/conformance.csv", index=False)

# ---------- 5. Headline KPIs ----------
rework = conf.issues.str.contains("Rework").mean()
los_re = conf[conf.issues.str.contains("Rework")].total_los_min.mean()
los_ok = conf[~conf.issues.str.contains("Rework")].total_los_min.mean()
kpis = pd.DataFrame([
    ("cases", len(conf)),
    ("avg_length_of_stay_min", round(conf.total_los_min.mean(), 1)),
    ("pct_cases_looping_back_to_triage", round(rework * 100, 1)),
    ("avg_los_with_loop_min", round(los_re, 1)),
    ("avg_los_without_loop_min", round(los_ok, 1)),
    ("pct_conformant", round(conf.compliant.mean() * 100, 1)),
], columns=["kpi", "value"])
kpis.to_csv(f"{OUT}/kpis.csv", index=False)

# ---------- 6. Process map (Spaghetti / DFG) with wait times ----------
g = graphviz.Digraph("careflow", format="png")
g.attr(rankdir="LR", dpi="160", fontname="Helvetica", bgcolor="white")
g.attr("node", shape="box", style="rounded,filled", fillcolor="#E8F0FE", fontname="Helvetica")
for _, r in acts.iterrows():
    g.node(r.Activity_Name, f"{r.Activity_Name}\n{r.events} events | svc {r.avg_service_min:.0f} min")
mx = edges.freq.max()
for _, r in edges.iterrows():
    hot = r.avg_wait_min >= 20
    g.edge(r["from"], r["to"], label=f"n={r.freq} | wait {r.avg_wait_min:.0f}m",
           penwidth=str(1 + 4 * r.freq / mx), color="#D93025" if hot else "#5F6368",
           fontcolor="#D93025" if hot else "#3C4043", fontsize="10")
g.render(f"{OUT}/process_map", cleanup=True)

print(kpis.to_string(index=False)); print(); print(edges.to_string(index=False))

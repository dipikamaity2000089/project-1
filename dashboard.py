import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="CareFlow | Patient Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# FORMAL CORPORATE THEME
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #F3F5F8;
    color: #263445;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

h1, h2, h3 {
    color: #17324D !important;
    font-weight: 650;
}

p, label {
    color: #526477;
}

[data-testid="stSidebar"] {
    background-color: #E8EDF3;
    border-right: 1px solid #D5DDE6;
}

[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #DCE3EB;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 7px rgba(25, 45, 70, 0.05);
}

[data-testid="stMetricLabel"] {
    color: #53677D;
}

[data-testid="stMetricValue"] {
    color: #17324D;
    font-weight: 700;
}

.stButton button,
.stDownloadButton button {
    background-color: #173F5F;
    color: white;
    border-radius: 7px;
    border: none;
}

.stButton button:hover,
.stDownloadButton button:hover {
    background-color: #246B83;
    color: white;
}

hr {
    border-color: #DCE3EB;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("data/cleaned_hospital_events.csv")

    required_columns = [
        "Case_ID",
        "Activity_Name",
        "Timestamp",
        "Activity_Start_Time",
        "Activity_End_Time"
    ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    for col in [
        "Timestamp",
        "Activity_Start_Time",
        "Activity_End_Time"
    ]:
        df[col] = pd.to_datetime(
            df[col],
            errors="coerce"
        )

    df = df.dropna(
        subset=["Case_ID", "Activity_Name", "Timestamp"]
    )

    df = df.sort_values(
        ["Case_ID", "Timestamp"]
    ).copy()

    df["Duration_Minutes"] = (
        df["Activity_End_Time"] -
        df["Activity_Start_Time"]
    ).dt.total_seconds() / 60

    return df


try:
    df = load_data()

except Exception as error:
    st.error(f"Unable to load dataset: {error}")
    st.stop()

if df.empty:
    st.error("The dataset contains no valid event records.")
    st.stop()

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("# 🏥 CareFlow")
st.markdown(
    "### Patient Journey & Healthcare Process Analytics"
)

st.caption(
    "Hospital Workflow Monitoring | Synthetic Educational Dataset"
)

st.divider()

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.title("Dashboard Controls")

st.sidebar.caption(
    "Filter the data to explore patient journeys."
)

patients = sorted(
    df["Case_ID"].astype(str).unique().tolist()
)

patient_options = ["All Patients"] + patients

selected_patient = st.sidebar.selectbox(
    "Select Patient",
    patient_options
)

activities = sorted(
    df["Activity_Name"].astype(str).unique().tolist()
)

activity_options = ["All Activities"] + activities

selected_activity = st.sidebar.selectbox(
    "Select Activity",
    activity_options
)

# --------------------------------------------------
# FILTER DATA
# --------------------------------------------------

filtered = df.copy()

if selected_patient != "All Patients":

    filtered = filtered[
        filtered["Case_ID"].astype(str) == selected_patient
    ]

if selected_activity != "All Activities":

    filtered = filtered[
        filtered["Activity_Name"] == selected_activity
    ]

# --------------------------------------------------
# PATIENT JOURNEY CALCULATION
# --------------------------------------------------

journeys = (
    df.groupby("Case_ID")
    .agg(
        First_Event=("Timestamp", "min"),
        Last_Event=("Timestamp", "max")
    )
)

journeys["Journey_Minutes"] = (
    journeys["Last_Event"] -
    journeys["First_Event"]
).dt.total_seconds() / 60

if selected_patient != "All Patients":

    journeys = journeys.loc[
        journeys.index.astype(str) == selected_patient
    ]

average_journey = (
    journeys["Journey_Minutes"].mean()
    if not journeys.empty else 0
)

valid_durations = filtered[
    filtered["Duration_Minutes"] >= 0
]["Duration_Minutes"]

average_duration = (
    valid_durations.mean()
    if not valid_durations.empty else 0
)

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

st.subheader("Performance Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Patients",
    filtered["Case_ID"].nunique()
)

col2.metric(
    "Total Events",
    len(filtered)
)

col3.metric(
    "Average Journey",
    f"{average_journey:.1f} min"
)

col4.metric(
    "Average Activity Duration",
    f"{average_duration:.1f} min"
)

st.divider()

# --------------------------------------------------
# ACTIVITY DISTRIBUTION
# --------------------------------------------------

st.subheader("Activity Analysis")

left, right = st.columns(2)

with left:

    st.markdown("#### Activity Distribution")

    activity_counts = (
        filtered["Activity_Name"]
        .value_counts()
        .rename_axis("Activity")
        .reset_index(name="Event Count")
    )

    fig1 = px.bar(
        activity_counts,
        x="Activity",
        y="Event Count",
        text="Event Count",
        color_discrete_sequence=["#315B7D"]
    )

    fig1.update_traces(
        textposition="outside"
    )

    fig1.update_layout(
        height=400,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font_color="#263445",
        xaxis_title="Hospital Activity",
        yaxis_title="Number of Events",
        margin=dict(l=30, r=20, t=30, b=70)
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with right:

    st.markdown("#### Average Activity Duration")

    duration_data = (
        filtered[
            filtered["Duration_Minutes"] >= 0
        ]
        .groupby("Activity_Name")["Duration_Minutes"]
        .mean()
        .reset_index()
    )

    duration_data.columns = [
        "Activity",
        "Average Minutes"
    ]

    fig2 = px.bar(
        duration_data,
        x="Activity",
        y="Average Minutes",
        text_auto=".1f",
        color_discrete_sequence=["#548C83"]
    )

    fig2.update_traces(
        textposition="outside"
    )

    fig2.update_layout(
        height=400,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font_color="#263445",
        xaxis_title="Hospital Activity",
        yaxis_title="Average Duration (Minutes)",
        margin=dict(l=30, r=20, t=30, b=70)
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.divider()

#

# --------------------------------------------------
# PATIENT JOURNEY TIMELINE
# --------------------------------------------------

st.subheader("Patient Journey Timeline")

timeline_data = filtered.dropna(
    subset=[
        "Activity_Start_Time",
        "Activity_End_Time"
    ]
).copy()

timeline_data = timeline_data[
    timeline_data["Activity_End_Time"] >=
    timeline_data["Activity_Start_Time"]
]

if not timeline_data.empty:

    fig4 = px.timeline(
        timeline_data,
        x_start="Activity_Start_Time",
        x_end="Activity_End_Time",
        y="Case_ID",
        color="Activity_Name",
        hover_data=[
            "Activity_Name",
            "Duration_Minutes"
        ],
        color_discrete_sequence=px.colors.qualitative.Safe
    )

    fig4.update_yaxes(
        autorange="reversed"
    )

    fig4.update_layout(
        height=max(
            420,
            55 * timeline_data["Case_ID"].nunique()
        ),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font_color="#263445",
        xaxis_title="Activity Time",
        yaxis_title="Patient",
        margin=dict(
            l=30,
            r=30,
            t=40,
            b=30
        )
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

else:

    st.info(
        "No valid activity start and end times are available."
    )

st.divider()
 
# --------------------------------------------------
# PATIENT JOURNEY SUMMARY
# --------------------------------------------------

st.subheader("Patient Journey Summary")

summary = (
    df.groupby("Case_ID")
    .agg(
        Activity_Count=("Activity_Name", "count"),
        First_Activity=("Timestamp", "min"),
        Last_Activity=("Timestamp", "max")
    )
    .reset_index()
)

summary["Journey_Minutes"] = (
    summary["Last_Activity"] -
    summary["First_Activity"]
).dt.total_seconds() / 60

if selected_patient != "All Patients":

    summary = summary[
        summary["Case_ID"].astype(str) == selected_patient
    ]

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# DOWNLOAD REPORTS
# --------------------------------------------------

st.subheader("Download Reports")

download1, download2 = st.columns(2)

with download1:

    st.download_button(
        "Download Patient Summary",
        data=summary.to_csv(
            index=False
        ).encode("utf-8"),
        file_name="careflow_patient_summary.csv",
        mime="text/csv",
        use_container_width=True
    )

with download2:

    st.download_button(
        "Download Filtered Events",
        data=filtered.to_csv(
            index=False
        ).encode("utf-8"),
        file_name="careflow_filtered_events.csv",
        mime="text/csv",
        use_container_width=True
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "CareFlow | Healthcare Process Analytics | "
    "Synthetic Educational Dataset"
)
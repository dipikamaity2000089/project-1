import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="CareFlow Analytics",
    page_icon="🏥",
    layout="wide"
)

DATA_PATH = Path("data/cleaned_hospital_events.csv")

st.markdown("""
<style>
.stApp {
    background-color: #F3F6F9;
    color: #243447;
}

[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #DCE4EC;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 2rem 1.2rem;
}

[data-testid="stSidebar"] h1 {
    color: #20364B;
    font-size: 23px;
    font-weight: 700;
}

[data-testid="stSidebar"] label {
    color: #42566B;
    font-size: 14px;
    font-weight: 600;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #F7F9FC;
    border: 1px solid #DCE4EC;
    border-radius: 8px;
    min-height: 42px;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div:hover {
    border-color: #159A9C;
}

[data-testid="stSidebar"] .stButton button {
    background-color: #20364B;
    color: white;
    border: none;
    border-radius: 8px;
    min-height: 40px;
    font-weight: 600;
    width: 100%;
}

[data-testid="stSidebar"] .stButton button:hover {
    background-color: #159A9C;
    color: white;
}

h1, h2, h3 {
    color: #20364B;
}

.metric-card {
    background-color: #FFFFFF;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #DCE4EC;
    box-shadow: 0 2px 7px rgba(20, 40, 60, 0.06);
    text-align: center;
}

.metric-label {
    color: #62758A;
    font-size: 14px;
}

.metric-value {
    color: #20364B;
    font-size: 27px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    required = [
        "Case_ID",
        "Activity_Name",
        "Timestamp",
        "Activity_Start_Time",
        "Activity_End_Time"
    ]

    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(
            "Missing required columns: " + ", ".join(missing)
        )

    for col in [
        "Timestamp",
        "Activity_Start_Time",
        "Activity_End_Time"
    ]:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    df = df.dropna(
        subset=["Case_ID", "Activity_Name", "Timestamp"]
    )

    df["Activity_Duration"] = (
        df["Activity_End_Time"] - df["Activity_Start_Time"]
    ).dt.total_seconds() / 60

    df.loc[
        df["Activity_Duration"] < 0,
        "Activity_Duration"
    ] = None

    return df


try:
    data = load_data()
except Exception as error:
    st.error(f"Unable to load the dataset: {error}")
    st.stop()


# Header
st.title("🏥 CareFlow Patient Journey Dashboard")

st.caption(
    "Hospital Workflow Analytics | Synthetic Dataset"
)

st.markdown("---")


# Sidebar filters
def reset_filters():
    st.session_state["patient_filter"] = "All"
    st.session_state["activity_filter"] = "All"


st.sidebar.title("Dashboard Filters")
st.sidebar.caption("Customize your patient data view")

st.sidebar.markdown("---")

patients = sorted(data["Case_ID"].astype(str).unique())
activities = sorted(data["Activity_Name"].unique())

selected_patient = st.sidebar.selectbox(
    "Select Patient",
    ["All"] + patients,
    key="patient_filter"
)

selected_activity = st.sidebar.selectbox(
    "Select Activity",
    ["All"] + activities,
    key="activity_filter"
)

st.sidebar.markdown("---")

st.sidebar.button(
    "Reset Filters",
    on_click=reset_filters,
    use_container_width=True
)

st.sidebar.caption("CareFlow Analytics | Data Filters")

filtered = data.copy()

if selected_patient != "All":
    filtered = filtered[
        filtered["Case_ID"].astype(str) == selected_patient
    ]

if selected_activity != "All":
    filtered = filtered[
        filtered["Activity_Name"] == selected_activity
    ]


# KPI calculations
total_patients = filtered["Case_ID"].nunique()
total_events = len(filtered)

patient_journey = (
    filtered.groupby("Case_ID")
    .agg(
        First_Activity=("Activity_Start_Time", "min"),
        Last_Activity=("Activity_End_Time", "max")
    )
)

patient_journey["Journey_Minutes"] = (
    patient_journey["Last_Activity"]
    - patient_journey["First_Activity"]
).dt.total_seconds() / 60

patient_journey.loc[
    patient_journey["Journey_Minutes"] < 0,
    "Journey_Minutes"
] = None

avg_journey = patient_journey["Journey_Minutes"].mean()
avg_activity = filtered["Activity_Duration"].mean()

avg_journey = 0 if pd.isna(avg_journey) else avg_journey
avg_activity = 0 if pd.isna(avg_activity) else avg_activity


# KPI cards
st.subheader("Overall Performance")

c1, c2, c3, c4 = st.columns(4)

metrics = [
    ("Total Patients", total_patients),
    ("Total Events", total_events),
    ("Average Journey", f"{avg_journey:.1f} min"),
    ("Average Activity Duration", f"{avg_activity:.1f} min")
]

for col, (label, value) in zip([c1, c2, c3, c4], metrics):
    with col:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("---")


# Activity analysis
st.subheader("Activity Analysis")

left, right = st.columns(2)

with left:
    st.markdown("### Activity Distribution")

    activity_counts = (
        filtered["Activity_Name"]
        .value_counts()
        .reset_index()
    )

    activity_counts.columns = ["Activity", "Count"]

    if not activity_counts.empty:
        fig = px.bar(
            activity_counts,
            x="Activity",
            y="Count",
            color="Count",
            color_continuous_scale="Blues",
            text="Count"
        )

        fig.update_layout(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font_color="#243447",
            showlegend=False,
            coloraxis_showscale=False,
            xaxis_title="Activity",
            yaxis_title="Number of Events"
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No activity data available.")


with right:
    st.markdown("### Average Activity Duration")

    duration_data = (
        filtered.dropna(subset=["Activity_Duration"])
        .groupby("Activity_Name")["Activity_Duration"]
        .mean()
        .reset_index()
    )

    duration_data.columns = ["Activity", "Average Minutes"]

    if not duration_data.empty:
        fig = px.bar(
            duration_data,
            x="Activity",
            y="Average Minutes",
            color="Average Minutes",
            color_continuous_scale="Teal",
            text_auto=".1f"
        )

        fig.update_layout(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font_color="#243447",
            showlegend=False,
            coloraxis_showscale=False,
            xaxis_title="Activity",
            yaxis_title="Average Duration (minutes)"
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No valid activity duration data available.")


# Workflow bottleneck alerts
st.markdown("---")
st.subheader("🚨 Workflow Bottleneck Alerts")

st.caption(
    "Highlights activities and patient journeys with durations "
    "above the average in the selected dataset."
)

alert_left, alert_right = st.columns(2)

valid_durations = filtered.dropna(
    subset=["Activity_Duration"]
)

with alert_left:
    st.markdown("### Activities Above Average Duration")

    if not valid_durations.empty:
        overall_avg_duration = valid_durations["Activity_Duration"].mean()

        activity_alerts = (
            valid_durations.groupby("Activity_Name")
            ["Activity_Duration"]
            .mean()
            .reset_index()
        )

        activity_alerts.columns = [
            "Activity",
            "Average Duration (Minutes)"
        ]

        activity_alerts = activity_alerts[
            activity_alerts["Average Duration (Minutes)"]
            > overall_avg_duration
        ].sort_values(
            "Average Duration (Minutes)",
            ascending=False
        )

        if not activity_alerts.empty:
            st.warning(
                f"{len(activity_alerts)} activities have an average "
                f"duration above {overall_avg_duration:.1f} minutes."
            )

            st.dataframe(
                activity_alerts.round(2),
                use_container_width=True,
                hide_index=True
            )

            longest_activity = activity_alerts.iloc[0]

            st.metric(
                "Longest Average Activity",
                longest_activity["Activity"],
                f"{longest_activity['Average Duration (Minutes)']:.1f} min"
            )
        else:
            st.success(
                "No activities are above the overall average duration."
            )
    else:
        st.info("No valid activity duration data available.")


with alert_right:
    st.markdown("### Patient Journey Delay Indicators")

    valid_journeys = patient_journey.dropna(
        subset=["Journey_Minutes"]
    )

    if not valid_journeys.empty:
        average_patient_journey = (
            valid_journeys["Journey_Minutes"].mean()
        )

        delayed_patients = valid_journeys[
            valid_journeys["Journey_Minutes"]
            > average_patient_journey
        ].sort_values(
            "Journey_Minutes",
            ascending=False
        )

        if not delayed_patients.empty:
            st.warning(
                f"{len(delayed_patients)} patient journeys are "
                f"longer than the average of "
                f"{average_patient_journey:.1f} minutes."
            )

            st.dataframe(
                delayed_patients[
                    ["Journey_Minutes"]
                ].round(2),
                use_container_width=True
            )

            longest_patient = delayed_patients["Journey_Minutes"].idxmax()

            st.metric(
                "Longest Patient Journey",
                str(longest_patient),
                f"{delayed_patients.loc[longest_patient, 'Journey_Minutes']:.1f} min"
            )
        else:
            st.success("No above-average patient journeys found.")
    else:
        st.info("Patient journey durations are unavailable.")

st.caption(
    "These are duration-based indicators, not confirmed clinical "
    "or operational bottlenecks."
)


# Hospital workflow performance radar
st.markdown("---")
st.subheader("🎯 Hospital Workflow Performance")

st.caption(
    "Compare hospital activities based on event frequency "
    "and average duration. Scores are normalized to a 0–100 scale."
)

radar_data = (
    filtered.dropna(subset=["Activity_Duration"])
    .groupby("Activity_Name")
    .agg(
        Event_Count=("Activity_Name", "count"),
        Average_Duration=("Activity_Duration", "mean")
    )
    .reset_index()
)

if not radar_data.empty:
    max_events = radar_data["Event_Count"].max()
    max_duration = radar_data["Average_Duration"].max()

    radar_data["Event Score"] = (
        radar_data["Event_Count"] / max_events * 100
        if max_events > 0 else 0
    )

    radar_data["Duration Score"] = (
        radar_data["Average_Duration"] / max_duration * 100
        if max_duration > 0 else 0
    )

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=radar_data["Event Score"].tolist()
        + [radar_data["Event Score"].iloc[0]],
        theta=radar_data["Activity_Name"].tolist()
        + [radar_data["Activity_Name"].iloc[0]],
        fill="toself",
        name="Event Frequency"
    ))

    fig.add_trace(go.Scatterpolar(
        r=radar_data["Duration Score"].tolist()
        + [radar_data["Duration Score"].iloc[0]],
        theta=radar_data["Activity_Name"].tolist()
        + [radar_data["Activity_Name"].iloc[0]],
        fill="toself",
        name="Average Duration"
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            ),
            bgcolor="#FFFFFF"
        ),
        paper_bgcolor="#FFFFFF",
        font_color="#243447",
        height=550,
        legend=dict(
            orientation="h",
            y=-0.15
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("View workflow performance details"):
        st.dataframe(
            radar_data.round(2),
            use_container_width=True,
            hide_index=True
        )
else:
    st.info("Not enough valid activity duration data for this chart.")


# Patient journey timeline
st.markdown("---")
st.subheader("Patient Journey Timeline")

timeline_data = filtered.dropna(
    subset=["Activity_Start_Time", "Activity_End_Time"]
).copy()

timeline_data = timeline_data[
    timeline_data["Activity_End_Time"]
    >= timeline_data["Activity_Start_Time"]
]

if not timeline_data.empty:
    timeline_data["Patient"] = (
        timeline_data["Case_ID"].astype(str)
    )

    fig = px.timeline(
        timeline_data,
        x_start="Activity_Start_Time",
        x_end="Activity_End_Time",
        y="Patient",
        color="Activity_Name",
        hover_data=["Activity_Name"],
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig.update_yaxes(autorange="reversed")

    fig.update_layout(
        height=550,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font_color="#243447",
        xaxis_title="Timeline",
        yaxis_title="Patient ID",
        legend_title="Activity"
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No valid patient timeline data available.")


st.markdown("---")


# Patient journey summary
st.subheader("Patient Journey Summary")

summary = (
    filtered.groupby("Case_ID")
    .agg(
        Activity_Count=("Activity_Name", "count"),
        First_Activity=("Activity_Start_Time", "min"),
        Last_Activity=("Activity_End_Time", "max")
    )
    .reset_index()
)

summary["Total_Journey_Minutes"] = (
    summary["Last_Activity"] - summary["First_Activity"]
).dt.total_seconds() / 60

summary["Total_Journey_Minutes"] = (
    summary["Total_Journey_Minutes"].round(1)
)

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)


# Download patient journey summary
st.download_button(
    label="Download Patient Journey Summary",
    data=summary.to_csv(index=False).encode("utf-8"),
    file_name="careflow_patient_journey_summary.csv",
    mime="text/csv"
)


# Download filtered patient data
st.markdown("---")

st.download_button(
    label="Download Filtered Patient Data",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="careflow_filtered_data.csv",
    mime="text/csv"
)

st.markdown("---")

st.caption(
    "CareFlow Analytics | Academic Project | Synthetic Hospital Data"
)
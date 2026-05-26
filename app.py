import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Teen Mental Health Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("Teen_Mental_Health_Dataset.csv")
    df["depression_label"] = df["depression_label"].map({0: "No Depression", 1: "Depression"})
    return df

df = load_data()

st.title("🧠 Teen Mental Health Dataset Dashboard")

# --- Sidebar Filters ---
with st.sidebar:
    st.header("Filters")
    gender = st.multiselect("Gender", df["gender"].unique(), default=df["gender"].unique())
    platform = st.multiselect("Platform", df["platform_usage"].unique(), default=df["platform_usage"].unique())
    age_range = st.slider("Age Range", int(df["age"].min()), int(df["age"].max()), (int(df["age"].min()), int(df["age"].max())))

filtered = df[
    df["gender"].isin(gender) &
    df["platform_usage"].isin(platform) &
    df["age"].between(*age_range)
]

# --- KPI Row ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Records", len(filtered))
col2.metric("Avg Sleep Hours", f"{filtered['sleep_hours'].mean():.1f} hrs")
col3.metric("Avg Stress Level", f"{filtered['stress_level'].mean():.1f}")
col4.metric("Depression Rate", f"{(filtered['depression_label'] == 'Depression').mean() * 100:.1f}%")

st.divider()

# --- Row 1 ---
c1, c2 = st.columns(2)

with c1:
    fig = px.histogram(filtered, x="daily_social_media_hours", color="gender",
                       nbins=20, title="Daily Social Media Hours by Gender", barmode="overlay")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.box(filtered, x="platform_usage", y="stress_level", color="platform_usage",
                 title="Stress Level by Platform")
    st.plotly_chart(fig, use_container_width=True)

# --- Row 2 ---
c3, c4 = st.columns(2)

with c3:
    fig = px.scatter(filtered, x="daily_social_media_hours", y="sleep_hours",
                     color="depression_label", hover_data=["age", "platform_usage"],
                     title="Social Media Hours vs Sleep Hours")
    st.plotly_chart(fig, use_container_width=True)

with c4:
    fig = px.pie(filtered, names="platform_usage", title="Platform Usage Distribution")
    st.plotly_chart(fig, use_container_width=True)

# --- Row 3 ---
c5, c6 = st.columns(2)

with c5:
    fig = px.bar(filtered.groupby("social_interaction_level")[["anxiety_level", "depression_label"]]
                 .agg(anxiety_level=("anxiety_level", "mean"),
                      depression_rate=("depression_label", lambda x: (x == "Depression").mean() * 100))
                 .reset_index(),
                 x="social_interaction_level", y=["anxiety_level", "depression_rate"],
                 barmode="group", title="Anxiety & Depression Rate by Social Interaction Level")
    st.plotly_chart(fig, use_container_width=True)

with c6:
    corr = filtered[["daily_social_media_hours", "sleep_hours", "stress_level",
                      "anxiety_level", "addiction_level", "academic_performance", "physical_activity"]].corr()
    fig = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r",
                    title="Correlation Heatmap")
    st.plotly_chart(fig, use_container_width=True)

# --- Raw Data ---
with st.expander("View Raw Data"):
    st.dataframe(filtered, use_container_width=True)

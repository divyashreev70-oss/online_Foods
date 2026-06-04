import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="🍽️ Indian Food Analytics Dashboard",
    page_icon="🍽️",
    layout="wide"
)

# ==================================================
# LOAD DATA
# ==================================================
@st.cache_data
def load_data():

    possible_files = [
        "onlinefoods.csv",
        "data/onlinefoods.csv"
    ]

    for file in possible_files:
        if os.path.exists(file):

            df = pd.read_csv(file)

            if "Unnamed: 12" in df.columns:
                df.drop("Unnamed: 12", axis=1, inplace=True)

            return df

    st.error("""
    ❌ Dataset not found.

    Please upload:
    onlinefoods.csv

    OR place it inside:
    data/onlinefoods.csv
    """)

    st.stop()

df = load_data()

# ==================================================
# TITLE
# ==================================================
st.title("🍽️ Indian Food Analytics Dashboard")
st.markdown("### Explore Customer Food Ordering Behaviour")

# ==================================================
# SHOW DATA
# ==================================================
st.subheader("Dataset Preview")
st.dataframe(df.head())

# ==================================================
# SIDEBAR FILTERS
# ==================================================
st.sidebar.header("Filters")

gender = st.sidebar.multiselect(
    "Select Gender",
    df["Gender"].unique(),
    default=df["Gender"].unique()
)

filtered_df = df[df["Gender"].isin(gender)]

# ==================================================
# KPI SECTION
# ==================================================
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Customers", len(filtered_df))

with col2:
    st.metric(
        "Average Age",
        round(filtered_df["Age"].mean(), 1)
    )

with col3:
    st.metric(
        "Average Family Size",
        round(filtered_df["Family size"].mean(), 1)
    )

# ==================================================
# GENDER ANALYSIS
# ==================================================
st.subheader("Gender Distribution")

gender_count = filtered_df["Gender"].value_counts()

fig = px.pie(
    values=gender_count.values,
    names=gender_count.index,
    title="Gender Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# ==================================================
# AGE DISTRIBUTION
# ==================================================
st.subheader("Age Distribution")

fig = px.histogram(
    filtered_df,
    x="Age",
    nbins=20,
    title="Age Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# ==================================================
# OCCUPATION ANALYSIS
# ==================================================
st.subheader("Occupation Analysis")

occupation_df = (
    filtered_df["Occupation"]
    .value_counts()
    .reset_index()
)

occupation_df.columns = ["Occupation", "Count"]

fig = px.bar(
    occupation_df,
    x="Occupation",
    y="Count",
    color="Count"
)

st.plotly_chart(fig, use_container_width=True)

# ==================================================
# FEEDBACK ANALYSIS
# ==================================================
if "Feedback" in filtered_df.columns:

    st.subheader("Feedback Analysis")

    feedback_df = (
        filtered_df["Feedback"]
        .value_counts()
        .reset_index()
    )

    feedback_df.columns = ["Feedback", "Count"]

    fig = px.bar(
        feedback_df,
        x="Feedback",
        y="Count",
        color="Feedback"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# DOWNLOAD
# ==================================================
csv = filtered_df.to_csv(index=False)

st.download_button(
    "⬇ Download Filtered Data",
    csv,
    "filtered_food_data.csv",
    "text/csv"
)

# ==================================================
# FOOTER
# ==================================================
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")

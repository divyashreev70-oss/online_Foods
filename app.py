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
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>
.main {
    background-color: #f8f9fa;
}

.metric-box {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():

    possible_paths = [
        "onlinefoods.csv",
        "data/onlinefoods.csv"
    ]

    for path in possible_paths:
        if os.path.exists(path):

            df = pd.read_csv(path)

            if "Unnamed: 12" in df.columns:
                df.drop(columns=["Unnamed: 12"], inplace=True)

            return df

    st.error("""
    ❌ Dataset not found.

    Please upload:

    onlinefoods.csv

    OR

    data/onlinefoods.csv
    """)

    st.stop()

df = load_data()

# ==================================================
# TITLE
# ==================================================

st.title("🍽️ Indian Food Analytics Dashboard")
st.markdown("### Explore Food Ordering Behavior Using Data Analytics")

# ==================================================
# SIDEBAR FILTERS
# ==================================================

st.sidebar.header("Filters")

gender = st.sidebar.multiselect(
    "Gender",
    df["Gender"].dropna().unique(),
    default=df["Gender"].dropna().unique()
)

occupation = st.sidebar.multiselect(
    "Occupation",
    df["Occupation"].dropna().unique(),
    default=df["Occupation"].dropna().unique()
)

feedback = st.sidebar.multiselect(
    "Feedback",
    df["Feedback"].dropna().unique(),
    default=df["Feedback"].dropna().unique()
)

filtered_df = df[
    (df["Gender"].isin(gender))
    &
    (df["Occupation"].isin(occupation))
    &
    (df["Feedback"].isin(feedback))
]

# ==================================================
# KPI SECTION
# ==================================================

st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Customers", len(filtered_df))

with col2:
    st.metric(
        "Average Age",
        round(filtered_df["Age"].mean(), 1)
        if len(filtered_df) > 0 else 0
    )

with col3:
    st.metric(
        "Average Family Size",
        round(filtered_df["Family size"].mean(), 1)
        if len(filtered_df) > 0 else 0
    )

with col4:

    if len(filtered_df) > 0:
        positive = len(
            filtered_df[
                filtered_df["Feedback"]
                .astype(str)
                .str.contains("Positive",
                              case=False,
                              na=False)
            ]
        )

        positive_rate = (positive / len(filtered_df)) * 100

    else:
        positive_rate = 0

    st.metric(
        "Positive Feedback %",
        f"{positive_rate:.1f}%"
    )

st.divider()

# ==================================================
# GENDER ANALYSIS
# ==================================================

col1, col2 = st.columns(2)

with col1:

    gender_count = filtered_df["Gender"].value_counts()

    fig = px.pie(
        values=gender_count.values,
        names=gender_count.index,
        title="Gender Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

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

st.subheader("💼 Occupation Analysis")

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

st.subheader("😊 Feedback Analysis")

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
# EDUCATION ANALYSIS
# ==================================================

st.subheader("🎓 Education Analysis")

edu_df = (
    filtered_df["Educational Qualifications"]
    .value_counts()
    .reset_index()
)

edu_df.columns = ["Education", "Count"]

fig = px.bar(
    edu_df,
    x="Education",
    y="Count",
    color="Count"
)

st.plotly_chart(fig, use_container_width=True)

# ==================================================
# MAP ANALYSIS
# ==================================================

if "latitude" in filtered_df.columns and "longitude" in filtered_df.columns:

    st.subheader("📍 Customer Locations")

    fig = px.scatter_mapbox(
        filtered_df,
        lat="latitude",
        lon="longitude",
        zoom=10,
        height=500,
        hover_name="Occupation"
    )

    fig.update_layout(
        mapbox_style="open-street-map"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# CORRELATION HEATMAP
# ==================================================

st.subheader("📈 Correlation Analysis")

numeric_df = filtered_df.select_dtypes(include="number")

if len(numeric_df.columns) > 1:

    corr = numeric_df.corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# BUSINESS INSIGHTS
# ==================================================

st.subheader("🧠 Business Insights")

if len(filtered_df) > 0:

    top_occ = (
        filtered_df["Occupation"]
        .value_counts()
        .idxmax()
    )

    top_edu = (
        filtered_df["Educational Qualifications"]
        .value_counts()
        .idxmax()
    )

    st.success(f"""
    • Most customers are **{top_occ}**

    • Most common education level is **{top_edu}**

    • Positive feedback rate is **{positive_rate:.1f}%**

    • Younger customers dominate food delivery usage.

    • Customer behavior can help businesses target promotions.
    """)

# ==================================================
# DATA TABLE
# ==================================================

st.subheader("📄 Dataset Preview")

st.dataframe(filtered_df)

# ==================================================
# DOWNLOAD DATA
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
st.markdown("Made with ❤️ using Streamlit and Plotly")

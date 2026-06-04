import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="🍽️ Indian Food Analytics Dashboard",
    page_icon="🍽️",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main {
    background-color:#f8f9fa;
}

.metric-card {
    background-color:white;
    padding:15px;
    border-radius:15px;
    box-shadow:0px 0px 10px rgba(0,0,0,0.1);
}

h1,h2,h3{
color:#ff4b4b;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🍽️ Indian Food Analytics Dashboard")
st.markdown("### Explore Customer Food Ordering Behaviour using Data Analytics")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("onlinefoods.csv")

    if "Unnamed: 12" in df.columns:
        df.drop("Unnamed: 12", axis=1, inplace=True)

    return df

df = load_data()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("🔍 Filters")

gender = st.sidebar.multiselect(
    "Select Gender",
    df["Gender"].unique(),
    default=df["Gender"].unique()
)

occupation = st.sidebar.multiselect(
    "Select Occupation",
    df["Occupation"].unique(),
    default=df["Occupation"].unique()
)

feedback = st.sidebar.multiselect(
    "Select Feedback",
    df["Feedback"].unique(),
    default=df["Feedback"].unique()
)

filtered_df = df[
    (df["Gender"].isin(gender))
    &
    (df["Occupation"].isin(occupation))
    &
    (df["Feedback"].isin(feedback))
]

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Customers", len(filtered_df))

with col2:
    st.metric("Average Age", round(filtered_df["Age"].mean(),1))

with col3:
    st.metric("Average Family Size",
              round(filtered_df["Family size"].mean(),1))

with col4:
    positive_rate = (
        len(filtered_df[filtered_df["Feedback"].str.contains("Positive")])
        / len(filtered_df)
    ) * 100

    st.metric("Positive Feedback %",
              f"{positive_rate:.1f}%")

st.divider()

# --------------------------------------------------
# CHARTS ROW 1
# --------------------------------------------------

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

# --------------------------------------------------
# CHARTS ROW 2
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    occupation_count = (
        filtered_df["Occupation"]
        .value_counts()
        .reset_index()
    )

    occupation_count.columns = ["Occupation","Count"]

    fig = px.bar(
        occupation_count,
        x="Occupation",
        y="Count",
        color="Count",
        title="Occupation Analysis"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    income_count = (
        filtered_df["Monthly Income"]
        .value_counts()
        .reset_index()
    )

    income_count.columns = ["Income","Count"]

    fig = px.bar(
        income_count,
        x="Income",
        y="Count",
        color="Count",
        title="Income Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# FEEDBACK ANALYSIS
# --------------------------------------------------

st.subheader("😊 Customer Feedback Analysis")

feedback_count = (
    filtered_df["Feedback"]
    .value_counts()
    .reset_index()
)

feedback_count.columns = ["Feedback","Count"]

fig = px.bar(
    feedback_count,
    x="Feedback",
    y="Count",
    color="Feedback",
    title="Feedback Overview"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# EDUCATION ANALYSIS
# --------------------------------------------------

st.subheader("🎓 Education Analysis")

edu = (
    filtered_df["Educational Qualifications"]
    .value_counts()
    .reset_index()
)

edu.columns = ["Education","Count"]

fig = px.bar(
    edu,
    x="Education",
    y="Count",
    color="Count",
    title="Educational Qualification Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# FAMILY SIZE ANALYSIS
# --------------------------------------------------

st.subheader("👨‍👩‍👧 Family Size Distribution")

fig = px.box(
    filtered_df,
    y="Family size",
    title="Family Size Spread"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# LOCATION ANALYSIS
# --------------------------------------------------

st.subheader("📍 Customer Locations")

fig = px.scatter_mapbox(
    filtered_df,
    lat="latitude",
    lon="longitude",
    hover_name="Occupation",
    zoom=10,
    height=500
)

fig.update_layout(
    mapbox_style="open-street-map"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# CORRELATION
# --------------------------------------------------

st.subheader("📈 Correlation Analysis")

numeric_df = filtered_df.select_dtypes(include="number")

corr = numeric_df.corr()

fig = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="RdBu_r"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# INSIGHTS
# --------------------------------------------------

st.subheader("🧠 AI Style Business Insights")

avg_age = filtered_df["Age"].mean()

top_occupation = (
    filtered_df["Occupation"]
    .value_counts()
    .idxmax()
)

top_education = (
    filtered_df["Educational Qualifications"]
    .value_counts()
    .idxmax()
)

st.success(f"""
### Key Insights

✔ Average customer age is **{avg_age:.1f} years**

✔ Most customers are **{top_occupation}**

✔ Majority educational qualification is **{top_education}**

✔ Positive feedback percentage is **{positive_rate:.1f}%**

✔ Customer concentration can be observed around Bangalore urban areas.

✔ Students form the major customer segment.

✔ Food delivery businesses should focus on younger demographics.
""")

# --------------------------------------------------
# DATA TABLE
# --------------------------------------------------

st.subheader("📄 Dataset Preview")

st.dataframe(filtered_df)

# --------------------------------------------------
# DOWNLOAD
# --------------------------------------------------

csv = filtered_df.to_csv(index=False)

st.download_button(
    "⬇ Download Filtered Data",
    csv,
    "filtered_food_data.csv",
    "text/csv"
)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")
st.markdown(
    "Developed with ❤️ using Streamlit, Plotly & Python"
)

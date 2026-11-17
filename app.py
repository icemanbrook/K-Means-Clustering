
import streamlit as st
import pandas as pd
from pathlib import Path

from src.preprocessing import preprocess_data
from src.clustering import (
    scale_features,
    calculate_elbow,
    perform_clustering,
    get_cluster_profiles
)

from src.visualization import (
    make_elbow_chart,
    make_cluster_chart,
    make_profile_chart
)


# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="CustomerIQ",
    page_icon="📊",
    layout="wide"
)


# ---------------- CUSTOM STYLING ----------------

st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }

    .block-container {
        padding-top: 2rem;
    }

    h1 {
        color: #60a5fa;
    }

    div[data-testid="stMetric"] {
        background-color: #1c2333;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #30394d;
    }
</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------

st.sidebar.title("📊 CustomerIQ")

st.sidebar.caption("Customer Segmentation System")

st.sidebar.divider()

uploaded_file = st.sidebar.file_uploader(
    "Upload Customer Dataset",
    type=["xlsx", "xls", "csv"]
)

st.sidebar.subheader("Clustering Settings")

n_clusters = st.sidebar.slider(
    "Number of Clusters (K)",
    min_value=2,
    max_value=8,
    value=4
)

st.sidebar.info(
    "CustomerIQ uses K-Means clustering "
    "to identify purchasing behaviour."
)


# ---------------- HEADER ----------------

st.title("CustomerIQ")
st.subheader("Customer Segmentation & Analytics")

st.markdown(
    "Discover customer purchasing patterns using "
    "Machine Learning and K-Means Clustering."
)

st.divider()


# ---------------- DATASET LOADING ----------------

default_file = Path("data/Online_Retail.xlsx")

if uploaded_file is not None:
    data_source = uploaded_file

elif default_file.exists():
    data_source = default_file

else:
    data_source = None


if data_source is None:

    st.warning("Please upload a customer dataset to begin.")

    st.stop()


# ---------------- PROCESSING ----------------

try:

    with st.spinner("Processing customer data..."):

        customer_data, cleaned_data, cleaning_info = (
            preprocess_data(data_source)
        )

        X_scaled, scaler = scale_features(customer_data)

        k_values, inertia_values = calculate_elbow(X_scaled)

        clustered_data, model, scaler = perform_clustering(
            customer_data,
            n_clusters=n_clusters
        )

        profiles = get_cluster_profiles(clustered_data)

except Exception as error:

    st.error(f"Unable to process dataset: {error}")
    st.stop()


# ---------------- KPI CARDS ----------------

st.markdown("### Business Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Customers",
    f"{len(clustered_data):,}"
)

col2.metric(
    "Customer Segments",
    n_clusters
)

col3.metric(
    "Valid Transactions",
    f"{cleaning_info['Cleaned Records']:,}"
)

col4.metric(
    "Total Revenue",
    f"£{customer_data['TotalSpending'].sum():,.2f}"
)


st.divider()


# ---------------- VISUALIZATIONS ----------------

st.markdown("### Customer Analytics")

tab1, tab2, tab3 = st.tabs([
    "Customer Segmentation",
    "Cluster Distribution",
    "Elbow Method"
])


with tab1:

    st.plotly_chart(
        make_cluster_chart(clustered_data),
        use_container_width=True
    )

    st.caption(
        "Each point represents a customer. "
        "Colours represent the assigned K-Means cluster."
    )


with tab2:

    st.plotly_chart(
        make_profile_chart(profiles),
        use_container_width=True
    )

    st.markdown("#### Customer Cluster Profiles")

    st.dataframe(
        profiles.round(2),
        use_container_width=True,
        hide_index=True
    )


with tab3:

    st.plotly_chart(
        make_elbow_chart(k_values, inertia_values),
        use_container_width=True
    )

    st.caption(
        "The Elbow Method compares inertia values "
        "for different numbers of clusters."
    )


# ---------------- SEGMENT INSIGHTS ----------------

st.divider()

st.markdown("### Customer Segment Insights")

for _, row in profiles.iterrows():

    cluster = int(row["Cluster"])

    st.markdown(f"**Cluster {cluster}**")

    st.write(
        f"""
        - Customers: {int(row['CustomerCount']):,}
        - Average Spending: £{row['AverageSpending']:,.2f}
        - Average Purchase Frequency: {row['AverageFrequency']:.2f}
        - Average Transaction Value: £{row['AverageTransactionValue']:,.2f}
        """
    )

    st.divider()


# ---------------- DATA PREVIEW ----------------

with st.expander("View Customer Dataset"):

    st.dataframe(
        clustered_data,
        use_container_width=True,
        hide_index=True
    )


with st.expander("View Data Cleaning Summary"):

    st.json(cleaning_info)


# ---------------- DOWNLOAD RESULTS ----------------

st.markdown("### Export Results")

csv_data = clustered_data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Segmented Customer Data",
    data=csv_data,
    file_name="customer_segmentation_results.csv",
    mime="text/csv"
)


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "CustomerIQ | Data Mining Project | "
    "Customer Segmentation using K-Means Clustering"
)


import plotly.express as px


def make_elbow_chart(k_values, inertia_values):

    fig = px.line(
        x=k_values,
        y=inertia_values,
        markers=True,
        title="Elbow Method",
        labels={
            "x": "Number of Clusters (K)",
            "y": "Inertia (WCSS)"
        }
    )

    fig.update_layout(template="plotly_dark")
    return fig


def make_cluster_chart(data):

    plot_data = data.copy()
    plot_data["Cluster"] = plot_data["Cluster"].astype(str)

    fig = px.scatter(
        plot_data,
        x="TotalSpending",
        y="PurchaseFrequency",
        color="Cluster",
        hover_data=[
            "CustomerID",
            "AverageTransactionValue"
        ],
        log_x=True,
        title="Customer Segmentation",
        labels={
            "TotalSpending": "Total Spending (£)",
            "PurchaseFrequency": "Purchase Frequency",
            "Cluster": "Customer Segment"
        }
    )

    fig.update_layout(template="plotly_dark")
    return fig


def make_profile_chart(profiles):

    fig = px.bar(
        profiles,
        x="Cluster",
        y="CustomerCount",
        color="Cluster",
        title="Customers in Each Segment",
        labels={
            "Cluster": "Customer Segment",
            "CustomerCount": "Number of Customers"
        }
    )

    fig.update_layout(template="plotly_dark")
    return fig

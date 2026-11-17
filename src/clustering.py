
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


FEATURES = [
    "TotalSpending",
    "PurchaseFrequency",
    "AverageTransactionValue"
]


def scale_features(customer_data):

    X = customer_data[FEATURES].copy()

    # Reduce the influence of extreme values
    X_log = np.log1p(X)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_log)

    return X_scaled, scaler


def calculate_elbow(X_scaled):

    inertia_values = []
    k_values = range(2, 11)

    for k in k_values:

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        model.fit(X_scaled)
        inertia_values.append(model.inertia_)

    return list(k_values), inertia_values


def perform_clustering(customer_data, n_clusters=4):

    X_scaled, scaler = scale_features(customer_data)

    model = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10
    )

    labels = model.fit_predict(X_scaled)

    result = customer_data.copy()
    result["Cluster"] = labels

    return result, model, scaler


def get_cluster_profiles(clustered_data):

    profiles = (
        clustered_data.groupby("Cluster")
        .agg(
            CustomerCount=("CustomerID", "count"),
            AverageSpending=("TotalSpending", "mean"),
            AverageFrequency=("PurchaseFrequency", "mean"),
            AverageTransactionValue=("AverageTransactionValue", "mean")
        )
        .reset_index()
    )

    return profiles

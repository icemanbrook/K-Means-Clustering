
import pandas as pd


def preprocess_data(file):

    # Load Excel or CSV
    filename = getattr(file, "name", str(file))

    if filename.lower().endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    initial_records = len(df)

    required = ["InvoiceNo", "Quantity", "UnitPrice", "CustomerID"]
    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Remove records without customer IDs
    df = df.dropna(subset=["CustomerID"]).copy()

    # Remove cancelled invoices
    df["InvoiceNo"] = df["InvoiceNo"].astype(str)
    df = df[~df["InvoiceNo"].str.startswith("C")]

    # Validate numerical values
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")

    df = df.dropna(subset=["Quantity", "UnitPrice"])
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

    # Calculate transaction amount
    df["TotalAmount"] = df["Quantity"] * df["UnitPrice"]

    # Calculate invoice-level totals
    invoice_data = (
        df.groupby(["CustomerID", "InvoiceNo"])["TotalAmount"]
        .sum()
        .reset_index()
    )

    # Create customer-level dataset
    customer_data = (
        invoice_data.groupby("CustomerID")
        .agg(
            TotalSpending=("TotalAmount", "sum"),
            PurchaseFrequency=("InvoiceNo", "nunique"),
            AverageTransactionValue=("TotalAmount", "mean")
        )
        .reset_index()
    )

    cleaning_info = {
        "Initial Records": initial_records,
        "Cleaned Records": len(df),
        "Removed Records": initial_records - len(df),
        "Total Customers": len(customer_data)
    }

    return customer_data, df, cleaning_info

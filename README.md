# CustomerIQ — Customer Segmentation Using K-Means

CustomerIQ is an interactive Data Mining application that segments customers by purchasing behaviour using the **K-Means clustering** algorithm. It is built with Python and Streamlit.

The application aggregates transaction data into customer-level features, transforms and scales those features, runs K-Means, and visualizes the resulting customer segments.

## Features

- Upload transaction data in CSV or Excel format
- Clean invalid transactions and rows without customer identifiers
- Aggregate transactions into customer-level metrics
- Apply `log1p` transformation and `StandardScaler`
- Run K-Means with a user-selectable number of clusters
- Explore the Elbow Method (inertia / WCSS)
- View interactive customer-segmentation charts and cluster profiles
- Download the customer-level results, including each customer's cluster assignment

## Dataset format: what to upload

Upload a **transaction-level** CSV or Excel file. Each row should represent an item line belonging to an invoice (transaction).

The file must contain these columns:

| Required column | Expected meaning | Example |
|---|---|---|
| `InvoiceNo` | Invoice or transaction identifier | `536365` |
| `Quantity` | Number of units on that invoice line | `2` |
| `UnitPrice` | Price per unit | `3.50` |
| `CustomerID` | Identifier for the customer | `17850` |

Additional columns are allowed and ignored by the current feature-engineering steps. Column names must match the spelling shown above.

**Important data expectations**
- `CustomerID` must identify the customer. Rows with a missing `CustomerID` are excluded.
- `Quantity` and `UnitPrice` must be numeric. Rows with non-positive quantities or prices are excluded.
- Cancelled invoices are excluded when `InvoiceNo` begins with `C`.
- Multiple rows can share an `InvoiceNo`; the app sums their line amounts to calculate the invoice total.
- The same customer can appear on many invoices.

The application derives these three clustering features for each customer:

| Derived feature | Calculation |
|---|---|
| `TotalSpending` | Sum of invoice totals for the customer |
| `PurchaseFrequency` | Number of unique invoices for the customer |
| `AverageTransactionValue` | Mean invoice total for the customer |

The original transaction dataset is **not included** in this repository. You can use the UCI Online Retail dataset linked below, or another transaction dataset that follows the required column format.

### Sample CSV structure

```csv
InvoiceNo,StockCode,Description,Quantity,UnitPrice,CustomerID
536365,85123A,WHITE HANGING HEART T-LIGHT HOLDER,6,2.55,17850
536365,71053,WHITE METAL LANTERN,6,3.39,17850
536366,22752,SET 7 BABUSHKA NESTING BOXES,2,7.65,17850
536367,84879,ASSORTED COLOUR BIRD ORNAMENT,8,1.69,13047
```

The rows above are only an illustration of the required structure, not a benchmark dataset or expected output.

## Dataset used for development

The project was developed with the **Online Retail** dataset from the UCI Machine Learning Repository:

- Dataset page: https://archive.ics.uci.edu/dataset/352/online+retail
- Download the Excel file and upload it through the app, or place it at `data/Online_Retail.xlsx` to use it as the default local dataset.

The dataset is not committed to this repository.

## Tech stack

- Python
- Pandas and NumPy
- Scikit-learn
- Streamlit
- Plotly
- OpenPyXL

## Run locally

1. Clone the repository:

   ```bash
   git clone https://github.com/icemanbrook/K-Means-Clustering.git
   cd K-Means-Clustering
   ```

2. Create and activate a virtual environment:

   **Windows PowerShell**
   ```powershell
   python -m venv .venv
   .venv\\Scripts\\Activate.ps1
   ```

   **macOS / Linux**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the app:

   ```bash
   streamlit run app.py
   ```

5. Upload a CSV or Excel file using the sidebar. The uploaded file must follow the format described above.

## How the workflow operates

1. Read the uploaded transaction file.
2. Exclude rows without a customer ID, cancelled invoices, invalid quantities, and invalid unit prices.
3. Calculate line amounts using `Quantity × UnitPrice`.
4. Aggregate line amounts into invoice totals.
5. Aggregate invoice totals into customer-level spending, frequency, and average transaction value.
6. Apply `log1p` to the three customer features.
7. Standardize the transformed features using `StandardScaler`.
8. Fit K-Means and assign a cluster label to each customer.
9. Display the Elbow Method, segment charts, and cluster profiles.
10. Allow the resulting customer-level dataset to be downloaded as CSV.

## Interpreting results and limitations

- K-Means cluster labels (0, 1, 2, …) are identifiers, not rankings.
- The number of clusters is selected by the user in the dashboard. The Elbow Method is provided as a guide; it does not automatically prove a uniquely optimal value of K.
- Cluster profiles are summaries of the customers assigned to each cluster. Segment names or marketing interpretations should be assigned only after examining those profiles.
- K-Means is sensitive to feature choices, scaling, outliers, and the selected K.
- The current implementation uses historical transaction behaviour; segments may change as new transactions are added.
- Monetary values are displayed using the pound symbol for the UCI Online Retail development dataset. For other datasets, confirm the currency before interpreting the displayed totals.

## Repository contents

```text
.
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── .gitkeep
└── src/
    ├── __init__.py
    ├── preprocessing.py
    ├── clustering.py
    └── visualization.py
```

## Academic project

**Topic:** Customer Segmentation Using K-Means Clustering  
**Subject:** Data Mining

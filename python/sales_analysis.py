
"""
Financial Performance Analytics
--------------------------------
Analyze sales transactions using Python and pandas.

The analysis includes:
- Data quality validation
- Overall financial KPIs
- Profitability by category
- Top 3 most profitable products
- Monthly revenue trends

Dataset: Synthetic sales transactions for 2026.
"""

from pathlib import Path

import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "sales_data.csv"

REQUIRED_COLUMNS = {
    "order_id",
    "order_date",
    "product",
    "category",
    "quantity",
    "revenue",
    "cost",
}


def load_data(file_path: Path) -> pd.DataFrame:
    """Load the sales dataset from a CSV file."""
    if not file_path.is_file():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    return pd.read_csv(file_path)


def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validate and prepare the sales dataset."""
    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    if df.empty:
        raise ValueError("The dataset is empty.")

    if df[list(REQUIRED_COLUMNS)].isnull().any().any():
        raise ValueError("The dataset contains missing values.")

    if df["order_id"].duplicated().any():
        raise ValueError("Duplicate order IDs detected.")

    df = df.copy()

    df["order_date"] = pd.to_datetime(
        df["order_date"], errors="raise"
    )

    numeric_columns = ["quantity", "revenue", "cost"]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column], errors="raise"
        )

    if (df["quantity"] <= 0).any():
        raise ValueError("Quantity must be positive.")

    if (df[["revenue", "cost"]] < 0).any().any():
        raise ValueError("Revenue and cost cannot be negative.")

    df["profit"] = df["revenue"] - df["cost"]
    df["month"] = df["order_date"].dt.to_period("M")

    return df


def calculate_kpis(df: pd.DataFrame) -> dict:
    """Calculate overall financial performance indicators."""
    total_revenue = df["revenue"].sum()
    total_cost = df["cost"].sum()
    total_profit = total_revenue - total_cost

    profit_margin = (
        total_profit / total_revenue * 100
        if total_revenue != 0
        else 0.0
    )

    return {
        "total_orders": len(df),
        "total_revenue": total_revenue,
        "total_cost": total_cost,
        "total_profit": total_profit,
        "profit_margin": profit_margin,
    }


def analyze_categories(df: pd.DataFrame) -> pd.Series:
    """Calculate total profit by product category."""
    return (
        df.groupby("category")["profit"]
        .sum()
        .sort_values(ascending=False)
    )


def analyze_products(df: pd.DataFrame) -> pd.Series:
    """Identify the three most profitable products."""
    return (
        df.groupby("product")["profit"]
        .sum()
        .sort_values(ascending=False)
        .head(3)
    )


def analyze_monthly_revenue(df: pd.DataFrame) -> pd.Series:
    """Calculate revenue by month in chronological order."""
    return (
        df.groupby("month")["revenue"]
        .sum()
        .sort_index()
    )


def main() -> None:
    """Run the complete financial analysis."""
    df = load_data(DATA_PATH)
    df = validate_data(df)

    kpis = calculate_kpis(df)
    category_profit = analyze_categories(df)
    product_profit = analyze_products(df)
    monthly_revenue = analyze_monthly_revenue(df)

    print("\n" + "=" * 45)
    print("FINANCIAL PERFORMANCE ANALYSIS")
    print("=" * 45)

    print("\nOVERALL FINANCIAL KPIs")
    print("-" * 45)
    print(f"Total Orders:       {kpis['total_orders']:,}")
    print(f"Total Revenue:      {kpis['total_revenue']:,.2f}")
    print(f"Total Cost:         {kpis['total_cost']:,.2f}")
    print(f"Total Profit:       {kpis['total_profit']:,.2f}")
    print(f"Profit Margin:      {kpis['profit_margin']:.2f}%")

    print("\nPROFIT BY CATEGORY")
    print("-" * 45)
    for category, profit in category_profit.items():
        print(f"{category:<20} {profit:>15,.2f}")

    print("\nTOP 3 MOST PROFITABLE PRODUCTS")
    print("-" * 45)
    for product, profit in product_profit.items():
        print(f"{product:<20} {profit:>15,.2f}")

    print("\nMONTHLY REVENUE")
    print("-" * 45)
    for month, revenue in monthly_revenue.items():
        print(f"{month}                  {revenue:>15,.2f}")

    print("\nAnalysis completed successfully.")


if __name__ == "__main__":
    main()

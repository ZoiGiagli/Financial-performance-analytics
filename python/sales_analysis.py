from pathlib import Path
import pandas as pd

df = pd.read_csv(Path(__file__).resolve().parent.parent / "data" / "sales_data.csv")

df["profit"] = df["revenue"] - df["cost"]

total_revenue = df["revenue"].sum()
total_cost = df["cost"].sum()
total_profit = total_revenue - total_cost
profit_margin = total_profit / total_revenue * 100

print("Total Revenue:", total_revenue)
print("Total Cost:", total_cost)
print("Total Profit:", total_profit)
print("Profit Margin:", profit_margin)

profit_by_category = df.groupby("category")["profit"].sum()

print("Profit by category:", profit_by_category)

profit_by_product = df.groupby("product")["profit"].sum().sort_values(ascending=False).head(3)

print("Profit by product:", profit_by_product)

df["order_date"] = pd.to_datetime(df["order_date"])
df["month"] = df["order_date"].dt.to_period("M")

revenue_by_month = df.groupby("month")["revenue"].sum()

print("Revenue by month:",  revenue_by_month)



"""
generate_sample_data.py
Creates a realistic, intentionally messy 5-year sales dataset so the
analyzer has real missing values, duplicates, and outliers to clean.
Run this once to (re)create sample_data/sales_data.csv.
"""

import numpy as np
import pandas as pd

np.random.seed(42)

PRODUCTS = {
    "Wireless Mouse": "Electronics",
    "Mechanical Keyboard": "Electronics",
    "USB-C Charger": "Electronics",
    "Bluetooth Speaker": "Electronics",
    "Running Shoes": "Sports",
    "Yoga Mat": "Sports",
    "Cricket Bat": "Sports",
    "Winter Jacket": "Clothing",
    "Cotton T-Shirt": "Clothing",
    "Denim Jeans": "Clothing",
    "Non-Stick Pan": "Home & Kitchen",
    "Coffee Maker": "Home & Kitchen",
    "Bed Sheet Set": "Home & Kitchen",
    "Face Moisturizer": "Beauty",
    "Shampoo": "Beauty",
}

REGIONS = ["North", "South", "East", "West"]

BASE_PRICE = {
    "Wireless Mouse": 15, "Mechanical Keyboard": 55, "USB-C Charger": 12,
    "Bluetooth Speaker": 35, "Running Shoes": 60, "Yoga Mat": 20,
    "Cricket Bat": 45, "Winter Jacket": 80, "Cotton T-Shirt": 15,
    "Denim Jeans": 40, "Non-Stick Pan": 25, "Coffee Maker": 50,
    "Bed Sheet Set": 30, "Face Moisturizer": 18, "Shampoo": 10,
}


def generate_rows(start_date="2021-01-01", end_date="2025-12-31", target_rows=4500):
    dates = pd.date_range(start=start_date, end=end_date, freq="D")
    rows = []
    order_id = 1000

    for date in dates:
        # More orders in Nov/Dec (seasonal boost) and slight year-over-year growth
        month = date.month
        year_factor = 1 + (date.year - 2021) * 0.08
        seasonal_factor = 1.6 if month in (11, 12) else (1.2 if month in (6, 7) else 1.0)
        daily_orders = max(1, int(np.random.poisson(2.4 * year_factor * seasonal_factor)))

        for _ in range(daily_orders):
            product = np.random.choice(list(PRODUCTS.keys()))
            category = PRODUCTS[product]
            region = np.random.choice(REGIONS)
            quantity = np.random.randint(1, 8)
            base_price = BASE_PRICE[product]
            unit_price = round(base_price * np.random.uniform(0.9, 1.15), 2)
            sales = round(quantity * unit_price, 2)

            rows.append({
                "OrderID": order_id,
                "Date": date.strftime("%Y-%m-%d"),
                "Product": product,
                "Category": category,
                "Region": region,
                "Quantity": quantity,
                "UnitPrice": unit_price,
                "Sales": sales,
            })
            order_id += 1

            if len(rows) >= target_rows:
                return pd.DataFrame(rows)

    return pd.DataFrame(rows)


def add_mess(df):
    """Introduces missing values, duplicates, and outliers on purpose."""
    df = df.copy()
    n = len(df)
    rng = np.random.default_rng(7)

    # Missing values (~3% each in a few columns)
    for col in ["UnitPrice", "Quantity", "Region"]:
        idx = rng.choice(n, size=int(n * 0.03), replace=False)
        df.loc[idx, col] = np.nan

    # Missing Sales in some rows (recomputable from Quantity * UnitPrice)
    idx = rng.choice(n, size=int(n * 0.02), replace=False)
    df.loc[idx, "Sales"] = np.nan

    # Duplicate rows (~2%)
    dup_rows = df.sample(int(n * 0.02), random_state=1)
    df = pd.concat([df, dup_rows], ignore_index=True)

    # A few extreme outliers in Sales
    outlier_idx = rng.choice(df.index, size=6, replace=False)
    df.loc[outlier_idx, "Sales"] = df.loc[outlier_idx, "Sales"] * rng.uniform(15, 25, size=6)

    # Shuffle rows so duplicates aren't obviously at the end
    df = df.sample(frac=1, random_state=3).reset_index(drop=True)
    return df


if __name__ == "__main__":
    df = generate_rows()
    df = add_mess(df)
    df.to_csv("sample_data/sales_data.csv", index=False)
    print(f"Generated {len(df)} rows -> sample_data/sales_data.csv")
    print(f"Missing values per column:\n{df.isna().sum()}")
    print(f"Duplicate rows: {df.duplicated().sum()}")

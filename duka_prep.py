"""Duka Electronics: cleaning and derived columns (Week 3 rules, reused for the board report).

Usage:
    from duka_prep import load_clean_duka
    df, log = load_clean_duka("duka_sales.csv")
    python duka_prep.py            # writes duka_sales_clean.csv
"""
import numpy as np
import pandas as pd

PREMIUM_MIN = 28_000          # Week 3 rule: Premium if unit_price >= KES 28,000, otherwise Value
MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def load_clean_duka(path="duka_sales.csv"):
    """Load, validate and enrich the Duka sales extract.

    Cleaning rules (applied in code, none hard-coded to rows):
      1. Parse order_date as datetime; strip whitespace in text columns.
      2. Drop repeated order_id (keep first).
      3. Drop rows with missing key fields (order_id, order_date, branch, product, channel, quantity, unit_price).
      4. Drop invalid rows (quantity <= 0 or unit_price <= 0).
    Derived columns: revenue, month_num, month (ordered), quarter (Q1/Q2), weekday (ordered),
    is_weekend, price_band (Premium >= KES 28,000, otherwise Value).

    Returns
    -------
    (df, log) : cleaned DataFrame and a log DataFrame (step, rule, rows_affected, rows_after).
    """
    df = pd.read_csv(path, parse_dates=["order_date"])
    log = [{"step": "0 Load", "rule": "Raw rows read", "rows_affected": 0, "rows_after": len(df)}]

    def note(step, rule, before):
        log.append({"step": step, "rule": rule, "rows_affected": before - len(df), "rows_after": len(df)})

    for c in ["branch", "product", "channel"]:
        df[c] = df[c].astype("string").str.strip()

    b = len(df); df = df.drop_duplicates(subset="order_id", keep="first"); note("1 Uniqueness", "Drop repeated order_id", b)
    key = ["order_id", "order_date", "branch", "product", "channel", "quantity", "unit_price"]
    b = len(df); df = df.dropna(subset=key); note("2 Completeness", "Drop rows missing a key field", b)
    b = len(df); df = df[(df.quantity > 0) & (df.unit_price > 0)]; note("3 Validity", "Drop quantity <= 0 or unit_price <= 0", b)
    df = df.reset_index(drop=True)

    df["revenue"] = df["quantity"] * df["unit_price"]                              # KES
    df["month_num"] = df["order_date"].dt.month
    df["month"] = pd.Categorical(df["order_date"].dt.month_name(), categories=MONTHS, ordered=True)
    df["quarter"] = np.where(df["month_num"] <= 3, "Q1", "Q2")
    df["weekday"] = pd.Categorical(df["order_date"].dt.day_name(), categories=WEEKDAYS, ordered=True)
    df["is_weekend"] = df["order_date"].dt.dayofweek >= 5
    df["price_band"] = np.where(df["unit_price"] >= PREMIUM_MIN, "Premium", "Value")
    return df, pd.DataFrame(log)


if __name__ == "__main__":
    clean, log = load_clean_duka()
    print(log.to_string(index=False))
    clean.assign(month=clean["month"].astype(str), weekday=clean["weekday"].astype(str)).to_csv("duka_sales_clean.csv", index=False)
    print("saved duka_sales_clean.csv", clean.shape)

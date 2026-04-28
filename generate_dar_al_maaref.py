"""
Dar Al Maaref — Egyptian Publishing & Printing Company
Dataset Generator for Digital Transformation Course - BINF 402, Spring 2026
GIU - Dr. Nourhan Hamdi
Team: Ali Haytham, Yehia Hossam, Frass Mohamed, Mohamed Mokhtar,
      Yassin Tourky, Youssef Ismail, Mariam Ahmed
"""

import os
import random
import numpy as np
import pandas as pd
from faker import Faker
from datetime import date, timedelta

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
fake_en = Faker("en_US")
fake_en.seed_instance(SEED)

PROJECT_SLUG = "dar_al_maaref"
OUTPUT_BASE  = f"output/{PROJECT_SLUG}"
STUDENT_DIR  = f"{OUTPUT_BASE}/student_dataset"
PRIVATE_DIR  = f"{OUTPUT_BASE}/private_instructor_notes"

DATE_START = date(2023, 1, 1)
DATE_END   = date(2024, 12, 31)
TARGET_SALES_ROWS = 2000
TARGET_INV_ROWS   = 300   # monthly inventory snapshots per book

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def make_dirs():
    os.makedirs(STUDENT_DIR, exist_ok=True)
    os.makedirs(PRIVATE_DIR, exist_ok=True)

def save(df: pd.DataFrame, path: str):
    df.to_csv(path, index=False, encoding="utf-8")
    print(f"  Saved {path}  ({len(df)} rows)")

# ─────────────────────────────────────────────
# DIM DATE
# ─────────────────────────────────────────────
EGYPTIAN_HOLIDAYS = {
    date(2023, 1, 7), date(2023, 4, 25), date(2023, 5, 1),
    date(2023, 6, 30), date(2023, 7, 23), date(2023, 10, 6),
    date(2024, 1, 7), date(2024, 4, 25), date(2024, 5, 1),
    date(2024, 6, 30), date(2024, 7, 23), date(2024, 10, 6),
}

def gen_dim_date():
    rows = []
    d = DATE_START
    while d <= DATE_END:
        rows.append({
            "date_id":     d.strftime("%Y%m%d"),
            "date":        d.strftime("%Y-%m-%d"),   # stored as string (cleaning task)
            "day":         d.day,
            "month":       d.month,
            "month_name":  d.strftime("%B"),
            "quarter":     (d.month - 1) // 3 + 1,
            "year":        d.year,
            "day_of_week": d.strftime("%A"),
            "is_weekend":  d.weekday() >= 4,
            "is_holiday":  d in EGYPTIAN_HOLIDAYS,
        })
        d += timedelta(days=1)
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# DIM BOOK
# ─────────────────────────────────────────────
BOOKS_RAW = [
    # (book_id, title, category, author, list_price_egp, cost_egp, published_year, is_bestseller)
    ("B001", "Arabic Language Grade 5",          "Educational",  "Ahmed Kamal",       45,  18, 2019, True),
    ("B002", "Mathematics Grade 7",              "Educational",  "Mona Salah",        50,  20, 2020, True),
    ("B003", "Science Grade 9",                  "Educational",  "Ibrahim Nasser",    55,  22, 2021, True),
    ("B004", "History of Egypt",                 "Educational",  "Rania Farouk",      48,  19, 2018, False),
    ("B005", "English Language Grade 6",         "Educational",  "Sara Hossam",       52,  21, 2020, True),
    ("B006", "Introduction to Economics",        "Academic",     "Tarek Mansour",    120,  48, 2017, True),
    ("B007", "Principles of Management",         "Academic",     "Dina Khalil",      135,  54, 2019, True),
    ("B008", "Business Statistics",              "Academic",     "Omar Gamal",       110,  44, 2021, False),
    ("B009", "Egyptian Law Fundamentals",        "Academic",     "Hana Suleiman",    150,  60, 2016, False),
    ("B010", "Introduction to Programming",     "Academic",     "Youssef Ramzy",    125,  50, 2022, True),
    ("B011", "The Nile and the Desert",          "Novel",        "Layla Sherif",      80,  25, 2020, True),
    ("B012", "Letters from Cairo",               "Novel",        "Karim Badawi",      75,  24, 2019, False),
    ("B013", "Shadows of the Pyramid",           "Novel",        "Heba Mostafa",      85,  27, 2021, True),
    ("B014", "A Summer in Alexandria",           "Novel",        "Nadia Fouad",       70,  22, 2018, False),
    ("B015", "The Last Pharaoh",                 "Novel",        "Samir Ismail",      90,  29, 2022, True),
    ("B016", "Encyclopedia of Egyptian History", "Reference",   "Editorial Board",  220,  88, 2015, False),
    ("B017", "Arabic Dictionary (Modern)",       "Reference",   "Editorial Board",  180,  72, 2017, False),
    ("B018", "Atlas of the Arab World",          "Reference",   "Geog. Dept.",      160,  64, 2018, False),
    ("B019", "Science Grade 10",                 "Educational",  "Ibrahim Nasser",    55,  22, 2022, False),
    ("B020", "Mathematics Grade 9",              "Educational",  "Mona Salah",        50,  20, 2021, True),
]

def gen_dim_book():
    rows = []
    rng = np.random.default_rng(SEED)
    for b in BOOKS_RAW:
        bid, title, cat, author, price, cost, year, best = b
        rows.append({
            "book_id":        bid,
            "title":          title,
            "category":       cat,
            "author":         author,
            "list_price_egp": price,
            "unit_cost_egp":  cost,
            "published_year": year,
            "is_bestseller":  best,
            "isbn":           f"978-977-{rng.integers(100,999)}-{rng.integers(100,999)}-{rng.integers(0,9)}",
        })
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# DIM CUSTOMER
# ─────────────────────────────────────────────
CUSTOMER_TYPES = ["Individual", "School", "Library", "Distributor"]
EGYPTIAN_GOVS  = [
    "Cairo", "Giza", "Alexandria", "Luxor", "Aswan", "Mansoura",
    "Tanta", "Suez", "Port Said", "Asyut", "Minya", "Sohag",
    "Fayoum", "Beni Suef", "Qena", "Ismailia", "Damanhur",
]

def gen_dim_customer():
    rng  = np.random.default_rng(SEED + 10)
    rows = []
    type_counts = {"Individual": 60, "School": 25, "Library": 15, "Distributor": 10}

    cid = 1
    for ctype, count in type_counts.items():
        for _ in range(count):
            gov = rng.choice(EGYPTIAN_GOVS)
            if ctype == "Individual":
                name = fake_en.name()
            elif ctype == "School":
                name = f"{gov} {rng.choice(['Primary','Preparatory','Secondary'])} School {rng.integers(1,20)}"
            elif ctype == "Library":
                name = f"{gov} Public Library"
            else:
                name = f"{fake_en.last_name()} Distribution Co."

            rows.append({
                "customer_id":   f"C{cid:04d}",
                "customer_name": name,
                "customer_type": ctype,
                "governorate":   gov,
                "region":        _gov_region(gov),
            })
            cid += 1
    return pd.DataFrame(rows)

def _gov_region(gov):
    upper = ["Luxor","Aswan","Asyut","Minya","Sohag","Qena","Fayoum","Beni Suef"]
    delta = ["Mansoura","Tanta","Damanhur","Ismailia"]
    canal = ["Suez","Port Said","Ismailia"]
    if gov in upper:  return "Upper Egypt"
    if gov in canal:  return "Canal Zone"
    if gov in delta:  return "Delta"
    return "Greater Cairo & Alex"

# ─────────────────────────────────────────────
# DIM CHANNEL
# ─────────────────────────────────────────────
CHANNELS = [
    ("CH01", "Online Store",       "Direct - B2C"),
    ("CH02", "Retail Bookstore",   "Direct - B2C"),
    ("CH03", "School Contract",    "B2B"),
    ("CH04", "Library Contract",   "B2B"),
    ("CH05", "Distributor Order",  "B2B"),
]

def gen_dim_channel():
    rows = [{"channel_id": cid, "channel_name": name, "channel_type": ctype}
            for cid, name, ctype in CHANNELS]
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# FACT SALES
# ─────────────────────────────────────────────
# Customer type → compatible channels
CTYPE_CHANNEL = {
    "Individual":  ["CH01", "CH02"],
    "School":      ["CH03", "CH01"],
    "Library":     ["CH04", "CH01"],
    "Distributor": ["CH05"],
}

# Customer type quantity ranges
QTY_RANGE = {
    "Individual":  (1, 3),
    "School":      (10, 200),
    "Library":     (5, 50),
    "Distributor": (50, 500),
}

# Discount by customer type
DISCOUNT_PROFILE = {
    "Individual":  [0, 5, 10],
    "School":      [10, 15, 20],
    "Library":     [15, 20, 25],
    "Distributor": [25, 30, 35],
}

def seasonality_weight(month):
    # Back-to-school peaks: Aug-Sep; end-of-year: Dec; summer slump: Jun-Jul
    w = {1:0.9, 2:0.9, 3:1.0, 4:1.1, 5:1.0, 6:0.75,
         7:0.70, 8:1.6, 9:1.8, 10:1.2, 11:1.0, 12:1.1}
    return w.get(month, 1.0)

# Book popularity weights
BOOK_WEIGHT = {
    "B001":9,"B002":9,"B003":8,"B004":4,"B005":8,
    "B006":6,"B007":6,"B008":4,"B009":3,"B010":6,
    "B011":7,"B012":5,"B013":6,"B014":4,"B015":6,
    "B016":2,"B017":3,"B018":2,"B019":5,"B020":8,
}

def gen_fact_sales(dim_date, dim_book, dim_customer, dim_channel):
    rng = np.random.default_rng(SEED + 20)

    book_ids   = [b[0] for b in BOOKS_RAW]
    book_wts   = [BOOK_WEIGHT[b] for b in book_ids]
    cust_df    = dim_customer.copy()
    book_df    = dim_book.set_index("book_id")

    rows = []
    sale_id = 1

    for _ in range(TARGET_SALES_ROWS):
        # Date with seasonality
        date_row = dim_date.sample(1, weights=dim_date["month"].map(seasonality_weight)).iloc[0]
        date_id  = date_row["date_id"]
        year     = date_row["year"]

        # Customer
        cust_row  = cust_df.sample(1).iloc[0]
        cust_id   = cust_row["customer_id"]
        cust_type = cust_row["customer_type"]

        # Book
        book_id   = random.choices(book_ids, weights=book_wts)[0]
        book_row  = book_df.loc[book_id]
        list_price = book_row["list_price_egp"]
        unit_cost  = book_row["unit_cost_egp"]
        category   = book_row["category"]

        # Educational books sell more to schools/libraries
        if category == "Educational" and cust_type in ("School", "Library"):
            pass  # natural fit, keep
        elif category == "Academic" and cust_type == "Distributor":
            pass
        # slight price variance (promotional pricing)
        actual_price = round(list_price * rng.uniform(0.97, 1.03), 2)

        # Quantity
        qmin, qmax = QTY_RANGE[cust_type]
        qty = int(rng.integers(qmin, qmax + 1))

        # Discount
        disc_options = DISCOUNT_PROFILE[cust_type]
        disc_pct     = random.choice(disc_options)
        disc_amt     = round(actual_price * qty * disc_pct / 100, 2)
        total_rev    = round(actual_price * qty - disc_amt, 2)
        total_cost   = round(unit_cost * qty, 2)
        profit       = round(total_rev - total_cost, 2)

        # Channel
        channel_id = random.choice(CTYPE_CHANNEL[cust_type])

        # Order status: mostly delivered
        status = random.choices(
            ["Delivered", "Returned", "Pending"],
            weights=[90, 5, 5]
        )[0]
        if status == "Returned":
            total_rev = 0
            profit    = 0

        # Processing days (B2B takes longer)
        proc_days = int(rng.integers(1, 3) if cust_type == "Individual"
                        else rng.integers(3, 14))

        rows.append({
            "sale_id":          f"ORD{sale_id:05d}",
            "date_id":          date_id,
            "book_id":          book_id,
            "customer_id":      cust_id,
            "channel_id":       channel_id,
            "quantity":         qty,
            "unit_price_egp":   actual_price,
            "discount_pct":     disc_pct,
            "discount_amount":  disc_amt,
            "total_revenue":    total_rev,
            "total_cost":       total_cost,
            "profit":           profit,
            "order_status":     status,
            "processing_days":  proc_days,
        })
        sale_id += 1

    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# FACT INVENTORY (monthly snapshot)
# ─────────────────────────────────────────────
def gen_fact_inventory(dim_book, dim_date):
    rng   = np.random.default_rng(SEED + 30)
    rows  = []
    inv_id = 1

    # Monthly snapshots for each book (only month-start dates)
    months = dim_date[dim_date["day"] == 1][["date_id", "month", "year"]].copy()

    for _, brow in dim_book.iterrows():
        book_id = brow["book_id"]
        is_best = brow["is_bestseller"]

        # Base stock level depends on popularity
        base_stock = 500 if is_best else 200

        for _, mrow in months.iterrows():
            month_num = mrow["month"]
            # Back-to-school months deplete stock faster
            depletion = rng.integers(30, 150) if month_num in (8, 9, 3) else rng.integers(5, 80)
            restock   = rng.integers(0, 200)
            stock_end = max(0, int(base_stock - depletion + restock))
            reorder_pt = 50 if is_best else 20

            rows.append({
                "inventory_id":      f"INV{inv_id:05d}",
                "date_id":           mrow["date_id"],
                "book_id":           book_id,
                "opening_stock":     base_stock,
                "units_received":    restock,
                "units_sold":        depletion,
                "closing_stock":     stock_end,
                "reorder_point":     reorder_pt,
                "below_reorder":     stock_end < reorder_pt,
            })
            base_stock = stock_end
            inv_id    += 1

    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# INJECT CLEANING ISSUES
# ─────────────────────────────────────────────
def inject_issues(df_sales, df_book, df_customer, df_channel, df_inv):
    n   = len(df_sales)
    rng = np.random.default_rng(SEED + 99)

    # 1. ~5% nulls in discount_pct
    idx = rng.choice(n, size=int(n * 0.05), replace=False)
    df_sales.loc[idx, "discount_pct"] = np.nan

    # 2. ~4% nulls in processing_days
    idx2 = rng.choice(n, size=int(n * 0.04), replace=False)
    df_sales.loc[idx2, "processing_days"] = np.nan

    # 3. Inconsistent casing in order_status (~3%)
    idx3 = rng.choice(n, size=int(n * 0.03), replace=False)
    df_sales.loc[idx3, "order_status"] = df_sales.loc[idx3, "order_status"].str.upper()

    # 4. total_revenue stored as string in ~3% of rows
    df_sales["total_revenue"] = df_sales["total_revenue"].astype(object)
    idx4 = rng.choice(n, size=int(n * 0.03), replace=False)
    for i in idx4:
        df_sales.at[i, "total_revenue"] = str(df_sales.at[i, "total_revenue"])

    # 5. Leading/trailing whitespace in channel_id for ~2%
    idx5 = rng.choice(n, size=int(n * 0.02), replace=False)
    df_sales.loc[idx5, "channel_id"] = " " + df_sales.loc[idx5, "channel_id"]

    # 6. Impossible processing_days (negative) — 3 rows
    bad = rng.choice(n, size=3, replace=False)
    for i in bad:
        df_sales.at[i, "processing_days"] = -rng.integers(1, 5)

    # 7. Duplicate rows (~1.5%)
    dup_idx = rng.choice(n, size=int(n * 0.015), replace=False)
    dups = df_sales.iloc[dup_idx].copy()
    df_sales = pd.concat([df_sales, dups], ignore_index=True)

    # 8. dim_book: inconsistent category casing for 3 rows
    df_book.loc[df_book["book_id"].isin(["B011","B012","B013"]), "category"] = "novel"

    # 9. dim_customer: whitespace in customer_type for ~5 rows
    ws_rows = df_customer.sample(5, random_state=SEED).index
    df_customer.loc[ws_rows, "customer_type"] = df_customer.loc[ws_rows, "customer_type"] + " "

    # 10. dim_date: date column is text already — that's intentional (noted for cleaning)

    return df_sales, df_book, df_customer, df_channel, df_inv

# ─────────────────────────────────────────────
# VALIDATION
# ─────────────────────────────────────────────
def validate(df_sales, df_inv, dim_date, dim_book, dim_customer, dim_channel):
    print("\nValidation:")
    errors = []
    valid_dates    = set(dim_date["date_id"])
    valid_books    = set(dim_book["book_id"])
    valid_custs    = set(dim_customer["customer_id"])
    valid_channels = set(dim_channel["channel_id"])

    # strip whitespace injected into channel_id before FK check
    cleaned_ch = df_sales["channel_id"].str.strip()
    if not cleaned_ch.isin(valid_channels).all():
        errors.append("  FK mismatch channel_id (expected — whitespace injection)")
    if not df_sales["date_id"].isin(valid_dates).all():
        errors.append("  FK mismatch date_id")
    if not df_sales["book_id"].isin(valid_books).all():
        errors.append("  FK mismatch book_id")
    if not df_sales["customer_id"].isin(valid_custs).all():
        errors.append("  FK mismatch customer_id")

    if errors:
        print("  Warnings (intentional or real):")
        for e in errors: print(e)

    n = len(df_sales)
    dups = df_sales.duplicated().sum()
    null_disc = df_sales["discount_pct"].isna().mean()
    null_proc = df_sales["processing_days"].isna().mean()

    print(f"  fact_sales rows (incl. dupes):  {n}")
    print(f"  Duplicate rows injected:        {dups}")
    print(f"  Null rate discount_pct:         {null_disc:.1%}")
    print(f"  Null rate processing_days:      {null_proc:.1%}")
    print(f"  fact_inventory rows:            {len(df_inv)}")

# ─────────────────────────────────────────────
# INSTRUCTOR NOTES
# ─────────────────────────────────────────────
CLEANING_MD = """\
# Expected Cleaning Tasks — Dar Al Maaref

## fact_sales.csv

| # | Issue | Column | Approx. Rate |
|---|-------|--------|--------------|
| 1 | Missing values | `discount_pct` | ~5% nulls |
| 2 | Missing values | `processing_days` | ~4% nulls |
| 3 | Inconsistent casing | `order_status` | ~3% stored as uppercase ("DELIVERED") |
| 4 | Mixed data type | `total_revenue` | ~3% stored as text strings |
| 5 | Leading whitespace | `channel_id` | ~2% have a leading space — causes FK lookup failure |
| 6 | Impossible values | `processing_days` | 3 rows with negative values |
| 7 | Duplicate rows | all columns | ~1.5% fully duplicated records |

## dim_book.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 8 | Inconsistent casing | `category` | "novel" (lowercase) for B011, B012, B013 — should be "Novel" |

## dim_customer.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 9 | Trailing whitespace | `customer_type` | 5 rows with trailing space — causes group-by errors |

## dim_date.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 10 | Date stored as string | `date` | Column is text "YYYY-MM-DD" — must be converted to Date type in Power Query |

## Notes for Instructor
- The whitespace in `channel_id` (fact) is the trickiest: a simple relationship in Power BI will silently fail for those rows, producing blanks. Students must use Trim in Power Query.
- Negative `processing_days` are subtle — students need to filter or flag these as data quality issues.
- Category casing in dim_book affects pie/bar charts (two "Novel" slices appear).
"""

DAX_MD = """\
# Suggested DAX Measures — Dar Al Maaref

## Revenue & Profit
```dax
Total Revenue =
    CALCULATE(
        SUM(fact_sales[total_revenue]),
        fact_sales[order_status] = "Delivered"
    )

Total Cost =
    CALCULATE(
        SUM(fact_sales[total_cost]),
        fact_sales[order_status] = "Delivered"
    )

Total Profit =
    [Total Revenue] - [Total Cost]

Profit Margin % =
    DIVIDE([Total Profit], [Total Revenue])

Total Orders =
    COUNTROWS(fact_sales)

Average Order Value =
    DIVIDE([Total Revenue], [Total Orders])
```

## Sales Performance
```dax
Total Units Sold =
    CALCULATE(
        SUM(fact_sales[quantity]),
        fact_sales[order_status] = "Delivered"
    )

Return Rate =
    DIVIDE(
        COUNTROWS(FILTER(fact_sales, fact_sales[order_status] = "Returned")),
        [Total Orders]
    )

Revenue by Category =
    CALCULATE([Total Revenue], ALLEXCEPT(dim_book, dim_book[category]))
```

## Growth & Time Intelligence
```dax
YTD Revenue =
    TOTALYTD([Total Revenue], dim_date[date])

Revenue MoM Growth % =
    VAR PrevMonth = CALCULATE([Total Revenue], DATEADD(dim_date[date], -1, MONTH))
    RETURN DIVIDE([Total Revenue] - PrevMonth, PrevMonth)

Revenue Previous Year =
    CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(dim_date[date]))

YoY Revenue Growth % =
    DIVIDE([Total Revenue] - [Revenue Previous Year], [Revenue Previous Year])
```

## Customer KPIs
```dax
Number of Customers =
    DISTINCTCOUNT(fact_sales[customer_id])

Repeat Customers =
    COUNTROWS(
        FILTER(
            VALUES(fact_sales[customer_id]),
            CALCULATE(COUNTROWS(fact_sales)) > 1
        )
    )

Customer Retention Rate =
    DIVIDE([Repeat Customers], [Number of Customers])

Avg Processing Days =
    AVERAGE(fact_sales[processing_days])
```

## Inventory KPIs
```dax
Total Closing Stock =
    SUM(fact_inventory[closing_stock])

Books Below Reorder Point =
    CALCULATE(
        COUNTROWS(fact_inventory),
        fact_inventory[below_reorder] = TRUE()
    )

Inventory Turnover =
    DIVIDE([Total Units Sold], [Total Closing Stock])
```
"""

DASHBOARD_MD = """\
# Dashboard Questions & Visual Suggestions — Dar Al Maaref

## Analytical Questions (student-facing prompts)
1. Which book titles and categories generate the most revenue?
2. Which customer type (Individual / School / Library / Distributor) drives the most sales?
3. How does revenue change month-over-month and year-over-year?
4. What is the profit margin across different book categories?
5. Which sales channel (online vs. contract vs. distributor) performs best?
6. Which governorates/regions generate the most sales?
7. Which books are running low on stock and may need reprinting?
8. What is the average order processing time by customer type?
9. How does back-to-school season (Aug–Sep) affect sales and inventory?
10. What is the return rate, and which books have the highest return rates?

## Suggested Visuals (instructor only)

| Visual | Type | Fields |
|--------|------|--------|
| Total Revenue KPI | Card | [Total Revenue] |
| Total Orders KPI | Card | [Total Orders] |
| Profit Margin % KPI | Card | [Profit Margin %] |
| Customer Retention Rate KPI | Card | [Customer Retention Rate] |
| Revenue by Book Category | Bar/Donut | dim_book[category], [Total Revenue] |
| Top 10 Best-Selling Books | Bar | dim_book[title], [Total Units Sold] |
| Sales over Time | Line | dim_date[month_name], [Total Revenue] — year slicer |
| Revenue by Customer Type | Stacked bar | dim_customer[customer_type], [Total Revenue] |
| Revenue by Governorate | Map / Choropleth | dim_customer[governorate], [Total Revenue] |
| Channel Comparison | Clustered bar | dim_channel[channel_name], [Total Revenue] |
| Inventory Below Reorder | Table/Alert | dim_book[title], fact_inventory[closing_stock], [reorder_point] |
| Avg Processing Days | Bar | dim_customer[customer_type], [Avg Processing Days] |
| YoY Revenue | Line | dim_date[year+month], [Total Revenue] + [Revenue Previous Year] |

## Suggested Slicers
- Year
- Quarter / Month
- Book Category
- Customer Type
- Governorate / Region
- Sales Channel
"""

MODEL_MD = """\
# Star Schema Relationships — Dar Al Maaref

## Tables
- **fact_sales** — central fact table (~2,000+ rows after cleaning)
- **fact_inventory** — secondary fact table (monthly stock snapshots per book)
- **dim_date** — date dimension (shared by both fact tables)
- **dim_book** — book dimension (shared by both fact tables)
- **dim_customer** — customer dimension
- **dim_channel** — sales channel dimension

## Relationships

### fact_sales relationships
| Fact Column | → | Dimension Table | Dimension Column | Cardinality | Filter Direction |
|-------------|---|-----------------|-----------------|-------------|-----------------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single (dim → fact) |
| `book_id` | → | `dim_book` | `book_id` | Many-to-One | Single (dim → fact) |
| `customer_id` | → | `dim_customer` | `customer_id` | Many-to-One | Single (dim → fact) |
| `channel_id` | → | `dim_channel` | `channel_id` | Many-to-One | Single (dim → fact) |

### fact_inventory relationships
| Fact Column | → | Dimension Table | Dimension Column | Cardinality | Filter Direction |
|-------------|---|-----------------|-----------------|-------------|-----------------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single (dim → fact) |
| `book_id` | → | `dim_book` | `book_id` | Many-to-One | Single (dim → fact) |

## Notes
- Both fact tables share `dim_date` and `dim_book` — Power BI handles this correctly with two separate relationships.
- Do **not** create a direct relationship between `fact_sales` and `fact_inventory` — route all filters through shared dimensions.
- Mark `dim_date[date]` as a **Date Table** for time intelligence DAX functions.
- After cleaning, `channel_id` whitespace must be removed (Trim in Power Query) or the FK relationship will silently produce blanks.
- Filter direction should be **single** (dimension → fact) for all relationships.
"""

DATA_DICT_MD = """\
# Data Dictionary — Dar Al Maaref
## Digital Transformation Course · BINF 402 · GIU · Spring 2026

---

## Business Story
Dar Al Maaref is an Egyptian publishing and printing company selling educational books, academic titles, novels, and reference works.
This dataset covers **book sales orders** and **monthly inventory snapshots** for 2023–2024.
Customers include individual buyers, schools, libraries, and distributors.
Your goal as a manager is to track sales performance, profitability, inventory levels, and channel efficiency.

---

## Files

### `fact_sales.csv` (main fact table)
| Column | Description |
|--------|-------------|
| `sale_id` | Unique order identifier |
| `date_id` | Foreign key → `dim_date.date_id` |
| `book_id` | Foreign key → `dim_book.book_id` |
| `customer_id` | Foreign key → `dim_customer.customer_id` |
| `channel_id` | Foreign key → `dim_channel.channel_id` |
| `quantity` | Number of copies ordered |
| `unit_price_egp` | Actual selling price per copy (EGP) |
| `discount_pct` | Discount percentage applied |
| `discount_amount` | Total discount value (EGP) |
| `total_revenue` | Net revenue for the order (EGP) |
| `total_cost` | Total production/procurement cost (EGP) |
| `profit` | Revenue minus cost (EGP) |
| `order_status` | Delivered, Returned, or Pending |
| `processing_days` | Days from order to delivery |

### `fact_inventory.csv` (secondary fact table)
| Column | Description |
|--------|-------------|
| `inventory_id` | Unique snapshot identifier |
| `date_id` | Foreign key → `dim_date.date_id` (month start) |
| `book_id` | Foreign key → `dim_book.book_id` |
| `opening_stock` | Units at start of month |
| `units_received` | Units restocked during the month |
| `units_sold` | Units sold/dispatched during the month |
| `closing_stock` | Units remaining at end of month |
| `reorder_point` | Minimum stock threshold before reorder |
| `below_reorder` | True if closing stock < reorder point |

### `dim_date.csv`
| Column | Description |
|--------|-------------|
| `date_id` | Primary key (YYYYMMDD) |
| `date` | Full date string (YYYY-MM-DD) |
| `day` | Day of month |
| `month` | Month number |
| `month_name` | Month name |
| `quarter` | Quarter (1–4) |
| `year` | Year |
| `day_of_week` | Weekday name |
| `is_weekend` | True if Friday or Saturday |
| `is_holiday` | True if Egyptian public holiday |

### `dim_book.csv`
| Column | Description |
|--------|-------------|
| `book_id` | Primary key |
| `title` | Book title |
| `category` | Educational, Academic, Novel, or Reference |
| `author` | Author name |
| `list_price_egp` | Standard retail price (EGP) |
| `unit_cost_egp` | Production cost per copy (EGP) |
| `published_year` | Year of publication |
| `is_bestseller` | Whether book is a top seller |
| `isbn` | Synthetic ISBN identifier |

### `dim_customer.csv`
| Column | Description |
|--------|-------------|
| `customer_id` | Primary key |
| `customer_name` | Customer or institution name |
| `customer_type` | Individual, School, Library, or Distributor |
| `governorate` | Egyptian governorate |
| `region` | Broader region (e.g., Upper Egypt, Delta) |

### `dim_channel.csv`
| Column | Description |
|--------|-------------|
| `channel_id` | Primary key |
| `channel_name` | Channel (Online Store, Retail Bookstore, etc.) |
| `channel_type` | Direct - B2C or B2B |

---

## Intended Relationships
- `fact_sales.date_id` → `dim_date.date_id`
- `fact_sales.book_id` → `dim_book.book_id`
- `fact_sales.customer_id` → `dim_customer.customer_id`
- `fact_sales.channel_id` → `dim_channel.channel_id`
- `fact_inventory.date_id` → `dim_date.date_id`
- `fact_inventory.book_id` → `dim_book.book_id`

## Notes for Students
- The dataset **requires cleaning** before analysis — look for type issues, missing values, and inconsistencies.
- Build a **star schema** in Power BI with both fact tables connected through shared dimensions.
- Mark `dim_date` as your Date Table for time intelligence.
- Back-to-school months (August–September) should show clear seasonal patterns in the data.
"""

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print("=" * 55)
    print("Dar Al Maaref — Dataset Generator")
    print("=" * 55)
    make_dirs()

    print("\n[1/5] Generating dimension tables...")
    dim_date     = gen_dim_date()
    dim_book     = gen_dim_book()
    dim_customer = gen_dim_customer()
    dim_channel  = gen_dim_channel()

    print("\n[2/5] Generating fact tables...")
    fact_sales = gen_fact_sales(dim_date, dim_book, dim_customer, dim_channel)
    fact_inv   = gen_fact_inventory(dim_book, dim_date)

    print("\n[3/5] Injecting cleaning issues...")
    fact_sales, dim_book, dim_customer, dim_channel, fact_inv = inject_issues(
        fact_sales, dim_book, dim_customer, dim_channel, fact_inv
    )

    print("\n[4/5] Saving files...")
    save(dim_date,     f"{STUDENT_DIR}/dim_date.csv")
    save(dim_book,     f"{STUDENT_DIR}/dim_book.csv")
    save(dim_customer, f"{STUDENT_DIR}/dim_customer.csv")
    save(dim_channel,  f"{STUDENT_DIR}/dim_channel.csv")
    save(fact_sales,   f"{STUDENT_DIR}/fact_sales.csv")
    save(fact_inv,     f"{STUDENT_DIR}/fact_inventory.csv")

    with open(f"{OUTPUT_BASE}/data_dictionary.md", "w", encoding="utf-8") as f:
        f.write(DATA_DICT_MD)
    print(f"  Saved {OUTPUT_BASE}/data_dictionary.md")

    notes = {
        "expected_cleaning_tasks.md": CLEANING_MD,
        "suggested_dax_measures.md":  DAX_MD,
        "dashboard_questions.md":     DASHBOARD_MD,
        "model_relationships.md":     MODEL_MD,
    }
    for fname, content in notes.items():
        path = f"{PRIVATE_DIR}/{fname}"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  Saved {path}")

    print("\n[5/5] Validating...")
    validate(fact_sales, fact_inv, dim_date, dim_book, dim_customer, dim_channel)

    print("\n" + "=" * 55)
    print("Done. Output folder: output/dar_al_maaref/")
    print("  student_dataset/          → share with students")
    print("  data_dictionary.md        → share with students")
    print("  private_instructor_notes/ → instructor only")
    print("=" * 55)

if __name__ == "__main__":
    main()

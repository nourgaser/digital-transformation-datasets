"""
ENR (Egyptian National Railways) - Team 07
Dataset Generator for Digital Transformation Course - BINF 402, Spring 2026
GIU - Dr. Nourhan Hamdi
Team: Fayrouz, Logaina, Ali, Hussein, Adam, Yassin
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
fake = Faker("ar_EG")
fake_en = Faker("en_US")
fake_en.seed_instance(SEED)

PROJECT_SLUG = "enr_t07"
OUTPUT_BASE = f"output/{PROJECT_SLUG}"
STUDENT_DIR = f"{OUTPUT_BASE}/student_dataset"
PRIVATE_DIR = f"{OUTPUT_BASE}/private_instructor_notes"

DATE_START = date(2023, 1, 1)
DATE_END   = date(2024, 12, 31)
TARGET_FACT_ROWS = 2000

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
def gen_dim_date():
    rows = []
    d = DATE_START
    while d <= DATE_END:
        rows.append({
            "date_id":      d.strftime("%Y%m%d"),
            "date":         d.strftime("%Y-%m-%d"),   # stored as string intentionally (cleaning task)
            "day":          d.day,
            "month":        d.month,
            "month_name":   d.strftime("%B"),
            "quarter":      (d.month - 1) // 3 + 1,
            "year":         d.year,
            "day_of_week":  d.strftime("%A"),
            "is_weekend":   d.weekday() >= 4,         # Friday–Saturday weekend in Egypt
            "is_holiday":   d in EGYPTIAN_HOLIDAYS,
        })
        d += timedelta(days=1)
    return pd.DataFrame(rows)

EGYPTIAN_HOLIDAYS = {
    date(2023, 1, 7),   # Coptic Christmas
    date(2023, 4, 25),  # Sinai Liberation
    date(2023, 5, 1),   # Labour Day
    date(2023, 6, 30),  # June 30 Revolution
    date(2023, 7, 23),  # Revolution Day
    date(2023, 10, 6),  # Armed Forces Day
    date(2024, 1, 7),
    date(2024, 4, 25),
    date(2024, 5, 1),
    date(2024, 6, 30),
    date(2024, 7, 23),
    date(2024, 10, 6),
}

# ─────────────────────────────────────────────
# DIM ROUTE
# ─────────────────────────────────────────────
ROUTES_RAW = [
    # (route_id, origin, destination, distance_km, region, is_express)
    ("R01", "Cairo",       "Alexandria",  208, "Delta",      True),
    ("R02", "Cairo",       "Luxor",       671, "Upper Egypt", True),
    ("R03", "Cairo",       "Aswan",       878, "Upper Egypt", True),
    ("R04", "Cairo",       "Port Said",   220, "Canal Zone",  False),
    ("R05", "Cairo",       "Suez",        134, "Canal Zone",  False),
    ("R06", "Cairo",       "Mansoura",    120, "Delta",       False),
    ("R07", "Cairo",       "Tanta",        94, "Delta",       False),
    ("R08", "Cairo",       "Minya",       245, "Upper Egypt", False),
    ("R09", "Cairo",       "Asyut",       375, "Upper Egypt", False),
    ("R10", "Cairo",       "Sohag",       467, "Upper Egypt", False),
    ("R11", "Alexandria",  "Luxor",       879, "Upper Egypt", True),
    ("R12", "Alexandria",  "Aswan",      1086, "Upper Egypt", True),
    ("R13", "Cairo",       "Damanhur",    170, "Delta",       False),
    ("R14", "Cairo",       "Beni Suef",   130, "Upper Egypt", False),
    ("R15", "Alexandria",  "Port Said",   290, "Delta",       False),
]

def gen_dim_route():
    rows = []
    for r in ROUTES_RAW:
        rid, origin, dest, dist, region, is_exp = r
        rows.append({
            "route_id":        rid,
            "origin_city":     origin,
            "destination_city": dest,
            "distance_km":     dist,
            "region":          region,
            "is_express":      is_exp,
            "estimated_duration_hrs": round(dist / 90 if is_exp else dist / 70, 1),
        })
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# DIM TRAIN
# ─────────────────────────────────────────────
TRAINS_RAW = [
    # (train_id, name, type, first_cap, second_cap, third_cap)
    ("T01", "Express 901",   "Spanish Express",     40,  80,   0),
    ("T02", "Express 902",   "Spanish Express",     40,  80,   0),
    ("T03", "Talgo 801",     "Talgo",               30,  120,  0),
    ("T04", "Talgo 802",     "Talgo",               30,  120,  0),
    ("T05", "AC Train 501",  "Air-Conditioned",     40,  100, 120),
    ("T06", "AC Train 502",  "Air-Conditioned",     40,  100, 120),
    ("T07", "AC Train 503",  "Air-Conditioned",     40,  100, 120),
    ("T08", "Standard 301",  "Standard",             0,   80, 200),
    ("T09", "Standard 302",  "Standard",             0,   80, 200),
    ("T10", "Standard 303",  "Standard",             0,   80, 200),
]

CLASS_PRICE_BASE = {
    "Spanish Express": {"First": 350, "Second": 200, "Third": None},
    "Talgo":           {"First": 280, "Second": 160, "Third": None},
    "Air-Conditioned": {"First": 180, "Second": 110, "Third":  55},
    "Standard":        {"First": None,"Second":  70, "Third":  35},
}

def gen_dim_train():
    rows = []
    for t in TRAINS_RAW:
        tid, name, ttype, fc, sc, tc = t
        rows.append({
            "train_id":            tid,
            "train_name":          name,
            "train_type":          ttype,
            "first_class_capacity":  fc,
            "second_class_capacity": sc,
            "third_class_capacity":  tc,
            "total_capacity":        fc + sc + tc,
        })
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# DIM CHANNEL
# ─────────────────────────────────────────────
CHANNELS = [
    ("CH01", "Online",  "Website"),
    ("CH02", "Online",  "Mobile App"),
    ("CH03", "Offline", "Station Counter"),
    ("CH04", "Offline", "Fawry"),
    ("CH05", "Offline", "Aman"),
    ("CH06", "Offline", "Vending Machine"),
]

def gen_dim_channel():
    rows = []
    for ch in CHANNELS:
        cid, category, name = ch
        rows.append({
            "channel_id":       cid,
            "channel_name":     name,
            "channel_category": category,
        })
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# FACT TICKET SALES
# ─────────────────────────────────────────────
def get_valid_classes(train_type):
    prices = CLASS_PRICE_BASE[train_type]
    return [cls for cls, p in prices.items() if p is not None]

def seasonality_weight(month):
    """Peaks in summer (Jul-Aug) and winter holidays (Dec-Jan), Ramadan dip."""
    weights = {1:1.3,2:1.0,3:0.95,4:0.85,5:0.9,6:1.1,
               7:1.5,8:1.5,9:1.0,10:1.0,11:0.95,12:1.3}
    return weights.get(month, 1.0)

# Route popularity weights (more passengers on busier routes)
ROUTE_WEIGHT = {
    "R01":8,"R02":7,"R03":6,"R04":3,"R05":2,
    "R06":3,"R07":3,"R08":3,"R09":3,"R10":2,
    "R11":4,"R12":3,"R13":2,"R14":2,"R15":2,
}

# Channel weights per category
CHANNEL_WEIGHTS = {
    "CH01":0.20, "CH02":0.18, "CH03":0.38,
    "CH04":0.10, "CH05":0.07, "CH06":0.07,
}

# Train type × route compatibility
COMPATIBLE_TRAINS = {
    "R01": ["T01","T02","T03","T04","T05","T06","T08","T09"],
    "R02": ["T03","T04","T05","T06","T07","T08","T09"],
    "R03": ["T03","T04","T05","T06","T07","T09","T10"],
    "R04": ["T05","T06","T08","T09","T10"],
    "R05": ["T08","T09","T10"],
    "R06": ["T08","T09","T10"],
    "R07": ["T08","T09","T10"],
    "R08": ["T05","T06","T08","T09"],
    "R09": ["T05","T06","T08","T09","T10"],
    "R10": ["T05","T06","T07","T09","T10"],
    "R11": ["T03","T04","T05","T06"],
    "R12": ["T03","T04","T05","T06","T07"],
    "R13": ["T08","T09","T10"],
    "R14": ["T08","T09","T10"],
    "R15": ["T08","T09","T10"],
}

TRAIN_LOOKUP = {t[0]: t for t in TRAINS_RAW}

def gen_fact_ticket_sales(dim_date, dim_route, dim_train, dim_channel):
    route_ids  = [r[0] for r in ROUTES_RAW]
    route_wts  = [ROUTE_WEIGHT[r] for r in route_ids]
    channel_ids = [ch[0] for ch in CHANNELS]
    channel_wts = [CHANNEL_WEIGHTS[c] for c in channel_ids]

    all_dates = dim_date["date_id"].tolist()
    rows = []
    sale_id = 1

    # Generate ~TARGET_FACT_ROWS transactions
    for _ in range(TARGET_FACT_ROWS):
        # Pick date with seasonality weighting
        date_row = dim_date.sample(1, weights=dim_date["month"].map(seasonality_weight)).iloc[0]
        date_id  = date_row["date_id"]
        month    = date_row["month"]
        year     = date_row["year"]

        # Pick route
        route_id = random.choices(route_ids, weights=route_wts)[0]
        route_row = next(r for r in ROUTES_RAW if r[0] == route_id)
        dist      = route_row[3]

        # Pick compatible train
        compat = COMPATIBLE_TRAINS[route_id]
        train_id = random.choice(compat)
        train_data = TRAIN_LOOKUP[train_id]
        train_type = train_data[2]

        # Pick class
        valid_classes = get_valid_classes(train_type)
        class_wts_map = {"First": 1, "Second": 3, "Third": 5}
        cls_wts = [class_wts_map[c] for c in valid_classes]
        ticket_class = random.choices(valid_classes, weights=cls_wts)[0]

        # Base price
        base_price = CLASS_PRICE_BASE[train_type][ticket_class]
        # Distance adjustment
        price_factor = 1.0 + (dist - 200) / 2000
        ticket_price = round(base_price * price_factor * random.uniform(0.95, 1.05), 2)

        # Quantity (1–4 tickets per transaction)
        qty = random.choices([1, 2, 3, 4], weights=[50, 30, 15, 5])[0]

        # Discount
        discount_pct = random.choices([0, 5, 10, 15, 20],
                                       weights=[55, 20, 12, 8, 5])[0]
        discount_amt = round(ticket_price * qty * discount_pct / 100, 2)
        revenue      = round(ticket_price * qty - discount_amt, 2)

        # Channel
        channel_id = random.choices(channel_ids, weights=channel_wts)[0]

        # Status: mostly completed, ~5% cancelled
        status = random.choices(["Completed", "Cancelled"], weights=[95, 5])[0]
        if status == "Cancelled":
            revenue = 0.0

        # Payment method
        pay_map = {
            "CH01": ["Credit Card", "Debit Card", "Instapay"],
            "CH02": ["Credit Card", "Debit Card", "Instapay", "Wallet"],
            "CH03": ["Cash", "Credit Card"],
            "CH04": ["Cash"],
            "CH05": ["Cash"],
            "CH06": ["Credit Card", "Debit Card"],
        }
        payment_method = random.choice(pay_map[channel_id])

        rows.append({
            "sale_id":         f"S{sale_id:05d}",
            "date_id":         date_id,
            "route_id":        route_id,
            "train_id":        train_id,
            "channel_id":      channel_id,
            "ticket_class":    ticket_class,
            "tickets_sold":    qty,
            "ticket_price":    ticket_price,
            "discount_pct":    discount_pct,
            "discount_amount": discount_amt,
            "total_revenue":   revenue,
            "payment_method":  payment_method,
            "booking_status":  status,
        })
        sale_id += 1

    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# INJECT CLEANING ISSUES
# ─────────────────────────────────────────────
def inject_issues(df_sales, df_route, df_train, df_channel):
    n = len(df_sales)
    rng = np.random.default_rng(SEED + 1)

    # 1. ~5% nulls in discount_pct
    null_idx = rng.choice(n, size=int(n * 0.05), replace=False)
    df_sales.loc[null_idx, "discount_pct"] = np.nan

    # 2. ~4% nulls in payment_method
    null_idx2 = rng.choice(n, size=int(n * 0.04), replace=False)
    df_sales.loc[null_idx2, "payment_method"] = np.nan

    # 3. Inconsistent casing in ticket_class (~3%)
    case_idx = rng.choice(n, size=int(n * 0.03), replace=False)
    df_sales.loc[case_idx, "ticket_class"] = df_sales.loc[case_idx, "ticket_class"].str.lower()

    # 4. Whitespace in booking_status (~2%)
    ws_idx = rng.choice(n, size=int(n * 0.02), replace=False)
    df_sales.loc[ws_idx, "booking_status"] = " " + df_sales.loc[ws_idx, "booking_status"] + " "

    # 5. Inconsistent channel name variants in a new raw column
    variant_map = {"Website": ["Website", "website", "Web Site", "WEBSITE"],
                   "Mobile App": ["Mobile App", "mobile app", "MobileApp", "Mobile app"],
                   "Station Counter": ["Station Counter", "station counter", "Counter"],
                   "Fawry": ["Fawry", "fawry", "FAWRY"],
                   "Aman": ["Aman", "aman"],
                   "Vending Machine": ["Vending Machine", "vending machine", "Machine"]}

    # 6. total_revenue stored as string in ~3% of rows
    str_idx = rng.choice(n, size=int(n * 0.03), replace=False)
    df_sales["total_revenue"] = df_sales["total_revenue"].astype(object)
    for i in str_idx:
        df_sales.at[i, "total_revenue"] = str(df_sales.at[i, "total_revenue"])

    # 7. Duplicate rows (~1.5%)
    dup_idx = rng.choice(n, size=int(n * 0.015), replace=False)
    dups = df_sales.iloc[dup_idx].copy()
    df_sales = pd.concat([df_sales, dups], ignore_index=True)

    # 8. A few impossible ticket_price values (negative — clearly wrong)
    bad_idx = rng.choice(len(df_sales), size=4, replace=False)
    for i in bad_idx:
        df_sales.at[i, "ticket_price"] = -abs(df_sales.at[i, "ticket_price"])

    # 9. date_id stored as integer in fact table (should be string FK — type mismatch)
    # Already stored as "YYYYMMDD" string — that's fine, date column itself is str (cleaning task noted)

    # Route dim: inconsistent region casing
    df_route.loc[df_route["route_id"].isin(["R04","R05"]), "region"] = "canal zone"

    # Train dim: whitespace in train_type for 2 rows
    df_train.loc[df_train["train_id"].isin(["T08","T09"]), "train_type"] = " Standard"

    return df_sales, df_route, df_train, df_channel

# ─────────────────────────────────────────────
# VALIDATION
# ─────────────────────────────────────────────
def validate(df_sales, dim_date, dim_route, dim_train, dim_channel):
    errors = []
    valid_dates   = set(dim_date["date_id"])
    valid_routes  = set(dim_route["route_id"])
    valid_trains  = set(dim_train["train_id"])
    valid_channels = set(dim_channel["channel_id"])

    bad_dates    = df_sales[~df_sales["date_id"].isin(valid_dates)]
    bad_routes   = df_sales[~df_sales["route_id"].isin(valid_routes)]
    bad_trains   = df_sales[~df_sales["train_id"].isin(valid_trains)]
    bad_channels = df_sales[~df_sales["channel_id"].isin(valid_channels)]

    if len(bad_dates):    errors.append(f"  Bad date_id:    {len(bad_dates)} rows")
    if len(bad_routes):   errors.append(f"  Bad route_id:   {len(bad_routes)} rows")
    if len(bad_trains):   errors.append(f"  Bad train_id:   {len(bad_trains)} rows")
    if len(bad_channels): errors.append(f"  Bad channel_id: {len(bad_channels)} rows")

    n = len(df_sales)
    if n < 1800 or n > 3000:
        errors.append(f"  Row count out of expected range: {n}")

    null_pct = df_sales["discount_pct"].isna().mean()
    if null_pct < 0.02:
        errors.append(f"  Null % in discount_pct too low: {null_pct:.1%}")

    dups = df_sales.duplicated(subset=["sale_id"]).sum()
    # duplicates introduced intentionally — just check they exist
    actual_dups = df_sales.duplicated().sum()

    if errors:
        print("\nVALIDATION WARNINGS:")
        for e in errors: print(e)
    else:
        print("\nValidation passed.")

    print(f"  Total fact rows (incl. injected dupes): {n}")
    print(f"  Intentional duplicate rows:             {actual_dups}")
    print(f"  Null rate in discount_pct:              {null_pct:.1%}")
    print(f"  Null rate in payment_method:            {df_sales['payment_method'].isna().mean():.1%}")

# ─────────────────────────────────────────────
# WRITE INSTRUCTOR NOTES
# ─────────────────────────────────────────────
CLEANING_MD = """\
# Expected Cleaning Tasks — ENR T07

## fact_ticket_sales.csv

| # | Issue | Column | Approx. Rate |
|---|-------|--------|--------------|
| 1 | Missing values | `discount_pct` | ~5% nulls |
| 2 | Missing values | `payment_method` | ~4% nulls |
| 3 | Inconsistent casing | `ticket_class` | ~3% stored as lowercase ("first", "second") |
| 4 | Leading/trailing whitespace | `booking_status` | ~2% |
| 5 | Mixed data type | `total_revenue` | ~3% stored as text strings instead of numeric |
| 6 | Negative impossible values | `ticket_price` | 4 rows with negative prices |
| 7 | Duplicate rows | all columns | ~1.5% fully duplicated records |

## dim_route.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 8 | Inconsistent casing | `region` | "canal zone" (lowercase) for R04, R05 — should be "Canal Zone" |

## dim_train.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 9 | Leading whitespace | `train_type` | " Standard" (space before) for T08, T09 |

## dim_date.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 10 | Date stored as string | `date` | Column is text "YYYY-MM-DD", not a Date type — students must convert in Power Query |

## Notes for Instructor
- `total_revenue` type mismatch (string vs number) is the trickiest issue — students must use "Replace Errors" or "Change Type" in Power Query.
- Negative `ticket_price` values look subtle — students should catch them with a Min check or a filter visual.
- Duplicate rows have no `sale_id` collision — they are exact row duplicates, so students must use "Remove Duplicates" on all columns.
"""

DAX_MD = """\
# Suggested DAX Measures — ENR T07

## Revenue & Sales
```dax
Total Revenue =
    CALCULATE(
        SUM(fact_ticket_sales[total_revenue]),
        fact_ticket_sales[booking_status] = "Completed"
    )

Total Tickets Sold =
    CALCULATE(
        SUM(fact_ticket_sales[tickets_sold]),
        fact_ticket_sales[booking_status] = "Completed"
    )

Average Ticket Price =
    DIVIDE([Total Revenue], [Total Tickets Sold])

Total Transactions =
    COUNTROWS(fact_ticket_sales)

Cancellation Rate =
    DIVIDE(
        COUNTROWS(FILTER(fact_ticket_sales, fact_ticket_sales[booking_status] = "Cancelled")),
        [Total Transactions]
    )
```

## Growth & Time Intelligence
```dax
Revenue MoM Growth % =
    VAR PrevMonth = CALCULATE([Total Revenue], DATEADD(dim_date[date], -1, MONTH))
    RETURN DIVIDE([Total Revenue] - PrevMonth, PrevMonth)

YTD Revenue =
    TOTALYTD([Total Revenue], dim_date[date])

Revenue Previous Year =
    CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(dim_date[date]))

YoY Revenue Growth % =
    DIVIDE([Total Revenue] - [Revenue Previous Year], [Revenue Previous Year])
```

## Occupancy
```dax
-- Occupancy Rate: tickets sold vs theoretical capacity per transaction
-- (requires knowing capacity per class per train — use dim_train)
Occupancy Rate =
    DIVIDE([Total Tickets Sold],
           SUMX(fact_ticket_sales,
               SWITCH(fact_ticket_sales[ticket_class],
                   "First",  RELATED(dim_train[first_class_capacity]),
                   "Second", RELATED(dim_train[second_class_capacity]),
                   "Third",  RELATED(dim_train[third_class_capacity])
               )
           )
    )
```

## Channel Analysis
```dax
Online Revenue =
    CALCULATE([Total Revenue],
        RELATED(dim_channel[channel_category]) = "Online"
    )

Offline Revenue =
    CALCULATE([Total Revenue],
        RELATED(dim_channel[channel_category]) = "Offline"
    )

Online Revenue % =
    DIVIDE([Online Revenue], [Total Revenue])
```

## Route Analysis
```dax
Revenue Per KM =
    DIVIDE([Total Revenue], SUM(dim_route[distance_km]))
```
"""

DASHBOARD_MD = """\
# Dashboard Questions & Visual Suggestions — ENR T07

## Analytical Questions (student-facing prompts)
1. Which routes generate the most total revenue?
2. How does ticket revenue change month-over-month and year-over-year?
3. Which ticket class (First / Second / Third) contributes the most to revenue and volume?
4. How does online channel performance compare to offline?
5. Which booking channel (Website, App, Fawry, etc.) sells the most tickets?
6. What is the cancellation rate, and does it vary by route or class?
7. How does occupancy rate vary by train type and route?
8. What is the revenue split between express and standard services?

## Suggested Visuals (instructor only)

| Visual | Type | Fields |
|--------|------|--------|
| Total Revenue KPI card | Card | [Total Revenue] |
| Total Tickets Sold KPI card | Card | [Total Tickets Sold] |
| Revenue Growth % KPI card | Card | [Revenue MoM Growth %] |
| Occupancy Rate KPI card | Card | [Occupancy Rate] |
| Revenue by Route | Bar chart | dim_route[origin_city] + destination, [Total Revenue] |
| Tickets by Class | Pie/Donut | fact[ticket_class], [Total Tickets Sold] |
| Sales over Time | Line chart | dim_date[month], [Total Revenue] — with year slicer |
| Online vs Offline | Clustered bar | dim_channel[channel_category], [Total Revenue] |
| Channel breakdown | Stacked bar | dim_channel[channel_name], [Total Revenue] |
| Revenue by Train Type | Bar | dim_train[train_type], [Total Revenue] |
| YoY Revenue | Line | dim_date[year+month], [Total Revenue] + [Revenue Previous Year] |
| Cancellation Rate | Card / Gauge | [Cancellation Rate] |

## Suggested Slicers
- Year
- Month
- Route
- Ticket Class
- Channel Category (Online / Offline)
- Train Type
"""

MODEL_MD = """\
# Star Schema Relationships — ENR T07

## Tables
- **fact_ticket_sales** — central fact table (~2,000+ rows after cleaning)
- **dim_date** — date dimension
- **dim_route** — route dimension
- **dim_train** — train dimension
- **dim_channel** — booking channel dimension

## Relationships

| Fact Column | → | Dimension Table | Dimension Column | Cardinality | Filter Direction |
|-------------|---|-----------------|-----------------|-------------|-----------------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single (dim → fact) |
| `route_id` | → | `dim_route` | `route_id` | Many-to-One | Single (dim → fact) |
| `train_id` | → | `dim_train` | `train_id` | Many-to-One | Single (dim → fact) |
| `channel_id` | → | `dim_channel` | `channel_id` | Many-to-One | Single (dim → fact) |

## Notes
- All relationships are standard **one-to-many** from dimension PK to fact FK.
- Filter direction should be **single** (dimension → fact) for correct measure context.
- No many-to-many relationships.
- `dim_date[date]` must be marked as a **Date Table** in Power BI for time intelligence DAX to work.
- After cleaning, `total_revenue` must be a **Decimal Number** type for SUM to work.
"""

DATA_DICT_MD = """\
# Data Dictionary — Egyptian National Railways (ENR)
## Digital Transformation Course · BINF 402 · GIU · Spring 2026

---

## Business Story
This dataset represents **ticket sales transactions** for Egyptian National Railways (ENR) over 2023–2024.
The data covers passenger journeys across key Egyptian routes, split by train type, ticket class, and booking channel.
Your goal as a Sales Manager is to understand revenue trends, identify high-performing routes and channels, and track occupancy.

---

## Files

### `fact_ticket_sales.csv` (main fact table)
| Column | Description |
|--------|-------------|
| `sale_id` | Unique transaction identifier |
| `date_id` | Foreign key → `dim_date.date_id` (format: YYYYMMDD) |
| `route_id` | Foreign key → `dim_route.route_id` |
| `train_id` | Foreign key → `dim_train.train_id` |
| `channel_id` | Foreign key → `dim_channel.channel_id` |
| `ticket_class` | Class of service: First, Second, or Third |
| `tickets_sold` | Number of tickets in this transaction |
| `ticket_price` | Price per single ticket (EGP) |
| `discount_pct` | Discount percentage applied (0–20%) |
| `discount_amount` | Total discount value (EGP) |
| `total_revenue` | Net revenue for this transaction (EGP) |
| `payment_method` | Payment method used |
| `booking_status` | Completed or Cancelled |

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

### `dim_route.csv`
| Column | Description |
|--------|-------------|
| `route_id` | Primary key |
| `origin_city` | Departure city |
| `destination_city` | Arrival city |
| `distance_km` | Route distance in kilometers |
| `region` | Geographic region served |
| `is_express` | Whether the route has express service |
| `estimated_duration_hrs` | Approximate travel time |

### `dim_train.csv`
| Column | Description |
|--------|-------------|
| `train_id` | Primary key |
| `train_name` | Train service name |
| `train_type` | Type: Spanish Express, Talgo, Air-Conditioned, Standard |
| `first_class_capacity` | Number of First Class seats |
| `second_class_capacity` | Number of Second Class seats |
| `third_class_capacity` | Number of Third Class seats |
| `total_capacity` | Total seats across all classes |

### `dim_channel.csv`
| Column | Description |
|--------|-------------|
| `channel_id` | Primary key |
| `channel_name` | Specific channel (e.g. Website, Fawry) |
| `channel_category` | Online or Offline |

---

## Intended Relationships
- `fact_ticket_sales.date_id` → `dim_date.date_id`
- `fact_ticket_sales.route_id` → `dim_route.route_id`
- `fact_ticket_sales.train_id` → `dim_train.train_id`
- `fact_ticket_sales.channel_id` → `dim_channel.channel_id`

## Notes for Students
- The data **requires cleaning** before analysis — check for inconsistencies, wrong types, and missing values.
- Build a **star schema** in Power BI with `fact_ticket_sales` at the center.
- Use the date table for **time intelligence** measures (MoM, YTD, YoY).
"""

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print("=" * 55)
    print("ENR T07 — Dataset Generator")
    print("=" * 55)
    make_dirs()

    print("\n[1/4] Generating dimension tables...")
    dim_date    = gen_dim_date()
    dim_route   = gen_dim_route()
    dim_train   = gen_dim_train()
    dim_channel = gen_dim_channel()

    print("\n[2/4] Generating fact table...")
    fact_sales = gen_fact_ticket_sales(dim_date, dim_route, dim_train, dim_channel)

    print("\n[3/4] Injecting cleaning issues...")
    fact_sales, dim_route, dim_train, dim_channel = inject_issues(
        fact_sales, dim_route, dim_train, dim_channel
    )

    print("\n[4/4] Saving files...")
    save(dim_date,    f"{STUDENT_DIR}/dim_date.csv")
    save(dim_route,   f"{STUDENT_DIR}/dim_route.csv")
    save(dim_train,   f"{STUDENT_DIR}/dim_train.csv")
    save(dim_channel, f"{STUDENT_DIR}/dim_channel.csv")
    save(fact_sales,  f"{STUDENT_DIR}/fact_ticket_sales.csv")

    # Data dictionary
    with open(f"{OUTPUT_BASE}/data_dictionary.md", "w", encoding="utf-8") as f:
        f.write(DATA_DICT_MD)
    print(f"  Saved {OUTPUT_BASE}/data_dictionary.md")

    # Private instructor notes
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

    validate(fact_sales, dim_date, dim_route, dim_train, dim_channel)

    print("\n" + "=" * 55)
    print("Done. Output folder: output/enr_t07/")
    print("  student_dataset/         → share with students")
    print("  data_dictionary.md       → share with students")
    print("  private_instructor_notes/ → instructor only")
    print("=" * 55)

if __name__ == "__main__":
    main()

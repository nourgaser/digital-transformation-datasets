"""
Misr Spinning and Weaving Company (MSW)
Textile Manufacturer, El Mahalla El Kubra, Egypt
Dataset Generator — BINF 402, Digital Transformation, GIU, Spring 2026
Dr. Nourhan Hamdi
Team: Mohamed Tamer, Mohamed Khairy, Ahmed Elkassas, Yassin Azhary, John Amgad, Adham Ragai (T7/6)
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

PROJECT_SLUG = "msw"
OUTPUT_BASE  = f"output/{PROJECT_SLUG}"
STUDENT_DIR  = f"{OUTPUT_BASE}/student_dataset"
PRIVATE_DIR  = f"{OUTPUT_BASE}/private_instructor_notes"

DATE_START = date(2023, 1, 1)
DATE_END   = date(2024, 12, 31)
TARGET_SALES_ROWS      = 2000
TARGET_PRODUCTION_ROWS = 360   # 15 lines × 24 months

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def make_dirs():
    os.makedirs(STUDENT_DIR, exist_ok=True)
    os.makedirs(PRIVATE_DIR, exist_ok=True)

def save(df, path):
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
            "date":        d.strftime("%Y-%m-%d"),   # string — cleaning task
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
# DIM PRODUCT
# ─────────────────────────────────────────────
PRODUCTS_RAW = [
    # (id, name, category, fiber_type, unit_of_measure, base_price_egp)
    ("PR01", "Carded Yarn 20s",        "Yarn",            "100% Egyptian Cotton", "kg",    110),
    ("PR02", "Combed Yarn 40s",        "Yarn",            "100% Egyptian Cotton", "kg",    145),
    ("PR03", "Cotton-Polyester Yarn",  "Yarn",            "Cotton Blend",         "kg",     85),
    ("PR04", "Grey Fabric Standard",   "Grey Fabric",     "100% Egyptian Cotton", "meter",  42),
    ("PR05", "Grey Fabric Heavy",      "Grey Fabric",     "100% Egyptian Cotton", "meter",  58),
    ("PR06", "Grey Fabric Blend",      "Grey Fabric",     "Cotton Blend",         "meter",  35),
    ("PR07", "Dyed Fabric Solid",      "Finished Fabric", "100% Egyptian Cotton", "meter",  80),
    ("PR08", "Printed Fabric",         "Finished Fabric", "100% Egyptian Cotton", "meter",  95),
    ("PR09", "Finished Fabric Blend",  "Finished Fabric", "Cotton Blend",         "meter",  65),
    ("PR10", "Cotton Towel Set",       "Garment",         "100% Egyptian Cotton", "piece", 210),
    ("PR11", "Cotton Bed Sheet Set",   "Garment",         "100% Egyptian Cotton", "piece", 380),
    ("PR12", "Cotton T-Shirt",         "Garment",         "100% Egyptian Cotton", "piece", 160),
    ("PR13", "Cotton Work Uniform",    "Garment",         "Cotton Blend",         "piece", 190),
    ("PR14", "Denim Fabric",           "Finished Fabric", "Cotton Blend",         "meter",  72),
    ("PR15", "Medical Cotton Gauze",   "Yarn",            "100% Egyptian Cotton", "kg",     95),
    ("PR16", "High-Thread Percale",    "Finished Fabric", "100% Egyptian Cotton", "meter", 115),
]

PRODUCT_WEIGHTS = [12, 8, 7, 10, 7, 6, 8, 6, 5, 7, 5, 8, 5, 4, 3, 3]

def gen_dim_product():
    rows = [{
        "product_id":      p[0],
        "product_name":    p[1],
        "category":        p[2],
        "fiber_type":      p[3],
        "unit_of_measure": p[4],
        "base_price_egp":  p[5],
    } for p in PRODUCTS_RAW]
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# DIM CUSTOMER
# ─────────────────────────────────────────────
CUSTOMER_TYPES   = ["Local Retailer", "Garment Manufacturer", "Wholesaler",
                    "Government/Military", "Export Buyer"]
CUSTOMER_WEIGHTS_C = [25, 20, 20, 10, 25]

EXPORT_COUNTRIES = ["Germany", "Italy", "USA", "UK", "Saudi Arabia", "UAE", "Turkey", "France"]
EGYPT_GOVS       = ["Cairo", "Giza", "Alexandria", "Mansoura", "Tanta", "Gharbia",
                    "Dakahlia", "Port Said", "Ismailia", "Suez", "Asyut", "Minya"]

def gen_dim_customer(n=120):
    rows = []
    for i in range(1, n + 1):
        ctype = random.choices(CUSTOMER_TYPES, weights=CUSTOMER_WEIGHTS_C)[0]
        if ctype == "Export Buyer":
            name    = fake_en.company()
            country = random.choice(EXPORT_COUNTRIES)
            gov     = None
            market  = "Export"
        else:
            if ctype in ("Garment Manufacturer", "Wholesaler", "Government/Military"):
                name = fake_en.company()
            else:
                name = fake_en.name()
            country = "Egypt"
            gov     = random.choice(EGYPT_GOVS)
            market  = "Domestic"
        rows.append({
            "customer_id":   f"CUS{i:04d}",
            "customer_name": name,
            "customer_type": ctype,
            "market":        market,
            "country":       country,
            "governorate":   gov,
        })
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# DIM CHANNEL
# ─────────────────────────────────────────────
CHANNELS = [
    ("CH01", "Direct Sales",      "Domestic"),
    ("CH02", "Distributor",       "Domestic"),
    ("CH03", "Export Agent",      "International"),
    ("CH04", "Government Tender", "Domestic"),
    ("CH05", "E-commerce",        "Domestic"),
    ("CH06", "Trade Fair",        "International"),
]

def gen_dim_channel():
    rows = [{"channel_id": c[0], "channel_name": c[1], "channel_type": c[2]}
            for c in CHANNELS]
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# DIM PRODUCTION LINE
# ─────────────────────────────────────────────
PRODUCTION_LINES_RAW = [
    # (id, name, department, type, capacity_kg_day, status)
    ("PL01", "Spinning Line A",   "Spinning",  "Carding",       8000, "Active"),
    ("PL02", "Spinning Line B",   "Spinning",  "Combing",       6000, "Active"),
    ("PL03", "Spinning Line C",   "Spinning",  "Open-End",      9000, "Active"),
    ("PL04", "Spinning Line D",   "Spinning",  "Ring Spinning", 5000, "Active"),
    ("PL05", "Weaving Hall 1",    "Weaving",   "Shuttle Loom",  5000, "Active"),
    ("PL06", "Weaving Hall 2",    "Weaving",   "Rapier Loom",   7000, "Active"),
    ("PL07", "Weaving Hall 3",    "Weaving",   "Air-Jet Loom",  8500, "Active"),
    ("PL08", "Weaving Hall 4",    "Weaving",   "Shuttle Loom",  4500, "Partial"),
    ("PL09", "Weaving Hall 5",    "Weaving",   "Rapier Loom",   6500, "Active"),
    ("PL10", "Finishing Unit 1",  "Finishing", "Dyeing",        4000, "Active"),
    ("PL11", "Finishing Unit 2",  "Finishing", "Printing",      3500, "Active"),
    ("PL12", "Finishing Unit 3",  "Finishing", "Bleaching",     5000, "Active"),
    ("PL13", "Garment Factory 1", "Garment",   "Cut-and-Sew",   2000, "Active"),
    ("PL14", "Garment Factory 2", "Garment",   "Knitwear",      1800, "Active"),
    ("PL15", "Garment Factory 3", "Garment",   "Home Textile",  2200, "Active"),
]

def gen_dim_production_line():
    rows = [{
        "line_id":             p[0],
        "line_name":           p[1],
        "department":          p[2],
        "production_type":     p[3],
        "capacity_kg_per_day": p[4],
        "operational_status":  p[5],
        "location":            "El Mahalla El Kubra",
    } for p in PRODUCTION_LINES_RAW]
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# FACT SALES
# ─────────────────────────────────────────────
def channel_weights(year):
    if year == 2023:
        return {"CH01": 0.30, "CH02": 0.25, "CH03": 0.20, "CH04": 0.12, "CH05": 0.08, "CH06": 0.05}
    else:   # 2024: e-commerce grows, digital adoption from ERP rollout
        return {"CH01": 0.27, "CH02": 0.22, "CH03": 0.20, "CH04": 0.10, "CH05": 0.15, "CH06": 0.06}

def sales_seasonality(month):
    # Textile peaks Sep–Nov (winter prep), trough Jun–Jul
    return {
        1: 1.10, 2: 1.00, 3: 1.05, 4: 1.00, 5: 0.90, 6: 0.75,
        7: 0.70, 8: 0.80, 9: 1.15, 10: 1.30, 11: 1.25, 12: 1.10,
    }.get(month, 1.0)

QUANTITY_RANGES = {
    "Yarn": {
        "Export Buyer":         (2000, 15000),
        "Garment Manufacturer": (1000,  8000),
        "Wholesaler":           ( 500,  3000),
        "Local Retailer":       ( 100,   800),
        "Government/Military":  ( 500,  5000),
    },
    "Grey Fabric": {
        "Export Buyer":         (3000, 20000),
        "Garment Manufacturer": (1000, 10000),
        "Wholesaler":           ( 500,  4000),
        "Local Retailer":       ( 100,  1000),
        "Government/Military":  (1000,  8000),
    },
    "Finished Fabric": {
        "Export Buyer":         (2000, 12000),
        "Garment Manufacturer": ( 500,  5000),
        "Wholesaler":           ( 300,  3000),
        "Local Retailer":       (  50,   500),
        "Government/Military":  ( 500,  4000),
    },
    "Garment": {
        "Export Buyer":         ( 500,  5000),
        "Garment Manufacturer": ( 200,  2000),
        "Wholesaler":           ( 100,  1500),
        "Local Retailer":       (  20,   300),
        "Government/Military":  ( 200,  3000),
    },
}

PRODUCT_LOOKUP = {p[0]: p for p in PRODUCTS_RAW}
ORDER_STATUSES = ["Completed", "Pending", "Cancelled", "Returned"]
ORDER_WEIGHTS  = [84, 8, 5, 3]

def gen_fact_sales(dim_date, dim_product, dim_customer, dim_channel):
    rng = np.random.default_rng(SEED + 20)
    prod_ids  = [p[0] for p in PRODUCTS_RAW]
    ch_ids    = [c[0] for c in CHANNELS]
    cust_ids  = dim_customer["customer_id"].tolist()
    ctype_map  = dim_customer.set_index("customer_id")["customer_type"].to_dict()
    market_map = dim_customer.set_index("customer_id")["market"].to_dict()

    rows    = []
    sale_id = 1

    for _ in range(TARGET_SALES_ROWS):
        prod_id    = random.choices(prod_ids, weights=PRODUCT_WEIGHTS)[0]
        prod       = PRODUCT_LOOKUP[prod_id]
        category   = prod[2]
        base_price = prod[5]

        # Date weighted by seasonality
        date_df  = dim_date.copy()
        date_df["w"] = date_df["month"].map(sales_seasonality)
        date_row = date_df.sample(1, weights="w").iloc[0]
        date_id  = date_row["date_id"]
        year     = int(date_row["year"])

        # Price: ~18% inflation in 2024 (EGP devaluation)
        year_factor = 1.0 if year == 2023 else 1.18
        unit_price  = round(base_price * year_factor * float(rng.uniform(0.93, 1.07)), 1)

        # Customer
        customer_id   = str(rng.choice(cust_ids))
        customer_type = ctype_map[customer_id]
        market        = market_map[customer_id]

        # Quantity depends on customer type × product category
        qty_range = QUANTITY_RANGES.get(category, {}).get(customer_type, (100, 1000))
        quantity  = int(rng.integers(qty_range[0], qty_range[1]))

        # Discount: export and government get higher rates
        if customer_type == "Export Buyer":
            discount_pct = round(float(rng.uniform(0.08, 0.18)), 3)
        elif customer_type == "Government/Military":
            discount_pct = round(float(rng.uniform(0.05, 0.12)), 3)
        else:
            discount_pct = round(float(rng.uniform(0.00, 0.07)), 3)

        total_revenue = round(quantity * unit_price * (1 - discount_pct), 1)

        cw         = channel_weights(year)
        channel_id = random.choices(ch_ids, weights=list(cw.values()))[0]

        order_status = random.choices(ORDER_STATUSES, weights=ORDER_WEIGHTS)[0]
        if order_status in ("Cancelled", "Returned"):
            total_revenue = 0.0

        rows.append({
            "sale_id":           f"SL{sale_id:05d}",
            "date_id":           date_id,
            "product_id":        prod_id,
            "customer_id":       customer_id,
            "channel_id":        channel_id,
            "quantity":          quantity,
            "unit_price_egp":    unit_price,
            "discount_pct":      discount_pct,
            "total_revenue_egp": total_revenue,
            "order_status":      order_status,
            "market":            market,
        })
        sale_id += 1

    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# FACT PRODUCTION (monthly snapshot per line)
# ─────────────────────────────────────────────
def gen_fact_production(dim_date, dim_production_line):
    rng = np.random.default_rng(SEED + 30)
    months = (dim_date[dim_date["day"] == 1][["date_id", "month", "year"]]
              .copy().reset_index(drop=True))

    dept_defect_range = {
        "Spinning":  (1.5, 4.0),
        "Weaving":   (2.0, 5.5),
        "Finishing": (2.5, 6.0),
        "Garment":   (3.0, 7.0),
    }

    def prod_seasonality(month):
        # Lower output in summer heat, higher in Q4
        return {
            1: 1.05, 2: 1.00, 3: 1.05, 4: 1.00, 5: 0.95, 6: 0.85,
            7: 0.80, 8: 0.82, 9: 0.95, 10: 1.05, 11: 1.10, 12: 1.08,
        }.get(month, 1.0)

    rows   = []
    row_id = 1

    for _, line_row in dim_production_line.iterrows():
        lid        = line_row["line_id"]
        dept       = line_row["department"]
        capacity   = line_row["capacity_kg_per_day"]
        is_partial = line_row["operational_status"] == "Partial"
        d_lo, d_hi = dept_defect_range[dept]

        for _, mrow in months.iterrows():
            month_num = int(mrow["month"])

            working_days = (int(rng.integers(18, 24))
                            if month_num not in (7, 8)
                            else int(rng.integers(14, 20)))
            season_factor = prod_seasonality(month_num)
            cap_factor    = (float(rng.uniform(0.60, 0.75)) if is_partial
                             else float(rng.uniform(0.82, 0.96)))
            planned_output = round(capacity * working_days * season_factor * cap_factor)

            efficiency_pct = round(
                float(rng.uniform(60, 82)) if is_partial else float(rng.uniform(78, 97)), 1
            )
            actual_output   = round(planned_output * efficiency_pct / 100)

            defect_rate_pct = round(float(rng.uniform(d_lo, d_hi)), 2)
            defect_qty      = round(actual_output * defect_rate_pct / 100)

            downtime_hours  = round(
                float(rng.uniform(20, 80)) if is_partial else float(rng.uniform(0, 40)), 1
            )

            if efficiency_pct > 93:
                status = "At Capacity"
            elif downtime_hours > 30:
                status = "Under Maintenance"
            else:
                status = "Normal"

            rows.append({
                "production_id":     f"PROD{row_id:05d}",
                "date_id":           mrow["date_id"],
                "line_id":           lid,
                "working_days":      working_days,
                "planned_output_kg": planned_output,
                "actual_output_kg":  actual_output,
                "efficiency_pct":    efficiency_pct,
                "defect_qty_kg":     defect_qty,
                "defect_rate_pct":   defect_rate_pct,
                "downtime_hours":    downtime_hours,
                "production_status": status,
            })
            row_id += 1

    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# INJECT CLEANING ISSUES
# ─────────────────────────────────────────────
def inject_issues(df_sales, df_prod, df_customer, df_product, df_line):
    n   = len(df_sales)
    np_ = len(df_prod)
    rng = np.random.default_rng(SEED + 99)

    # ── fact_sales ────────────────────────────
    # 1. ~5% nulls in discount_pct
    idx1 = rng.choice(n, size=int(n * 0.05), replace=False)
    df_sales.loc[idx1, "discount_pct"] = np.nan

    # 2. ~4% nulls in quantity
    idx2 = rng.choice(n, size=int(n * 0.04), replace=False)
    df_sales.loc[idx2, "quantity"] = np.nan

    # 3. Inconsistent casing in order_status (~3%)
    idx3 = rng.choice(n, size=int(n * 0.03), replace=False)
    df_sales.loc[idx3, "order_status"] = df_sales.loc[idx3, "order_status"].str.upper()

    # 4. total_revenue_egp stored as string ~3% — cast to object first
    df_sales["total_revenue_egp"] = df_sales["total_revenue_egp"].astype(object)
    idx4 = rng.choice(n, size=int(n * 0.03), replace=False)
    for i in idx4:
        df_sales.at[i, "total_revenue_egp"] = str(df_sales.at[i, "total_revenue_egp"])

    # 5. Negative total_revenue_egp (impossible) — 4 rows
    bad = rng.choice(n, size=4, replace=False)
    for i in bad:
        val = df_sales.at[i, "total_revenue_egp"]
        df_sales.at[i, "total_revenue_egp"] = -abs(float(val))

    # 6. Trailing whitespace in market (~2%)
    idx6 = rng.choice(n, size=int(n * 0.02), replace=False)
    df_sales.loc[idx6, "market"] = df_sales.loc[idx6, "market"] + " "

    # 7. Duplicate rows (~1.5%)
    dup_idx  = rng.choice(n, size=int(n * 0.015), replace=False)
    dups     = df_sales.iloc[dup_idx].copy()
    df_sales = pd.concat([df_sales, dups], ignore_index=True)

    # ── fact_production ───────────────────────
    # 8. ~5% nulls in downtime_hours
    idx8 = rng.choice(np_, size=int(np_ * 0.05), replace=False)
    df_prod.loc[idx8, "downtime_hours"] = np.nan

    # 9. Inconsistent casing in production_status (~3%)
    idx9 = rng.choice(np_, size=int(np_ * 0.03), replace=False)
    df_prod.loc[idx9, "production_status"] = df_prod.loc[idx9, "production_status"].str.upper()

    # ── dim_customer ───────────────────────────
    # 10. Inconsistent customer_type casing for 4 rows
    s_idx = df_customer.sample(4, random_state=SEED).index
    df_customer.loc[s_idx, "customer_type"] = df_customer.loc[s_idx, "customer_type"].str.lower()

    # ── dim_product ────────────────────────────
    # 11. Trailing whitespace in category for 3 rows
    df_product.loc[df_product["product_id"].isin(["PR10", "PR11", "PR12"]), "category"] = "Garment "

    # ── dim_production_line ────────────────────
    # 12. Inconsistent casing in production_type for 2 rows
    df_line.loc[df_line["line_id"].isin(["PL08", "PL09"]), "production_type"] = \
        df_line.loc[df_line["line_id"].isin(["PL08", "PL09"]), "production_type"].str.lower()

    return df_sales, df_prod, df_customer, df_product, df_line

# ─────────────────────────────────────────────
# VALIDATION
# ─────────────────────────────────────────────
def validate(df_sales, df_prod, dim_date, dim_product, dim_customer, dim_channel, dim_line):
    print("\nValidation:")
    valid_dates = set(dim_date["date_id"])
    valid_prod  = set(dim_product["product_id"])
    valid_cust  = set(dim_customer["customer_id"])
    valid_ch    = set(dim_channel["channel_id"])
    valid_lines = set(dim_line["line_id"])

    errors = []
    for col, valid, lbl in [
        ("date_id",    valid_dates, "sales date_id"),
        ("product_id", valid_prod,  "sales product_id"),
        ("customer_id",valid_cust,  "sales customer_id"),
        ("channel_id", valid_ch,    "sales channel_id"),
    ]:
        bad = df_sales[~df_sales[col].isin(valid)]
        if len(bad): errors.append(f"  FK issue ({lbl}): {len(bad)} rows")

    for col, valid, lbl in [
        ("date_id", valid_dates, "prod date_id"),
        ("line_id", valid_lines, "prod line_id"),
    ]:
        bad = df_prod[~df_prod[col].isin(valid)]
        if len(bad): errors.append(f"  FK issue ({lbl}): {len(bad)} rows")

    for e in errors: print(e)
    if not errors: print("  FK checks passed.")

    dups    = df_sales.duplicated().sum()
    str_rev = df_sales["total_revenue_egp"].apply(lambda x: isinstance(x, str)).mean()
    print(f"  fact_sales rows (incl. dupes):      {len(df_sales)}")
    print(f"  Duplicate rows:                     {dups}")
    print(f"  Null rate discount_pct:             {df_sales['discount_pct'].isna().mean():.1%}")
    print(f"  total_revenue_egp as string:        {str_rev:.1%}")
    print(f"  fact_production rows:               {len(df_prod)}")
    print(f"  Null rate downtime_hours:           {df_prod['downtime_hours'].isna().mean():.1%}")

# ─────────────────────────────────────────────
# INSTRUCTOR NOTES
# ─────────────────────────────────────────────
CLEANING_MD = """\
# Expected Cleaning Tasks — Misr Spinning and Weaving Company (MSW)

## fact_sales.csv

| # | Issue | Column | Approx. Rate |
|---|-------|--------|--------------|
| 1 | Missing values | `discount_pct` | ~5% nulls |
| 2 | Missing values | `quantity` | ~4% nulls |
| 3 | Inconsistent casing | `order_status` | ~3% uppercase ("COMPLETED", "CANCELLED") |
| 4 | Mixed data type | `total_revenue_egp` | ~3% stored as text strings |
| 5 | Impossible negative values | `total_revenue_egp` | 4 rows with negative values |
| 6 | Trailing whitespace | `market` | ~2% with trailing space ("Domestic ", "Export ") |
| 7 | Duplicate rows | all columns | ~1.5% fully duplicated records |

## fact_production.csv

| # | Issue | Column | Approx. Rate |
|---|-------|--------|--------------|
| 8 | Missing values | `downtime_hours` | ~5% nulls |
| 9 | Inconsistent casing | `production_status` | ~3% uppercase ("NORMAL", "AT CAPACITY") |

## dim_customer.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 10 | Inconsistent casing | `customer_type` | 4 rows lowercase ("local retailer", "export buyer") |

## dim_product.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 11 | Trailing whitespace | `category` | "Garment " (trailing space) for PR10, PR11, PR12 |

## dim_production_line.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 12 | Inconsistent casing | `production_type` | "shuttle loom", "rapier loom" (lowercase) for PL08, PL09 |

## dim_date.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 13 | Date stored as string | `date` | Text "YYYY-MM-DD" — must be converted to Date type in Power Query |

## Notes for Instructor
- The `market` trailing whitespace causes "Domestic" and "Domestic " to appear as separate slicer values — realistic and subtle.
- Negative `total_revenue_egp` combined with string-type rows is a compound issue: students must fix the type first, then remove negatives.
- The `production_status` casing issue directly distorts the "Lines Under Maintenance" KPI if uncleaned.
- The `category` whitespace in dim_product causes "Garment" and "Garment " to appear as separate groups in charts.
"""

DAX_MD = """\
# Suggested DAX Measures — Misr Spinning and Weaving Company (MSW)

## Sales Revenue
```dax
Total Revenue =
    CALCULATE(
        SUM(fact_sales[total_revenue_egp]),
        fact_sales[order_status] = "Completed",
        fact_sales[total_revenue_egp] > 0
    )

Total Orders =
    CALCULATE(
        COUNTROWS(fact_sales),
        fact_sales[order_status] = "Completed"
    )

Average Order Value =
    DIVIDE([Total Revenue], [Total Orders])

Average Unit Price =
    DIVIDE(
        CALCULATE(SUM(fact_sales[total_revenue_egp]),
                  fact_sales[order_status] = "Completed"),
        CALCULATE(SUM(fact_sales[quantity]),
                  fact_sales[order_status] = "Completed")
    )

Total Quantity Sold =
    CALCULATE(
        SUM(fact_sales[quantity]),
        fact_sales[order_status] = "Completed"
    )

Cancellation Rate =
    DIVIDE(
        CALCULATE(COUNTROWS(fact_sales), fact_sales[order_status] = "Cancelled"),
        COUNTROWS(fact_sales)
    )
```

## Channel & Market Performance
```dax
Export Revenue =
    CALCULATE([Total Revenue], fact_sales[market] = "Export")

Domestic Revenue =
    CALCULATE([Total Revenue], fact_sales[market] = "Domestic")

Export Revenue % =
    DIVIDE([Export Revenue], [Total Revenue])

E-commerce Revenue =
    CALCULATE([Total Revenue],
        RELATED(dim_channel[channel_name]) = "E-commerce"
    )

E-commerce Revenue % =
    DIVIDE([E-commerce Revenue], [Total Revenue])
```

## Production KPIs
```dax
Avg Production Efficiency % =
    AVERAGE(fact_production[efficiency_pct])

Avg Defect Rate % =
    AVERAGE(fact_production[defect_rate_pct])

Total Output KG =
    SUM(fact_production[actual_output_kg])

Total Defect KG =
    SUM(fact_production[defect_qty_kg])

Lines Under Maintenance =
    CALCULATE(
        DISTINCTCOUNT(fact_production[line_id]),
        fact_production[production_status] = "Under Maintenance"
    )

Avg Downtime Hours =
    CALCULATE(
        AVERAGE(fact_production[downtime_hours]),
        NOT(ISBLANK(fact_production[downtime_hours]))
    )
```

## Growth & Time Intelligence
```dax
YTD Revenue =
    TOTALYTD([Total Revenue], dim_date[date])

MoM Revenue Growth % =
    VAR Prev = CALCULATE([Total Revenue], DATEADD(dim_date[date], -1, MONTH))
    RETURN DIVIDE([Total Revenue] - Prev, Prev)

YoY Revenue Growth % =
    DIVIDE(
        [Total Revenue] - CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(dim_date[date])),
        CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(dim_date[date]))
    )

YoY Efficiency Change % =
    DIVIDE(
        [Avg Production Efficiency %] -
        CALCULATE([Avg Production Efficiency %], SAMEPERIODLASTYEAR(dim_date[date])),
        CALCULATE([Avg Production Efficiency %], SAMEPERIODLASTYEAR(dim_date[date]))
    )
```
"""

DASHBOARD_MD = """\
# Dashboard Questions & Visual Suggestions — MSW

## Analytical Questions (student-facing prompts)
1. Which product category (Yarn, Grey Fabric, Finished Fabric, Garment) generates the most revenue?
2. How has the Export vs Domestic revenue split changed from 2023 to 2024?
3. Which sales channel is growing fastest — and what is the share of E-commerce in 2024?
4. What is the seasonal pattern of sales revenue (are there peaks in Sep–Nov)?
5. Which customer type (Local Retailer, Garment Manufacturer, Export Buyer, etc.) drives the most total revenue?
6. How does average production efficiency compare across the four departments?
7. Which production line has the highest defect rate, and which has the most downtime hours?
8. What is the 2024 vs 2023 price inflation impact on average unit price?
9. What is the order cancellation and return rate — does it vary by product category or channel?
10. How has monthly production output changed from 2023 to 2024 (digitization impact on efficiency)?

## Suggested Visuals (instructor only)

| Visual | Type | Fields |
|--------|------|--------|
| Total Revenue KPI | Card | [Total Revenue] |
| Total Orders KPI | Card | [Total Orders] |
| Export Revenue % KPI | Card | [Export Revenue %] |
| Avg Production Efficiency KPI | Card | [Avg Production Efficiency %] |
| Revenue by Category | Bar | dim_product[category], [Total Revenue] |
| Revenue by Channel | Bar | dim_channel[channel_name], [Total Revenue] |
| Revenue Over Time | Line | dim_date[month_name], [Total Revenue] |
| YoY Revenue Comparison | Line (dual) | dim_date[month], current vs prior year |
| Export vs Domestic Split | Donut | fact_sales[market], [Total Revenue] |
| Channel Mix 2023 vs 2024 | Clustered bar | dim_channel[channel_name], year slicer |
| Defect Rate by Department | Bar | dim_production_line[department], [Avg Defect Rate %] |
| Efficiency by Production Line | Bar | dim_production_line[line_name], [Avg Production Efficiency %] |
| Production Output Trend | Line | dim_date[month_name], [Total Output KG] |
| Customer Type Revenue | Bar | dim_customer[customer_type], [Total Revenue] |
| Cancellation Rate by Product | Bar | dim_product[category], [Cancellation Rate] |

## Suggested Slicers
- Year / Quarter / Month
- Product Category / Fiber Type
- Customer Type / Market (Export vs Domestic)
- Sales Channel
- Department (for production views)
- Order Status
"""

MODEL_MD = """\
# Star Schema Relationships — MSW

## Tables
- **fact_sales** — main fact: product sales orders (~2,000+ rows)
- **fact_production** — secondary fact: monthly production line snapshots (~360 rows)
- **dim_date** — date dimension (shared by both fact tables)
- **dim_product** — product catalog (sales only)
- **dim_customer** — buyer dimension (sales only)
- **dim_channel** — sales channel (sales only)
- **dim_production_line** — factory lines (production only)

## Relationships

### fact_sales
| Fact Column | → | Dimension | PK | Cardinality | Filter |
|-------------|---|-----------|----|-------------|--------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single |
| `product_id` | → | `dim_product` | `product_id` | Many-to-One | Single |
| `customer_id` | → | `dim_customer` | `customer_id` | Many-to-One | Single |
| `channel_id` | → | `dim_channel` | `channel_id` | Many-to-One | Single |

### fact_production
| Fact Column | → | Dimension | PK | Cardinality | Filter |
|-------------|---|-----------|----|-------------|--------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single |
| `line_id` | → | `dim_production_line` | `line_id` | Many-to-One | Single |

## Notes
- Both fact tables share `dim_date` — Power BI handles this correctly with separate relationships.
- `dim_product`, `dim_customer`, `dim_channel` connect to `fact_sales` only.
- `dim_production_line` connects to `fact_production` only.
- Do NOT connect the two fact tables directly — use `dim_date` for cross-table time analysis.
- Mark `dim_date[date]` as a **Date Table** after converting from string to Date type in Power Query.
- `total_revenue_egp` must be converted to Decimal Number before any SUM measure will work.
- `market` exists in both `fact_sales` (denormalized convenience column) and `dim_customer` — use `dim_customer[market]` via the relationship for cleaner filtering.
"""

DATA_DICT_MD = """\
# Data Dictionary — Misr Spinning and Weaving Company (MSW)
## Digital Transformation Course · BINF 402 · GIU · Spring 2026

---

## Business Story
Misr Spinning and Weaving Company (MSW), founded in 1927 in El Mahalla El Kubra, Egypt, is one of the largest textile manufacturers in the Middle East and Africa. The company specialises in spinning, weaving, and garment production using high-quality Egyptian cotton.

This dataset covers **product sales orders** and **monthly production line performance** for 2023–2024 — a period when MSW undertook major digital transformation: implementing ERP systems, automating production lines, adopting CRM tools, and expanding its digital sales presence. Your goal as management is to track sales performance by product and customer segment, monitor export vs domestic revenue trends, measure production efficiency across factory departments, and identify quality improvement opportunities.

---

## Files

### `fact_sales.csv` (main fact table)
| Column | Description |
|--------|-------------|
| `sale_id` | Unique order identifier |
| `date_id` | Foreign key → `dim_date.date_id` (order date) |
| `product_id` | Foreign key → `dim_product.product_id` |
| `customer_id` | Foreign key → `dim_customer.customer_id` |
| `channel_id` | Foreign key → `dim_channel.channel_id` |
| `quantity` | Quantity ordered (units depend on product — kg, meter, or piece) |
| `unit_price_egp` | Price per unit (EGP) |
| `discount_pct` | Discount applied (decimal, e.g. 0.10 = 10%) |
| `total_revenue_egp` | Net revenue after discount (EGP) |
| `order_status` | Completed, Pending, Cancelled, or Returned |
| `market` | Domestic or Export |

### `fact_production.csv` (secondary fact table)
| Column | Description |
|--------|-------------|
| `production_id` | Unique snapshot identifier |
| `date_id` | Foreign key → `dim_date.date_id` (first day of month) |
| `line_id` | Foreign key → `dim_production_line.line_id` |
| `working_days` | Number of working days in the month |
| `planned_output_kg` | Target output for the month (kg) |
| `actual_output_kg` | Actual production achieved (kg) |
| `efficiency_pct` | Actual as % of planned output |
| `defect_qty_kg` | Quantity rejected due to quality defects (kg) |
| `defect_rate_pct` | Defect quantity as % of actual output |
| `downtime_hours` | Unplanned machine downtime (hours) |
| `production_status` | Normal, Under Maintenance, or At Capacity |

### `dim_date.csv`
| Column | Description |
|--------|-------------|
| `date_id` | Primary key (YYYYMMDD) |
| `date` | Full date string (YYYY-MM-DD) |
| `day` / `month` / `year` | Date components |
| `month_name` | Month name |
| `quarter` | Quarter (1–4) |
| `day_of_week` | Weekday name |
| `is_weekend` | True if Friday or Saturday |
| `is_holiday` | True if Egyptian public holiday |

### `dim_product.csv`
| Column | Description |
|--------|-------------|
| `product_id` | Primary key |
| `product_name` | Full product name |
| `category` | Yarn, Grey Fabric, Finished Fabric, or Garment |
| `fiber_type` | 100% Egyptian Cotton or Cotton Blend |
| `unit_of_measure` | kg, meter, or piece |
| `base_price_egp` | Reference base price per unit (EGP) |

### `dim_customer.csv`
| Column | Description |
|--------|-------------|
| `customer_id` | Primary key |
| `customer_name` | Synthetic customer name |
| `customer_type` | Local Retailer, Garment Manufacturer, Wholesaler, Government/Military, or Export Buyer |
| `market` | Domestic or Export |
| `country` | Egypt (domestic) or export destination |
| `governorate` | Egyptian governorate (domestic customers only) |

### `dim_channel.csv`
| Column | Description |
|--------|-------------|
| `channel_id` | Primary key |
| `channel_name` | Direct Sales, Distributor, Export Agent, Government Tender, E-commerce, Trade Fair |
| `channel_type` | Domestic or International |

### `dim_production_line.csv`
| Column | Description |
|--------|-------------|
| `line_id` | Primary key |
| `line_name` | Factory line or hall name |
| `department` | Spinning, Weaving, Finishing, or Garment |
| `production_type` | Specific machinery type (e.g. Rapier Loom, Dyeing) |
| `capacity_kg_per_day` | Rated daily capacity (kg) |
| `operational_status` | Active or Partial |
| `location` | All lines located in El Mahalla El Kubra |

---

## Intended Relationships
- `fact_sales` → `dim_date`, `dim_product`, `dim_customer`, `dim_channel`
- `fact_production` → `dim_date`, `dim_production_line`

## Notes for Students
- `total_revenue_egp` must be converted to a numeric type before any SUM or AVERAGE measure will work.
- The `market` column (Domestic / Export) is useful for comparing revenue streams without a join.
- Unit prices in 2024 reflect the impact of EGP currency fluctuations — year-over-year price comparisons are meaningful.
- `fact_production` records are monthly snapshots per production line — connect to both `dim_date` and `dim_production_line` to analyse factory efficiency.
- Clean all data in Power Query before building any measures or visuals.
"""

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print("=" * 62)
    print("Misr Spinning and Weaving Company (MSW) — Dataset Generator")
    print("=" * 62)
    make_dirs()

    print("\n[1/5] Generating dimension tables...")
    dim_date            = gen_dim_date()
    dim_product         = gen_dim_product()
    dim_customer        = gen_dim_customer(n=120)
    dim_channel         = gen_dim_channel()
    dim_production_line = gen_dim_production_line()

    print("\n[2/5] Generating fact tables...")
    fact_sales      = gen_fact_sales(dim_date, dim_product, dim_customer, dim_channel)
    fact_production = gen_fact_production(dim_date, dim_production_line)

    print("\n[3/5] Injecting cleaning issues...")
    fact_sales, fact_production, dim_customer, dim_product, dim_production_line = inject_issues(
        fact_sales, fact_production, dim_customer, dim_product, dim_production_line
    )

    print("\n[4/5] Saving files...")
    save(dim_date,            f"{STUDENT_DIR}/dim_date.csv")
    save(dim_product,         f"{STUDENT_DIR}/dim_product.csv")
    save(dim_customer,        f"{STUDENT_DIR}/dim_customer.csv")
    save(dim_channel,         f"{STUDENT_DIR}/dim_channel.csv")
    save(dim_production_line, f"{STUDENT_DIR}/dim_production_line.csv")
    save(fact_sales,          f"{STUDENT_DIR}/fact_sales.csv")
    save(fact_production,     f"{STUDENT_DIR}/fact_production.csv")

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
    validate(fact_sales, fact_production, dim_date, dim_product,
             dim_customer, dim_channel, dim_production_line)

    print("\n" + "=" * 62)
    print("Done. Output folder: output/msw/")
    print("  student_dataset/          → share with students")
    print("  data_dictionary.md        → share with students")
    print("  private_instructor_notes/ → instructor only")
    print("=" * 62)


if __name__ == "__main__":
    main()

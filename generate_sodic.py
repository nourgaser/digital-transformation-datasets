"""
SODIC — Sixth of October Development and Investment Company
Real Estate Developer, Egypt
Dataset Generator for Digital Transformation Course - BINF 402, Spring 2026
GIU - Dr. Nourhan Hamdi
Team: Aley Tamer, Ahmed Shahbour, Saifeldin Darwish, Ali Ahmed, Karim Ahmed (T7)
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

PROJECT_SLUG = "sodic"
OUTPUT_BASE  = f"output/{PROJECT_SLUG}"
STUDENT_DIR  = f"{OUTPUT_BASE}/student_dataset"
PRIVATE_DIR  = f"{OUTPUT_BASE}/private_instructor_notes"

DATE_START = date(2023, 1, 1)
DATE_END   = date(2024, 12, 31)
TARGET_SALES_ROWS    = 2000
TARGET_PROGRESS_ROWS = 240   # 10 projects × 24 months

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
# DIM PROJECT
# ─────────────────────────────────────────────
PROJECTS_RAW = [
    # (id, name, location, area, type, launch_year, total_units, target_delivery)
    ("PJ01", "Allegria",        "West Cairo",  "Sheikh Zayed",      "Residential",  2008, 1200, 2025),
    ("PJ02", "Beverly Hills",   "West Cairo",  "Sheikh Zayed",      "Mixed-Use",    2005,  900, 2024),
    ("PJ03", "Westown",         "West Cairo",  "Sheikh Zayed",      "Mixed-Use",    2010,  800, 2024),
    ("PJ04", "Eastown",         "East Cairo",  "New Cairo",         "Residential",  2012, 1100, 2025),
    ("PJ05", "SODIC East",      "East Cairo",  "New Cairo",         "Mixed-Use",    2018, 1500, 2026),
    ("PJ06", "Villette",        "East Cairo",  "New Cairo",         "Residential",  2016,  700, 2024),
    ("PJ07", "Ogami",           "North Coast", "Ras El Hekma",      "Resort",       2021,  600, 2026),
    ("PJ08", "Caesar",          "North Coast", "North Coast",       "Resort",       2019,  500, 2025),
    ("PJ09", "The Polygon",     "West Cairo",  "New Zayed",         "Commercial",   2022,  300, 2026),
    ("PJ10", "Kattameya Plaza", "East Cairo",  "Kattameya",         "Residential",  1998,  400, 2023),
]

def gen_dim_project():
    rows = [{
        "project_id":       p[0],
        "project_name":     p[1],
        "location":         p[2],
        "sub_area":         p[3],
        "project_type":     p[4],
        "launch_year":      p[5],
        "total_units":      p[6],
        "target_delivery_year": p[7],
    } for p in PROJECTS_RAW]
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# DIM UNIT TYPE
# ─────────────────────────────────────────────
UNIT_TYPES_RAW = [
    # (id, type, min_sqm, max_sqm, bedrooms, base_price_per_sqm_egp)
    ("UT01", "Studio",       35,   55,  0, 35000),
    ("UT02", "Apartment 1BR",65,   90,  1, 32000),
    ("UT03", "Apartment 2BR",110,  160, 2, 30000),
    ("UT04", "Apartment 3BR",170,  240, 3, 28000),
    ("UT05", "Penthouse",    200,  350, 4, 38000),
    ("UT06", "Twin House",   250,  380, 4, 25000),
    ("UT07", "Villa",        350,  600, 5, 22000),
    ("UT08", "Commercial",    50,  300, 0, 40000),
]

def gen_dim_unit_type():
    rows = [{
        "unit_type_id":        u[0],
        "unit_type":           u[1],
        "min_area_sqm":        u[2],
        "max_area_sqm":        u[3],
        "bedrooms":            u[4],
        "base_price_per_sqm":  u[5],
    } for u in UNIT_TYPES_RAW]
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# DIM CHANNEL
# ─────────────────────────────────────────────
CHANNELS = [
    ("CH01", "Broker",         "Offline"),
    ("CH02", "Direct Sales",   "Offline"),
    ("CH03", "Sakneen Digital","Online"),
    ("CH04", "Corporate/B2B",  "Offline"),
    ("CH05", "Referral",       "Offline"),
]

def gen_dim_channel():
    rows = [{"channel_id": c[0], "channel_name": c[1], "channel_type": c[2]}
            for c in CHANNELS]
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# DIM CUSTOMER
# ─────────────────────────────────────────────
BUYER_TYPES   = ["Egyptian Local", "Egyptian Diaspora", "Arab Expat", "Corporate Investor"]
BUYER_WEIGHTS = [55, 20, 15, 10]

def gen_dim_customer(n=150):
    rng  = np.random.default_rng(SEED + 5)
    rows = []
    gov_pool = ["Cairo", "Giza", "Alexandria", "Overseas", "Gulf", "UAE", "KSA", "UK"]
    gov_wts  = [30, 20, 10, 10, 10, 8, 7, 5]

    for i in range(1, n + 1):
        btype = random.choices(BUYER_TYPES, weights=BUYER_WEIGHTS)[0]
        if btype == "Corporate Investor":
            name = fake_en.company() + " Real Estate"
            gov  = "Cairo"
        else:
            name = fake_en.name()
            gov  = random.choices(gov_pool, weights=gov_wts)[0]

        rows.append({
            "customer_id":   f"CUS{i:04d}",
            "customer_name": name,
            "buyer_type":    btype,
            "nationality":   "Egyptian" if "Egyptian" in btype else btype.replace(" Expat","").replace(" Investor",""),
            "governorate":   gov,
            "age":           int(rng.integers(25, 65)) if btype != "Corporate Investor" else None,
            "gender":        random.choice(["Male", "Female"]) if btype != "Corporate Investor" else None,
            "is_investor":   btype == "Corporate Investor" or random.random() < 0.20,
        })
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# FACT UNIT SALES
# ─────────────────────────────────────────────

# Project × unit type compatibility
PROJ_UNIT_COMPAT = {
    "PJ01": ["UT06","UT07"],                        # Allegria — villas, twin houses
    "PJ02": ["UT03","UT04","UT06","UT07","UT08"],   # Beverly Hills — mixed
    "PJ03": ["UT02","UT03","UT04","UT08"],           # Westown — apartments, commercial
    "PJ04": ["UT02","UT03","UT04","UT05"],           # Eastown — apartments
    "PJ05": ["UT02","UT03","UT04","UT05","UT08"],   # SODIC East — mixed
    "PJ06": ["UT03","UT04","UT05","UT06"],           # Villette — apartments, twins
    "PJ07": ["UT01","UT02","UT03","UT06"],           # Ogami (resort) — chalets, apartments
    "PJ08": ["UT01","UT02","UT03"],                  # Caesar (resort) — chalets
    "PJ09": ["UT08"],                               # The Polygon — commercial
    "PJ10": ["UT02","UT03","UT04"],                  # Kattameya — apartments
}

# Project popularity weights (busier projects = more sales)
PROJ_WEIGHT = {
    "PJ01":10,"PJ02":6,"PJ03":7,"PJ04":9,"PJ05":12,
    "PJ06":7,"PJ07":8,"PJ08":5,"PJ09":4,"PJ10":3,
}

# Channel weights shift toward digital in 2024
def channel_weights(year):
    if year == 2023:
        return {"CH01":0.45,"CH02":0.25,"CH03":0.12,"CH04":0.10,"CH05":0.08}
    else:   # 2024: more digital, Sakneen adoption grows
        return {"CH01":0.38,"CH02":0.25,"CH03":0.20,"CH04":0.10,"CH05":0.07}

# Real estate sales peak around year-end (Q4) and post-Eid
def sales_seasonality(month):
    return {1:0.9, 2:0.85, 3:1.0, 4:0.95, 5:1.0, 6:0.90,
            7:1.1, 8:1.2, 9:1.05, 10:1.1, 11:1.2, 12:1.3}.get(month, 1.0)

UNIT_TYPE_LOOKUP = {u[0]: u for u in UNIT_TYPES_RAW}

# North Coast (PJ07, PJ08) sell more in summer
def proj_season(proj_id, month):
    if proj_id in ("PJ07", "PJ08"):
        return {4:1.0, 5:1.5, 6:1.8, 7:2.0, 8:1.8, 9:1.2}.get(month, 0.8)
    return sales_seasonality(month)

CONTRACT_STATUSES = ["Signed", "Under Review", "Cancelled"]
CONTRACT_WEIGHTS  = [88, 8, 4]

PAYMENT_PLANS = ["5-Year Installment", "7-Year Installment", "10-Year Installment", "Cash"]
PAYMENT_WEIGHTS = [30, 35, 25, 10]

def gen_fact_unit_sales(dim_date, dim_project, dim_unit_type, dim_customer, dim_channel):
    rng       = np.random.default_rng(SEED + 20)
    proj_ids  = [p[0] for p in PROJECTS_RAW]
    proj_wts  = [PROJ_WEIGHT[p] for p in proj_ids]
    ch_ids    = [c[0] for c in CHANNELS]
    cust_ids  = dim_customer["customer_id"].tolist()
    is_inv_map = dim_customer.set_index("customer_id")["is_investor"].to_dict()

    rows    = []
    sale_id = 1

    for _ in range(TARGET_SALES_ROWS):
        proj_id  = random.choices(proj_ids, weights=proj_wts)[0]
        compat   = PROJ_UNIT_COMPAT[proj_id]
        unit_type_id = random.choice(compat)
        ut       = UNIT_TYPE_LOOKUP[unit_type_id]
        ut_name, min_sqm, max_sqm, beds, base_psm = ut[1], ut[2], ut[3], ut[4], ut[5]

        # Date — weighted by seasonality
        date_row = dim_date.copy()
        date_row["w"] = date_row["month"].map(
            {m: proj_season(proj_id, m) for m in range(1, 13)}
        )
        date_row  = date_row.sample(1, weights="w").iloc[0]
        date_id   = date_row["date_id"]
        year      = date_row["year"]
        month     = date_row["month"]

        # Unit area
        area_sqm  = round(rng.uniform(min_sqm, max_sqm), 1)

        # Price per sqm: base ± project premium ± 2024 price inflation (~EGP devaluation effect)
        proj_premium = {
            "PJ01":1.35,"PJ02":1.20,"PJ03":1.15,"PJ04":1.10,"PJ05":1.25,
            "PJ06":1.10,"PJ07":1.40,"PJ08":1.30,"PJ09":1.50,"PJ10":0.95,
        }[proj_id]
        year_factor  = 1.0 if year == 2023 else 1.18   # ~18% price increase in 2024
        psm_actual   = round(base_psm * proj_premium * year_factor * rng.uniform(0.95, 1.05))
        contract_val = round(psm_actual * area_sqm, -3)  # round to thousands

        # Down payment
        dp_pct = random.choice([10, 15, 20, 25, 30])
        down_payment = round(contract_val * dp_pct / 100, -3)
        remaining    = contract_val - down_payment

        # Payment plan
        payment_plan = random.choices(PAYMENT_PLANS, weights=PAYMENT_WEIGHTS)[0]

        # Commission (broker fee)
        channel_id = random.choices(ch_ids,
                                    weights=list(channel_weights(year).values()))[0]
        commission_pct = 0.0
        if channel_id == "CH01":    # Broker
            commission_pct = round(rng.uniform(0.02, 0.04), 3)
        elif channel_id == "CH05":  # Referral
            commission_pct = round(rng.uniform(0.01, 0.02), 3)
        commission_amt = round(contract_val * commission_pct, -2)

        # Customer
        customer_id  = rng.choice(cust_ids)
        contract_status = random.choices(CONTRACT_STATUSES, weights=CONTRACT_WEIGHTS)[0]
        if contract_status == "Cancelled":
            contract_val  = 0
            down_payment  = 0
            commission_amt = 0

        rows.append({
            "sale_id":          f"SL{sale_id:05d}",
            "date_id":          date_id,
            "project_id":       proj_id,
            "unit_type_id":     unit_type_id,
            "customer_id":      customer_id,
            "channel_id":       channel_id,
            "area_sqm":         area_sqm,
            "price_per_sqm":    psm_actual,
            "contract_value":   contract_val,
            "down_payment":     down_payment,
            "remaining_balance":remaining if contract_status == "Signed" else 0,
            "down_payment_pct": dp_pct,
            "payment_plan":     payment_plan,
            "commission_pct":   commission_pct,
            "commission_amount":commission_amt,
            "contract_status":  contract_status,
            "is_investor_buyer": is_inv_map.get(customer_id, False),
        })
        sale_id += 1

    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# FACT PROJECT PROGRESS (monthly snapshots)
# ─────────────────────────────────────────────
def gen_fact_project_progress(dim_date, dim_project):
    rng  = np.random.default_rng(SEED + 30)
    # One row per project per month
    months = dim_date[dim_date["day"] == 1][["date_id","month","year","quarter"]].copy()

    proj_budget = {
        "PJ01":4500,"PJ02":3200,"PJ03":2800,"PJ04":3800,"PJ05":6000,
        "PJ06":2200,"PJ07":2500,"PJ08":1800,"PJ09":1500,"PJ10":1200,
    }  # budget in millions EGP

    # Delivery status per project (90%+ delivered ahead = SODIC's metric)
    proj_delivery = {
        "PJ01":"On Track","PJ02":"Delivered","PJ03":"Delivered",
        "PJ04":"On Track","PJ05":"On Track","PJ06":"Delivered",
        "PJ07":"On Track","PJ08":"On Track","PJ09":"Early Stage",
        "PJ10":"Delivered",
    }

    rows  = []
    row_id = 1

    for _, proj_row in dim_project.iterrows():
        pid         = proj_row["project_id"]
        launch_year = proj_row["launch_year"]
        budget_m    = proj_budget[pid]
        delivery    = proj_delivery[pid]

        # Cumulative construction % starts from where project was in Jan 2023
        # Older projects are more complete
        age_years    = 2023 - launch_year
        start_pct    = min(95, max(20, age_years * 8 + rng.integers(0, 10)))

        cum_pct = float(start_pct)
        for _, mrow in months.iterrows():
            month_num = mrow["month"]
            yr        = mrow["year"]

            # Monthly progress increment (construction slows in summer heat)
            increment = rng.uniform(1.5, 4.5) if month_num not in (7, 8) else rng.uniform(0.5, 2.0)
            if delivery == "Delivered":
                cum_pct = 100.0
            elif delivery == "Early Stage":
                cum_pct = min(40, cum_pct + increment * 0.5)
            else:
                cum_pct = min(99, cum_pct + increment)

            # Budget spend: proportional to progress + fixed overhead
            budget_spent_pct = min(100, cum_pct * rng.uniform(0.95, 1.05))
            budget_spent     = round(budget_m * budget_spent_pct / 100, 1)
            cost_overrun_pct = round((budget_spent_pct - cum_pct), 1)

            # Units under construction vs completed
            total_u  = proj_row["total_units"]
            completed_u = int(total_u * cum_pct / 100)
            under_con_u = total_u - completed_u if delivery != "Delivered" else 0

            rows.append({
                "progress_id":        f"PR{row_id:05d}",
                "date_id":            mrow["date_id"],
                "project_id":         pid,
                "completion_pct":     round(cum_pct, 1),
                "budget_total_mEGP":  budget_m,
                "budget_spent_mEGP":  budget_spent,
                "cost_overrun_pct":   cost_overrun_pct,
                "units_completed":    completed_u,
                "units_under_construction": under_con_u,
                "delivery_status":    delivery,
                "is_ahead_of_schedule": delivery in ("Delivered","On Track") and cost_overrun_pct < 5,
            })
            row_id += 1

    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# INJECT CLEANING ISSUES
# ─────────────────────────────────────────────
def inject_issues(df_sales, df_progress, df_customer, df_project, df_unit_type):
    n   = len(df_sales)
    np_ = len(df_progress)
    rng = np.random.default_rng(SEED + 99)

    # ── fact_unit_sales ────────────────────────
    # 1. ~5% nulls in commission_pct
    idx1 = rng.choice(n, size=int(n * 0.05), replace=False)
    df_sales.loc[idx1, "commission_pct"] = np.nan

    # 2. ~4% nulls in down_payment_pct
    idx2 = rng.choice(n, size=int(n * 0.04), replace=False)
    df_sales.loc[idx2, "down_payment_pct"] = np.nan

    # 3. Inconsistent casing in contract_status (~3%)
    idx3 = rng.choice(n, size=int(n * 0.03), replace=False)
    df_sales.loc[idx3, "contract_status"] = df_sales.loc[idx3, "contract_status"].str.upper()

    # 4. contract_value stored as string in ~3% of rows
    df_sales["contract_value"] = df_sales["contract_value"].astype(object)
    idx4 = rng.choice(n, size=int(n * 0.03), replace=False)
    for i in idx4:
        df_sales.at[i, "contract_value"] = str(df_sales.at[i, "contract_value"])

    # 5. Negative contract_value (impossible) — 3 rows
    bad = rng.choice(n, size=3, replace=False)
    for i in bad:
        val = df_sales.at[i, "contract_value"]
        df_sales.at[i, "contract_value"] = -abs(float(val))

    # 6. Whitespace in payment_plan (~2%)
    idx6 = rng.choice(n, size=int(n * 0.02), replace=False)
    df_sales.loc[idx6, "payment_plan"] = df_sales.loc[idx6, "payment_plan"] + " "

    # 7. Duplicate rows (~1.5%)
    dup_idx = rng.choice(n, size=int(n * 0.015), replace=False)
    dups    = df_sales.iloc[dup_idx].copy()
    df_sales = pd.concat([df_sales, dups], ignore_index=True)

    # ── fact_project_progress ─────────────────
    # 8. ~5% nulls in cost_overrun_pct
    idx8 = rng.choice(np_, size=int(np_ * 0.05), replace=False)
    df_progress.loc[idx8, "cost_overrun_pct"] = np.nan

    # 9. Inconsistent casing in delivery_status (~3%)
    idx9 = rng.choice(np_, size=int(np_ * 0.03), replace=False)
    df_progress.loc[idx9, "delivery_status"] = df_progress.loc[idx9, "delivery_status"].str.lower()

    # ── dim_customer ───────────────────────────
    # 10. Inconsistent buyer_type casing for 4 rows
    s_idx = df_customer.sample(4, random_state=SEED).index
    df_customer.loc[s_idx, "buyer_type"] = df_customer.loc[s_idx, "buyer_type"].str.lower()

    # ── dim_project ────────────────────────────
    # 11. Trailing whitespace in project_type for 2 rows
    df_project.loc[df_project["project_id"].isin(["PJ07","PJ08"]), "project_type"] = "Resort "

    # ── dim_unit_type ──────────────────────────
    # 12. Inconsistent casing in unit_type for 2 rows
    df_unit_type.loc[df_unit_type["unit_type_id"].isin(["UT06","UT07"]), "unit_type"] = \
        df_unit_type.loc[df_unit_type["unit_type_id"].isin(["UT06","UT07"]), "unit_type"].str.lower()

    return df_sales, df_progress, df_customer, df_project, df_unit_type

# ─────────────────────────────────────────────
# VALIDATION
# ─────────────────────────────────────────────
def validate(df_sales, df_prog, dim_date, dim_project, dim_unit_type,
             dim_customer, dim_channel):
    print("\nValidation:")
    valid_dates   = set(dim_date["date_id"])
    valid_proj    = set(dim_project["project_id"])
    valid_ut      = set(dim_unit_type["unit_type_id"])
    valid_cust    = set(dim_customer["customer_id"])
    valid_ch      = set(dim_channel["channel_id"])

    errors = []
    for col, valid, lbl in [
        ("date_id",      valid_dates, "sales date_id"),
        ("project_id",   valid_proj,  "sales project_id"),
        ("unit_type_id", valid_ut,    "sales unit_type_id"),
        ("customer_id",  valid_cust,  "sales customer_id"),
        ("channel_id",   valid_ch,    "sales channel_id"),
    ]:
        bad = df_sales[~df_sales[col].isin(valid)]
        if len(bad): errors.append(f"  FK issue ({lbl}): {len(bad)} rows")

    for col, valid, lbl in [
        ("date_id",    valid_dates, "prog date_id"),
        ("project_id", valid_proj,  "prog project_id"),
    ]:
        bad = df_prog[~df_prog[col].isin(valid)]
        if len(bad): errors.append(f"  FK issue ({lbl}): {len(bad)} rows")

    for e in errors: print(e)
    if not errors: print("  FK checks passed.")

    dups = df_sales.duplicated().sum()
    str_cv = (df_sales["contract_value"].apply(lambda x: isinstance(x, str))).mean()
    signed = (df_sales["contract_status"].str.strip().str.title() == "Signed").mean()
    print(f"  fact_unit_sales rows (incl. dupes): {len(df_sales)}")
    print(f"  Duplicate rows:                     {dups}")
    print(f"  Null rate commission_pct:           {df_sales['commission_pct'].isna().mean():.1%}")
    print(f"  contract_value as string:           {str_cv:.1%}")
    print(f"  fact_project_progress rows:         {len(df_prog)}")
    print(f"  Null rate cost_overrun_pct:         {df_prog['cost_overrun_pct'].isna().mean():.1%}")

# ─────────────────────────────────────────────
# INSTRUCTOR NOTES
# ─────────────────────────────────────────────
CLEANING_MD = """\
# Expected Cleaning Tasks — SODIC

## fact_unit_sales.csv

| # | Issue | Column | Approx. Rate |
|---|-------|--------|--------------|
| 1 | Missing values | `commission_pct` | ~5% nulls |
| 2 | Missing values | `down_payment_pct` | ~4% nulls |
| 3 | Inconsistent casing | `contract_status` | ~3% uppercase ("SIGNED", "CANCELLED") |
| 4 | Mixed data type | `contract_value` | ~3% stored as text strings |
| 5 | Impossible negative values | `contract_value` | 3 rows with negative values |
| 6 | Trailing whitespace | `payment_plan` | ~2% with trailing space |
| 7 | Duplicate rows | all columns | ~1.5% fully duplicated records |

## fact_project_progress.csv

| # | Issue | Column | Approx. Rate |
|---|-------|--------|--------------|
| 8 | Missing values | `cost_overrun_pct` | ~5% nulls |
| 9 | Inconsistent casing | `delivery_status` | ~3% lowercase ("on track", "delivered") |

## dim_customer.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 10 | Inconsistent casing | `buyer_type` | 4 rows lowercase ("egyptian local") |

## dim_project.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 11 | Trailing whitespace | `project_type` | "Resort " (trailing space) for PJ07 and PJ08 |

## dim_unit_type.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 12 | Inconsistent casing | `unit_type` | "twin house", "villa" (lowercase) for UT06, UT07 |

## dim_date.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 13 | Date stored as string | `date` | Text "YYYY-MM-DD" — must be converted to Date type in Power Query |

## Notes for Instructor
- The `payment_plan` trailing whitespace issue means grouping in charts shows "5-Year Installment" and "5-Year Installment " as two separate categories — a very realistic and subtle data quality lesson.
- Negative `contract_value` + text-type rows in the same column is a compound issue that students must resolve in the right order (fix type → filter negatives).
- The `delivery_status` lowercase issue in fact_project_progress directly distorts the "On Track %" KPI if uncleaned — a meaningful business consequence.
"""

DAX_MD = """\
# Suggested DAX Measures — SODIC

## Sales Revenue
```dax
Total Contract Value =
    CALCULATE(
        SUM(fact_unit_sales[contract_value]),
        fact_unit_sales[contract_status] = "Signed",
        fact_unit_sales[contract_value] > 0
    )

Total Units Sold =
    CALCULATE(
        COUNTROWS(fact_unit_sales),
        fact_unit_sales[contract_status] = "Signed"
    )

Average Contract Value =
    DIVIDE([Total Contract Value], [Total Units Sold])

Average Price per SQM =
    DIVIDE(
        CALCULATE(SUM(fact_unit_sales[contract_value]),
                  fact_unit_sales[contract_status] = "Signed"),
        CALCULATE(SUM(fact_unit_sales[area_sqm]),
                  fact_unit_sales[contract_status] = "Signed")
    )

Cancellation Rate =
    DIVIDE(
        CALCULATE(COUNTROWS(fact_unit_sales),
                  fact_unit_sales[contract_status] = "Cancelled"),
        COUNTROWS(fact_unit_sales)
    )

Total Down Payments Collected =
    CALCULATE(
        SUM(fact_unit_sales[down_payment]),
        fact_unit_sales[contract_status] = "Signed"
    )

Total Commission Paid =
    CALCULATE(
        SUM(fact_unit_sales[commission_amount]),
        fact_unit_sales[contract_status] = "Signed"
    )
```

## Channel Performance
```dax
Digital Sales Value =
    CALCULATE([Total Contract Value],
        RELATED(dim_channel[channel_type]) = "Online"
    )

Broker Sales Value =
    CALCULATE([Total Contract Value],
        dim_channel[channel_name] = "Broker"
    )

Digital Sales % =
    DIVIDE([Digital Sales Value], [Total Contract Value])
```

## Project Performance
```dax
Avg Completion % =
    AVERAGE(fact_project_progress[completion_pct])

Projects On Track =
    CALCULATE(
        DISTINCTCOUNT(fact_project_progress[project_id]),
        fact_project_progress[delivery_status] = "On Track"
    )

Avg Cost Overrun % =
    CALCULATE(
        AVERAGE(fact_project_progress[cost_overrun_pct]),
        fact_project_progress[cost_overrun_pct] >= 0
    )

Budget Utilization % =
    DIVIDE(
        SUM(fact_project_progress[budget_spent_mEGP]),
        SUM(fact_project_progress[budget_total_mEGP])
    )
```

## Growth & Time Intelligence
```dax
YTD Contract Value =
    TOTALYTD([Total Contract Value], dim_date[date])

MoM Sales Growth % =
    VAR Prev = CALCULATE([Total Contract Value], DATEADD(dim_date[date], -1, MONTH))
    RETURN DIVIDE([Total Contract Value] - Prev, Prev)

YoY Sales Growth % =
    DIVIDE(
        [Total Contract Value] - CALCULATE([Total Contract Value], SAMEPERIODLASTYEAR(dim_date[date])),
        CALCULATE([Total Contract Value], SAMEPERIODLASTYEAR(dim_date[date]))
    )
```

## Customer KPIs
```dax
Total Buyers =
    DISTINCTCOUNT(fact_unit_sales[customer_id])

Investor Buyers % =
    DIVIDE(
        CALCULATE([Total Units Sold], fact_unit_sales[is_investor_buyer] = TRUE()),
        [Total Units Sold]
    )

Diaspora Buyers % =
    DIVIDE(
        CALCULATE([Total Buyers],
            RELATED(dim_customer[buyer_type]) = "Egyptian Diaspora"),
        [Total Buyers]
    )
```
"""

DASHBOARD_MD = """\
# Dashboard Questions & Visual Suggestions — SODIC

## Analytical Questions (student-facing prompts)
1. Which projects generate the highest total contract value?
2. How does revenue from Broker vs Direct vs Digital (Sakneen) compare, and how has the channel mix shifted from 2023 to 2024?
3. Which unit types (Villa, Apartment, Commercial) drive the most revenue and volume?
4. How does sales volume change by month — are there seasonal peaks (North Coast in summer, year-end Q4)?
5. What is the average contract value per project, and how does price per sqm compare across projects?
6. What is the project completion rate, and which projects are on track vs delayed?
7. What share of buyers are investors vs end-users, and which buyer types prefer which projects?
8. How does 2024 pricing compare to 2023 (EGP inflation impact on contract values)?
9. What is the cancellation rate by project and channel?
10. Which payment plan is most popular, and does it vary by unit type or buyer segment?

## Suggested Visuals (instructor only)

| Visual | Type | Fields |
|--------|------|--------|
| Total Contract Value KPI | Card | [Total Contract Value] |
| Total Units Sold KPI | Card | [Total Units Sold] |
| Avg Contract Value KPI | Card | [Average Contract Value] |
| Digital Sales % KPI | Card | [Digital Sales %] |
| Sales by Project | Bar | dim_project[project_name], [Total Contract Value] |
| Sales by Unit Type | Bar/Donut | dim_unit_type[unit_type], [Total Units Sold] |
| Contract Value over Time | Line | dim_date[month_name], [Total Contract Value] |
| YoY Comparison | Line (dual) | dim_date[month], current vs prior year |
| Channel Mix 2023 vs 2024 | Clustered bar | dim_channel[channel_name], year slicer |
| Project Completion | Gauge/Bar | dim_project[project_name], [Avg Completion %] |
| Budget vs Actual | Clustered bar | dim_project[project_name], budget_total vs budget_spent |
| Buyer Type Breakdown | Donut | dim_customer[buyer_type], [Total Buyers] |
| Sales by Location | Bar/Map | dim_project[location], [Total Contract Value] |
| Payment Plan Distribution | Pie | fact_unit_sales[payment_plan], count |
| Cancellation Rate by Project | Bar | dim_project[project_name], [Cancellation Rate] |

## Suggested Slicers
- Year / Quarter / Month
- Project Name / Location
- Unit Type
- Sales Channel
- Buyer Type
- Contract Status
"""

MODEL_MD = """\
# Star Schema Relationships — SODIC

## Tables
- **fact_unit_sales** — main fact: property unit contracts (~2,000+ rows)
- **fact_project_progress** — secondary fact: monthly project status snapshots (~240 rows)
- **dim_date** — date dimension (shared)
- **dim_project** — project/compound dimension (shared)
- **dim_unit_type** — unit type dimension (sales only)
- **dim_customer** — buyer dimension (sales only)
- **dim_channel** — sales channel dimension (sales only)

## Relationships

### fact_unit_sales
| Fact Column | → | Dimension | PK | Cardinality | Filter |
|-------------|---|-----------|----|-------------|--------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single |
| `project_id` | → | `dim_project` | `project_id` | Many-to-One | Single |
| `unit_type_id` | → | `dim_unit_type` | `unit_type_id` | Many-to-One | Single |
| `customer_id` | → | `dim_customer` | `customer_id` | Many-to-One | Single |
| `channel_id` | → | `dim_channel` | `channel_id` | Many-to-One | Single |

### fact_project_progress
| Fact Column | → | Dimension | PK | Cardinality | Filter |
|-------------|---|-----------|----|-------------|--------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single |
| `project_id` | → | `dim_project` | `project_id` | Many-to-One | Single |

## Notes
- Both fact tables share `dim_date` and `dim_project` — Power BI handles this correctly with separate relationships.
- `dim_unit_type`, `dim_customer`, and `dim_channel` are only connected to `fact_unit_sales`.
- Do NOT connect the two fact tables to each other directly — use shared dimensions for cross-table analysis.
- Mark `dim_date[date]` as a **Date Table** after converting from string to Date type.
- `contract_value` must be a numeric type (Decimal Number) before any SUM measure will work.
- The `delivery_status` casing issue in `fact_project_progress` directly affects the "On Track %" calculation — clean before building visuals.
"""

DATA_DICT_MD = """\
# Data Dictionary — SODIC
## Digital Transformation Course · BINF 402 · GIU · Spring 2026

---

## Business Story
SODIC (Sixth of October Development and Investment Company) is one of Egypt's leading real estate developers, operating across West Cairo, East Cairo, and North Coast communities.
This dataset covers **property unit sales contracts** and **monthly project construction progress** for 2023–2024.
Your goal as management is to track sales performance, monitor project delivery, analyse channel effectiveness, and understand buyer behaviour.

---

## Files

### `fact_unit_sales.csv` (main fact table)
| Column | Description |
|--------|-------------|
| `sale_id` | Unique contract identifier |
| `date_id` | Foreign key → `dim_date.date_id` (contract date) |
| `project_id` | Foreign key → `dim_project.project_id` |
| `unit_type_id` | Foreign key → `dim_unit_type.unit_type_id` |
| `customer_id` | Foreign key → `dim_customer.customer_id` |
| `channel_id` | Foreign key → `dim_channel.channel_id` |
| `area_sqm` | Unit size in square meters |
| `price_per_sqm` | Selling price per sqm (EGP) |
| `contract_value` | Total contract value (EGP) |
| `down_payment` | Initial down payment amount (EGP) |
| `remaining_balance` | Remaining installment balance (EGP) |
| `down_payment_pct` | Down payment as % of contract value |
| `payment_plan` | Installment plan selected (e.g. 7-Year Installment) |
| `commission_pct` | Broker/referral commission rate |
| `commission_amount` | Total commission paid (EGP) |
| `contract_status` | Signed, Under Review, or Cancelled |
| `is_investor_buyer` | True if buyer is purchasing for investment |

### `fact_project_progress.csv` (secondary fact table)
| Column | Description |
|--------|-------------|
| `progress_id` | Unique snapshot identifier |
| `date_id` | Foreign key → `dim_date.date_id` (month start) |
| `project_id` | Foreign key → `dim_project.project_id` |
| `completion_pct` | % of construction completed at month end |
| `budget_total_mEGP` | Total approved project budget (millions EGP) |
| `budget_spent_mEGP` | Cumulative spend to date (millions EGP) |
| `cost_overrun_pct` | % difference between spend and completion |
| `units_completed` | Number of units fully delivered |
| `units_under_construction` | Units currently being built |
| `delivery_status` | On Track, Delivered, or Early Stage |
| `is_ahead_of_schedule` | True if progressing ahead of plan |

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

### `dim_project.csv`
| Column | Description |
|--------|-------------|
| `project_id` | Primary key |
| `project_name` | Community/compound name |
| `location` | West Cairo / East Cairo / North Coast |
| `sub_area` | More specific area |
| `project_type` | Residential, Mixed-Use, Resort, Commercial |
| `launch_year` | Year project was launched |
| `total_units` | Total number of units in the development |
| `target_delivery_year` | Planned delivery completion year |

### `dim_unit_type.csv`
| Column | Description |
|--------|-------------|
| `unit_type_id` | Primary key |
| `unit_type` | Studio, Apartment 1BR, Twin House, Villa, etc. |
| `min_area_sqm` | Minimum unit size |
| `max_area_sqm` | Maximum unit size |
| `bedrooms` | Number of bedrooms |
| `base_price_per_sqm` | Reference base price per sqm (EGP) |

### `dim_customer.csv`
| Column | Description |
|--------|-------------|
| `customer_id` | Primary key |
| `customer_name` | Synthetic buyer name |
| `buyer_type` | Egyptian Local, Egyptian Diaspora, Arab Expat, Corporate Investor |
| `nationality` | Nationality |
| `governorate` | Buyer's location (or Overseas/Gulf) |
| `age` | Age (individuals only) |
| `gender` | Gender (individuals only) |
| `is_investor` | True if purchasing for investment purposes |

### `dim_channel.csv`
| Column | Description |
|--------|-------------|
| `channel_id` | Primary key |
| `channel_name` | Broker, Direct Sales, Sakneen Digital, Corporate/B2B, Referral |
| `channel_type` | Offline or Online |

---

## Intended Relationships
- `fact_unit_sales` → `dim_date`, `dim_project`, `dim_unit_type`, `dim_customer`, `dim_channel`
- `fact_project_progress` → `dim_date`, `dim_project`

## Notes for Students
- `contract_value` must be converted to a numeric type before any SUM measure will work.
- The digital channel (Sakneen) shows growing share from 2023 to 2024 — this is a key insight to surface.
- North Coast projects (Ogami, Caesar) follow a summer seasonality pattern — look at monthly breakdowns.
- SODIC's 91% ahead-of-schedule delivery record is reflected in the `is_ahead_of_schedule` column.
"""

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print("=" * 55)
    print("SODIC — Dataset Generator")
    print("=" * 55)
    make_dirs()

    print("\n[1/5] Generating dimension tables...")
    dim_date      = gen_dim_date()
    dim_project   = gen_dim_project()
    dim_unit_type = gen_dim_unit_type()
    dim_channel   = gen_dim_channel()
    dim_customer  = gen_dim_customer(n=150)

    print("\n[2/5] Generating fact tables...")
    fact_sales    = gen_fact_unit_sales(dim_date, dim_project, dim_unit_type,
                                        dim_customer, dim_channel)
    fact_progress = gen_fact_project_progress(dim_date, dim_project)

    print("\n[3/5] Injecting cleaning issues...")
    fact_sales, fact_progress, dim_customer, dim_project, dim_unit_type = inject_issues(
        fact_sales, fact_progress, dim_customer, dim_project, dim_unit_type
    )

    print("\n[4/5] Saving files...")
    save(dim_date,      f"{STUDENT_DIR}/dim_date.csv")
    save(dim_project,   f"{STUDENT_DIR}/dim_project.csv")
    save(dim_unit_type, f"{STUDENT_DIR}/dim_unit_type.csv")
    save(dim_channel,   f"{STUDENT_DIR}/dim_channel.csv")
    save(dim_customer,  f"{STUDENT_DIR}/dim_customer.csv")
    save(fact_sales,    f"{STUDENT_DIR}/fact_unit_sales.csv")
    save(fact_progress, f"{STUDENT_DIR}/fact_project_progress.csv")

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
    validate(fact_sales, fact_progress, dim_date, dim_project,
             dim_unit_type, dim_customer, dim_channel)

    print("\n" + "=" * 55)
    print("Done. Output folder: output/sodic/")
    print("  student_dataset/          → share with students")
    print("  data_dictionary.md        → share with students")
    print("  private_instructor_notes/ → instructor only")
    print("=" * 55)

if __name__ == "__main__":
    main()

"""
Misr Insurance Company — Egyptian Non-Life (General) Insurance
Dataset Generator for Digital Transformation Course - BINF 402, Spring 2026
GIU - Dr. Nourhan Hamdi
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

PROJECT_SLUG = "misr_insurance"
OUTPUT_BASE  = f"output/{PROJECT_SLUG}"
STUDENT_DIR  = f"{OUTPUT_BASE}/student_dataset"
PRIVATE_DIR  = f"{OUTPUT_BASE}/private_instructor_notes"

DATE_START = date(2023, 1, 1)
DATE_END   = date(2024, 12, 31)
TARGET_POLICY_ROWS = 2000
TARGET_CLAIM_ROWS  = 700

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
            "date":        d.strftime("%Y-%m-%d"),  # string — cleaning task
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
    # (product_id, name, category, customer_type, premium_min, premium_max, expected_loss_ratio)
    ("PR01", "Comprehensive Motor",     "Motor",         "Individual",  1500,   8000,  0.62),
    ("PR02", "Third-Party Motor",       "Motor",         "Individual",   400,   2000,  0.55),
    ("PR03", "Home Property",           "Property",      "Individual",  2000,  15000,  0.45),
    ("PR04", "Commercial Property",     "Property",      "Corporate",  10000, 100000,  0.50),
    ("PR05", "Marine Cargo",            "Marine",        "Corporate",   5000,  80000,  0.48),
    ("PR06", "Marine Hull",             "Marine",        "Corporate",  20000, 200000,  0.52),
    ("PR07", "Individual Travel",       "Travel",        "Individual",   200,   1500,  0.35),
    ("PR08", "Corporate Travel",        "Travel",        "Corporate",  3000,  20000,  0.38),
    ("PR09", "Engineering & Machinery", "Engineering",   "Corporate",  15000, 150000,  0.55),
    ("PR10", "Corporate Risk Package",  "Corporate Risk","Corporate",  50000, 500000,  0.50),
]

def gen_dim_product():
    rows = [{
        "product_id":        p[0],
        "product_name":      p[1],
        "product_category":  p[2],
        "customer_type":     p[3],
        "premium_min_egp":   p[4],
        "premium_max_egp":   p[5],
        "expected_loss_ratio": p[6],
    } for p in PRODUCTS_RAW]
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# DIM BRANCH
# ─────────────────────────────────────────────
BRANCHES_RAW = [
    ("BR01", "Cairo HQ",         "Cairo",       "Greater Cairo"),
    ("BR02", "Heliopolis",       "Cairo",       "Greater Cairo"),
    ("BR03", "Giza",             "Giza",        "Greater Cairo"),
    ("BR04", "Alexandria",       "Alexandria",  "Alexandria"),
    ("BR05", "Mansoura",         "Dakahlia",    "Delta"),
    ("BR06", "Tanta",            "Gharbia",     "Delta"),
    ("BR07", "Luxor",            "Luxor",       "Upper Egypt"),
    ("BR08", "Aswan",            "Aswan",       "Upper Egypt"),
    ("BR09", "Suez",             "Suez",        "Canal Zone"),
    ("BR10", "Port Said",        "Port Said",   "Canal Zone"),
    ("BR11", "Asyut",            "Asyut",       "Upper Egypt"),
    ("BR12", "Ismailia",         "Ismailia",    "Canal Zone"),
]

def gen_dim_branch():
    rows = [{"branch_id": b[0], "branch_name": b[1],
             "governorate": b[2], "region": b[3]}
            for b in BRANCHES_RAW]
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# DIM CHANNEL
# ─────────────────────────────────────────────
CHANNELS = [
    ("CH01", "Branch",  "Offline"),
    ("CH02", "Agent",   "Offline"),
    ("CH03", "Broker",  "Offline"),
    ("CH04", "Online",  "Digital"),
    ("CH05", "Call Center", "Digital"),
]

def gen_dim_channel():
    rows = [{"channel_id": c[0], "channel_name": c[1], "channel_type": c[2]}
            for c in CHANNELS]
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# DIM CUSTOMER
# ─────────────────────────────────────────────
def gen_dim_customer(n=180):
    rng = np.random.default_rng(SEED + 7)
    rows = []
    branch_ids = [b[0] for b in BRANCHES_RAW]

    # 70% individual, 30% corporate
    n_ind = int(n * 0.70)
    n_corp = n - n_ind

    for i in range(1, n + 1):
        is_corp = (i > n_ind)
        ctype = "Corporate" if is_corp else "Individual"
        rows.append({
            "customer_id":   f"CUS{i:04d}",
            "customer_name": fake_en.company() if is_corp else fake_en.name(),
            "customer_type": ctype,
            "age":           int(rng.integers(22, 70)) if not is_corp else None,
            "gender":        random.choice(["Male", "Female"]) if not is_corp else None,
            "governorate":   rng.choice([b[2] for b in BRANCHES_RAW]),
            "region":        None,   # derived from governorate — will fill below
            "home_branch_id": rng.choice(branch_ids),
            "is_returning":  random.choices([True, False], weights=[60, 40])[0],
        })

    gov_region = {b[2]: b[3] for b in BRANCHES_RAW}
    df = pd.DataFrame(rows)
    df["region"] = df["governorate"].map(gov_region).fillna("Greater Cairo")
    return df

# ─────────────────────────────────────────────
# FACT POLICIES
# ─────────────────────────────────────────────
# Product popularity weights
PRODUCT_WEIGHT = {
    "PR01": 30, "PR02": 25, "PR03": 12, "PR04": 6,
    "PR05": 5,  "PR06": 3,  "PR07": 10, "PR08": 4,
    "PR09": 3,  "PR10": 2,
}

# Channel weights
CHANNEL_WEIGHT = {
    "CH01": 0.30, "CH02": 0.35, "CH03": 0.20,
    "CH04": 0.10, "CH05": 0.05,
}

# Branch weights (HQ busiest)
BRANCH_WEIGHT = {
    "BR01": 8, "BR02": 5, "BR03": 5, "BR04": 6,
    "BR05": 3, "BR06": 3, "BR07": 2, "BR08": 2,
    "BR09": 3, "BR10": 3, "BR11": 2, "BR12": 2,
}

def policy_seasonality(month, product_category):
    # Travel peaks in summer; Motor peaks year-round; Engineering peaks Q1
    if product_category == "Travel":
        return {1:0.8,2:0.8,3:1.0,4:1.1,5:1.2,6:1.5,
                7:1.8,8:1.8,9:1.2,10:0.9,11:0.8,12:1.0}.get(month, 1.0)
    if product_category == "Engineering":
        return {1:1.5,2:1.4,3:1.2,4:1.0,5:0.9,6:0.8,
                7:0.8,8:0.8,9:0.9,10:1.0,11:1.1,12:1.2}.get(month, 1.0)
    # Default slight year-end bump (renewals)
    return {1:1.0,2:0.9,3:1.0,4:1.0,5:1.0,6:0.9,
            7:0.9,8:0.9,9:1.0,10:1.1,11:1.1,12:1.2}.get(month, 1.0)

PROD_INFO = {p[0]: p for p in PRODUCTS_RAW}

def gen_fact_policies(dim_date, dim_customer, dim_branch, dim_product, dim_channel):
    rng = np.random.default_rng(SEED + 20)
    prod_ids   = [p[0] for p in PRODUCTS_RAW]
    prod_wts   = [PRODUCT_WEIGHT[p] for p in prod_ids]
    ch_ids     = [c[0] for c in CHANNELS]
    ch_wts     = list(CHANNEL_WEIGHT.values())
    br_ids     = [b[0] for b in BRANCHES_RAW]
    br_wts     = [BRANCH_WEIGHT[b] for b in br_ids]
    cust_df    = dim_customer.copy()

    rows = []
    pol_id = 1

    for _ in range(TARGET_POLICY_ROWS):
        # Product first — drives customer type
        product_id   = random.choices(prod_ids, weights=prod_wts)[0]
        pinfo        = PROD_INFO[product_id]
        prod_ctype   = pinfo[3]   # "Individual" or "Corporate"
        prod_cat     = pinfo[2]
        p_min, p_max = pinfo[4], pinfo[5]
        loss_ratio   = pinfo[6]

        # Date with product-specific seasonality
        month_wts = [policy_seasonality(m, prod_cat) for m in range(1, 13)]
        # sample from date dim weighted by month
        date_row = dim_date.copy()
        date_row["w"] = date_row["month"].map(
            {m: policy_seasonality(m, prod_cat) for m in range(1, 13)}
        )
        date_row  = date_row.sample(1, weights="w").iloc[0]
        date_id   = date_row["date_id"]
        month     = date_row["month"]
        year      = date_row["year"]

        # Match customer type
        pool = cust_df[cust_df["customer_type"] == prod_ctype]
        if len(pool) == 0:
            pool = cust_df
        cust_row    = pool.sample(1).iloc[0]
        customer_id = cust_row["customer_id"]
        is_returning = cust_row["is_returning"]

        # Premium
        premium = round(rng.uniform(p_min, p_max), 2)

        # Cost (underwriting + admin): ~25-35% of premium
        underwriting_cost = round(premium * rng.uniform(0.10, 0.18), 2)
        admin_cost        = round(premium * rng.uniform(0.08, 0.15), 2)
        total_cost        = round(underwriting_cost + admin_cost, 2)

        # Expected claim reserve (probabilistic)
        expected_claim = round(premium * loss_ratio * rng.uniform(0.7, 1.3), 2)

        # Policy term
        term_months = random.choice([6, 12, 24])

        channel_id = random.choices(ch_ids, weights=ch_wts)[0]
        branch_id  = random.choices(br_ids, weights=br_wts)[0]

        policy_status = random.choices(
            ["Active", "Expired", "Cancelled"],
            weights=[65, 25, 10]
        )[0]

        rows.append({
            "policy_id":          f"POL{pol_id:05d}",
            "date_id":            date_id,
            "customer_id":        customer_id,
            "product_id":         product_id,
            "branch_id":          branch_id,
            "channel_id":         channel_id,
            "premium_egp":        premium,
            "underwriting_cost":  underwriting_cost,
            "admin_cost":         admin_cost,
            "total_cost":         total_cost,
            "expected_claim_reserve": expected_claim,
            "term_months":        term_months,
            "policy_status":      policy_status,
            "customer_type":      prod_ctype,
            "is_returning_customer": is_returning,
        })
        pol_id += 1

    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# FACT CLAIMS
# ─────────────────────────────────────────────
CLAIM_STATUSES = ["Approved", "Rejected", "Pending", "Under Review"]
STATUS_WEIGHTS = [55, 20, 15, 10]

def claims_seasonality(month, prod_cat):
    # Motor claims peak in winter (fog, rain); Property claims peak in summer (fire)
    if prod_cat == "Motor":
        return {1:1.5,2:1.4,3:1.1,4:1.0,5:0.9,6:0.8,
                7:0.8,8:0.9,9:1.0,10:1.1,11:1.2,12:1.4}.get(month, 1.0)
    if prod_cat == "Property":
        return {1:0.9,2:0.9,3:1.0,4:1.0,5:1.1,6:1.3,
                7:1.4,8:1.4,9:1.1,10:1.0,11:0.9,12:0.9}.get(month, 1.0)
    return 1.0

def gen_fact_claims(dim_date, fact_policies, dim_customer):
    rng     = np.random.default_rng(SEED + 30)
    # Only active/expired policies can have claims; sample from those
    eligible = fact_policies[
        fact_policies["policy_status"].isin(["Active", "Expired"])
    ].copy()

    prod_cat_map = {p[0]: p[2] for p in PRODUCTS_RAW}
    rows   = []
    cl_id  = 1

    for _ in range(TARGET_CLAIM_ROWS):
        pol_row    = eligible.sample(1).iloc[0]
        policy_id  = pol_row["policy_id"]
        date_id    = pol_row["date_id"]         # claim on same or later date
        product_id = pol_row["product_id"]
        customer_id = pol_row["customer_id"]
        branch_id   = pol_row["branch_id"]
        prod_cat    = prod_cat_map.get(product_id, "Motor")
        premium     = pol_row["premium_egp"]

        # Claim amount: 30–150% of premium (large single claim possible)
        pinfo    = PROD_INFO[product_id]
        loss_r   = pinfo[6]
        claim_amt = round(premium * loss_r * rng.uniform(0.5, 1.8), 2)
        claim_amt = max(claim_amt, 100)

        status = random.choices(CLAIM_STATUSES, weights=STATUS_WEIGHTS)[0]
        if status == "Rejected":
            amount_paid = 0.0
        elif status == "Approved":
            amount_paid = claim_amt
        else:
            amount_paid = 0.0  # pending / under review — not yet paid

        # Processing time in days
        proc_days = int(rng.integers(1, 7)   if status == "Rejected" else
                        rng.integers(5, 60)  if status == "Approved"  else
                        rng.integers(7, 90))

        claim_cause_map = {
            "Motor":       ["Accident", "Theft", "Natural Disaster", "Vandalism"],
            "Property":    ["Fire", "Flood", "Theft", "Structural Damage"],
            "Marine":      ["Cargo Damage", "Vessel Incident", "Weather", "Theft"],
            "Travel":      ["Medical Emergency", "Trip Cancellation", "Lost Luggage"],
            "Engineering": ["Equipment Failure", "Construction Accident", "Fire"],
            "Corporate Risk": ["Liability", "Property Loss", "Business Interruption"],
        }
        cause = random.choice(claim_cause_map.get(prod_cat, ["Other"]))

        rows.append({
            "claim_id":          f"CLM{cl_id:05d}",
            "date_id":           date_id,
            "policy_id":         policy_id,
            "customer_id":       customer_id,
            "branch_id":         branch_id,
            "product_id":        product_id,
            "claim_amount_egp":  claim_amt,
            "amount_paid_egp":   amount_paid,
            "claim_status":      status,
            "claim_cause":       cause,
            "processing_days":   proc_days,
            "product_category":  prod_cat,
        })
        cl_id += 1

    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# INJECT CLEANING ISSUES
# ─────────────────────────────────────────────
def inject_issues(df_pol, df_claims, df_customer, df_branch, df_product):
    n   = len(df_pol)
    nc  = len(df_claims)
    rng = np.random.default_rng(SEED + 99)

    # ── fact_policies ──────────────────────────
    # 1. ~5% nulls in admin_cost
    idx1 = rng.choice(n, size=int(n * 0.05), replace=False)
    df_pol.loc[idx1, "admin_cost"] = np.nan

    # 2. ~4% nulls in term_months
    idx2 = rng.choice(n, size=int(n * 0.04), replace=False)
    df_pol.loc[idx2, "term_months"] = np.nan

    # 3. Inconsistent casing in policy_status (~3%)
    idx3 = rng.choice(n, size=int(n * 0.03), replace=False)
    df_pol.loc[idx3, "policy_status"] = df_pol.loc[idx3, "policy_status"].str.upper()

    # 4. premium_egp stored as string in ~3% of rows
    df_pol["premium_egp"] = df_pol["premium_egp"].astype(object)
    idx4 = rng.choice(n, size=int(n * 0.03), replace=False)
    for i in idx4:
        df_pol.at[i, "premium_egp"] = str(df_pol.at[i, "premium_egp"])

    # 5. Impossible negative premium — 3 rows
    bad = rng.choice(n, size=3, replace=False)
    for i in bad:
        df_pol.at[i, "premium_egp"] = -abs(float(df_pol.at[i, "premium_egp"]))

    # 6. Duplicate rows (~1.5%)
    dup_idx = rng.choice(n, size=int(n * 0.015), replace=False)
    dups = df_pol.iloc[dup_idx].copy()
    df_pol = pd.concat([df_pol, dups], ignore_index=True)

    # ── fact_claims ────────────────────────────
    # 7. ~5% nulls in processing_days
    idx7 = rng.choice(nc, size=int(nc * 0.05), replace=False)
    df_claims.loc[idx7, "processing_days"] = np.nan

    # 8. Inconsistent casing in claim_status (~3%)
    idx8 = rng.choice(nc, size=int(nc * 0.03), replace=False)
    df_claims.loc[idx8, "claim_status"] = df_claims.loc[idx8, "claim_status"].str.lower()

    # 9. Leading whitespace in claim_cause (~2%)
    idx9 = rng.choice(nc, size=int(nc * 0.02), replace=False)
    df_claims.loc[idx9, "claim_cause"] = " " + df_claims.loc[idx9, "claim_cause"]

    # 10. Impossible negative processing_days — 3 rows
    bad2 = rng.choice(nc, size=3, replace=False)
    df_claims.loc[bad2, "processing_days"] = -rng.integers(1, 10, size=3).astype(float)

    # ── dim_customer ───────────────────────────
    # 11. Inconsistent customer_type casing for 4 rows
    s_idx = df_customer.sample(4, random_state=SEED).index
    df_customer.loc[s_idx, "customer_type"] = df_customer.loc[s_idx, "customer_type"].str.lower()

    # ── dim_product ────────────────────────────
    # 12. Inconsistent product_category casing for 2 rows
    df_product.loc[df_product["product_id"].isin(["PR07","PR08"]), "product_category"] = "travel"

    # ── dim_branch ─────────────────────────────
    # 13. Trailing whitespace in region for 3 rows
    df_branch.loc[df_branch["branch_id"].isin(["BR07","BR08","BR11"]), "region"] = "Upper Egypt "

    return df_pol, df_claims, df_customer, df_branch, df_product

# ─────────────────────────────────────────────
# VALIDATION
# ─────────────────────────────────────────────
def validate(df_pol, df_claims, dim_date, dim_branch, dim_customer,
             dim_channel, dim_product):
    print("\nValidation:")
    valid_dates   = set(dim_date["date_id"])
    valid_br      = set(dim_branch["branch_id"])
    valid_cust    = set(dim_customer["customer_id"])
    valid_ch      = set(dim_channel["channel_id"])
    valid_prod    = set(dim_product["product_id"])
    valid_pol     = set(df_pol["policy_id"])

    errors = []
    for col, valid, label in [
        ("date_id", valid_dates, "pol date_id"),
        ("branch_id", valid_br, "pol branch_id"),
        ("customer_id", valid_cust, "pol customer_id"),
        ("channel_id", valid_ch, "pol channel_id"),
        ("product_id", valid_prod, "pol product_id"),
    ]:
        bad = df_pol[~df_pol[col].isin(valid)]
        if len(bad): errors.append(f"  FK issue ({label}): {len(bad)} rows")

    # Claims: policy_id FK (allow — duplicates inflate pol IDs)
    for col, valid, label in [
        ("date_id", valid_dates, "clm date_id"),
        ("customer_id", valid_cust, "clm customer_id"),
        ("product_id", valid_prod, "clm product_id"),
    ]:
        bad = df_claims[~df_claims[col].isin(valid)]
        if len(bad): errors.append(f"  FK issue ({label}): {len(bad)} rows")

    for e in errors: print(e)
    if not errors: print("  FK checks passed.")

    dups = df_pol.duplicated().sum()
    npl  = (df_claims["claim_status"] == "Approved").mean()
    print(f"  fact_policies rows (incl. dupes): {len(df_pol)}")
    print(f"  Duplicate policy rows:            {dups}")
    print(f"  Null rate admin_cost:             {df_pol['admin_cost'].isna().mean():.1%}")
    print(f"  Null rate term_months:            {df_pol['term_months'].isna().mean():.1%}")
    print(f"  fact_claims rows:                 {len(df_claims)}")
    print(f"  Claim approval rate:              {npl:.1%}")
    print(f"  Null rate processing_days:        {df_claims['processing_days'].isna().mean():.1%}")

# ─────────────────────────────────────────────
# INSTRUCTOR NOTES
# ─────────────────────────────────────────────
CLEANING_MD = """\
# Expected Cleaning Tasks — Misr Insurance Company

## fact_policies.csv

| # | Issue | Column | Approx. Rate |
|---|-------|--------|--------------|
| 1 | Missing values | `admin_cost` | ~5% nulls |
| 2 | Missing values | `term_months` | ~4% nulls |
| 3 | Inconsistent casing | `policy_status` | ~3% uppercase ("ACTIVE", "EXPIRED") |
| 4 | Mixed data type | `premium_egp` | ~3% stored as text strings |
| 5 | Impossible negative values | `premium_egp` | 3 rows with negative premiums |
| 6 | Duplicate rows | all columns | ~1.5% fully duplicated records |

## fact_claims.csv

| # | Issue | Column | Approx. Rate |
|---|-------|--------|--------------|
| 7 | Missing values | `processing_days` | ~5% nulls |
| 8 | Inconsistent casing | `claim_status` | ~3% lowercase ("approved", "rejected") |
| 9 | Leading whitespace | `claim_cause` | ~2% with leading space |
| 10 | Impossible negative values | `processing_days` | 3 rows with negative values |

## dim_customer.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 11 | Inconsistent casing | `customer_type` | 4 rows lowercase ("individual", "corporate") |

## dim_product.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 12 | Inconsistent casing | `product_category` | "travel" (lowercase) for PR07, PR08 |

## dim_branch.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 13 | Trailing whitespace | `region` | "Upper Egypt " (trailing space) for BR07, BR08, BR11 |

## dim_date.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 14 | Date stored as string | `date` | Text "YYYY-MM-DD" — must be converted to Date type in Power Query |

## Notes for Instructor
- Negative `premium_egp` combined with text-type rows in the same column is a compound type issue — students must handle "Change Type" errors before filtering negatives.
- `claim_cause` whitespace causes grouping issues on the Claims by Cause chart — a very realistic, practical cleaning lesson.
- The `policy_status` uppercase issue will silently skew Active vs Cancelled ratios if uncleaned.
- Loss Ratio (claims paid / premium) is a key derived metric — it only works correctly after both fact tables are cleaned.
"""

DAX_MD = """\
# Suggested DAX Measures — Misr Insurance Company

## Financial KPIs
```dax
Total Premium Revenue =
    CALCULATE(
        SUM(fact_policies[premium_egp]),
        fact_policies[premium_egp] > 0
    )

Total Claims Paid =
    CALCULATE(
        SUM(fact_claims[amount_paid_egp]),
        fact_claims[claim_status] = "Approved"
    )

Total Underwriting Cost =
    SUM(fact_policies[underwriting_cost])

Total Admin Cost =
    SUM(fact_policies[admin_cost])

Total Cost =
    [Total Underwriting Cost] + [Total Admin Cost]

Net Profit =
    [Total Premium Revenue] - [Total Claims Paid] - [Total Cost]

Loss Ratio =
    DIVIDE([Total Claims Paid], [Total Premium Revenue])

Combined Ratio =
    DIVIDE([Total Claims Paid] + [Total Cost], [Total Premium Revenue])

Profit Margin % =
    DIVIDE([Net Profit], [Total Premium Revenue])
```

## Sales & Product KPIs
```dax
Total Policies Issued =
    COUNTROWS(fact_policies)

Active Policies =
    CALCULATE(COUNTROWS(fact_policies), fact_policies[policy_status] = "Active")

Cancellation Rate =
    DIVIDE(
        CALCULATE(COUNTROWS(fact_policies), fact_policies[policy_status] = "Cancelled"),
        [Total Policies Issued]
    )

Avg Premium per Policy =
    DIVIDE([Total Premium Revenue], [Total Policies Issued])

Revenue by Product =
    CALCULATE([Total Premium Revenue],
        ALLEXCEPT(dim_product, dim_product[product_id])
    )
```

## Claims & Operational KPIs
```dax
Total Claims Filed =
    COUNTROWS(fact_claims)

Claim Approval Rate =
    DIVIDE(
        CALCULATE(COUNTROWS(fact_claims), fact_claims[claim_status] = "Approved"),
        [Total Claims Filed]
    )

Claim Rejection Rate =
    DIVIDE(
        CALCULATE(COUNTROWS(fact_claims), fact_claims[claim_status] = "Rejected"),
        [Total Claims Filed]
    )

Avg Claim Processing Days =
    CALCULATE(
        AVERAGE(fact_claims[processing_days]),
        fact_claims[processing_days] > 0
    )

Claims per Month =
    DIVIDE([Total Claims Filed], DISTINCTCOUNT(dim_date[month]))
```

## Customer KPIs
```dax
Total Customers =
    DISTINCTCOUNT(fact_policies[customer_id])

Returning Customers =
    CALCULATE(
        DISTINCTCOUNT(fact_policies[customer_id]),
        fact_policies[is_returning_customer] = TRUE()
    )

Customer Retention Rate =
    DIVIDE([Returning Customers], [Total Customers])

New Customers =
    [Total Customers] - [Returning Customers]
```

## Growth & Time Intelligence
```dax
YTD Premium Revenue =
    TOTALYTD([Total Premium Revenue], dim_date[date])

MoM Premium Growth % =
    VAR Prev = CALCULATE([Total Premium Revenue], DATEADD(dim_date[date], -1, MONTH))
    RETURN DIVIDE([Total Premium Revenue] - Prev, Prev)

YoY Premium Growth % =
    DIVIDE(
        [Total Premium Revenue] - CALCULATE([Total Premium Revenue], SAMEPERIODLASTYEAR(dim_date[date])),
        CALCULATE([Total Premium Revenue], SAMEPERIODLASTYEAR(dim_date[date]))
    )
```
"""

DASHBOARD_MD = """\
# Dashboard Questions & Visual Suggestions — Misr Insurance Company

## Analytical Questions (student-facing prompts)
1. Which insurance product generates the highest premium revenue and net profit?
2. What is the overall Loss Ratio, and how does it vary by product category?
3. Which regions have the highest claim frequency and claim value?
4. How does premium revenue trend month-over-month and year-over-year?
5. What is the claim approval rate, and how long does processing typically take?
6. Which sales channel (Branch / Agent / Online) drives the most policies?
7. What share of customers are returning vs new, and how does this affect revenue?
8. Are there seasonal patterns in policy sales (e.g., Travel in summer, Motor in winter)?
9. Which branches perform best in terms of policy volume and premium collected?
10. How does the combined ratio compare to industry benchmarks?

## Suggested Visuals (instructor only)

| Visual | Type | Fields |
|--------|------|--------|
| Total Premium Revenue KPI | Card | [Total Premium Revenue] |
| Total Claims Paid KPI | Card | [Total Claims Paid] |
| Net Profit KPI | Card | [Net Profit] |
| Loss Ratio KPI | Card/Gauge | [Loss Ratio] |
| Claim Approval Rate KPI | Card | [Claim Approval Rate] |
| Premium Revenue over Time | Line | dim_date[month_name], [Total Premium Revenue] |
| Revenue by Product Category | Bar | dim_product[product_category], [Total Premium Revenue] |
| Claims by Product Category | Bar | dim_product[product_category], [Total Claims Paid] |
| Loss Ratio by Product | Bar | dim_product[product_name], [Loss Ratio] |
| Revenue by Region | Map / Bar | dim_branch[region], [Total Premium Revenue] |
| Claims by Cause | Treemap / Bar | fact_claims[claim_cause], count |
| Claim Status Breakdown | Donut | fact_claims[claim_status], count |
| Avg Processing Days by Product | Bar | dim_product[product_category], [Avg Claim Processing Days] |
| Channel Mix | Donut | dim_channel[channel_name], [Total Policies Issued] |
| Returning vs New Customers | Stacked bar | dim_date[year], [Returning Customers] + [New Customers] |
| YoY Revenue Comparison | Line (dual) | dim_date[month], [Total Premium Revenue] vs prev year |

## Suggested Slicers
- Year / Quarter / Month
- Product Category
- Region / Branch
- Customer Type (Individual / Corporate)
- Channel
- Claim Status
"""

MODEL_MD = """\
# Star Schema Relationships — Misr Insurance Company

## Tables
- **fact_policies** — main fact: insurance policies sold (~2,000+ rows)
- **fact_claims** — secondary fact: claims filed (~700 rows)
- **dim_date** — date dimension (shared)
- **dim_branch** — branch dimension (shared)
- **dim_customer** — customer dimension (shared)
- **dim_product** — insurance product dimension (shared)
- **dim_channel** — sales channel (policies only)

## Relationships

### fact_policies
| Fact Column | → | Dimension | PK | Cardinality | Filter |
|-------------|---|-----------|----|-------------|--------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single |
| `customer_id` | → | `dim_customer` | `customer_id` | Many-to-One | Single |
| `branch_id` | → | `dim_branch` | `branch_id` | Many-to-One | Single |
| `product_id` | → | `dim_product` | `product_id` | Many-to-One | Single |
| `channel_id` | → | `dim_channel` | `channel_id` | Many-to-One | Single |

### fact_claims
| Fact Column | → | Dimension | PK | Cardinality | Filter |
|-------------|---|-----------|----|-------------|--------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single |
| `customer_id` | → | `dim_customer` | `customer_id` | Many-to-One | Single |
| `branch_id` | → | `dim_branch` | `branch_id` | Many-to-One | Single |
| `product_id` | → | `dim_product` | `product_id` | Many-to-One | Single |

## Notes
- `fact_claims.policy_id` references `fact_policies.policy_id` — do NOT create a direct fact-to-fact relationship in Power BI. Route all analysis through shared dimensions.
- Both fact tables share `dim_date`, `dim_branch`, `dim_customer`, and `dim_product` — Power BI handles this correctly with separate relationships.
- `dim_channel` applies only to `fact_policies` (how the policy was sold); claims do not have a channel.
- Mark `dim_date[date]` as a **Date Table** after converting from string.
- Loss Ratio = [Total Claims Paid] / [Total Premium Revenue] — a key insurance KPI that spans both fact tables; students must be careful about filter context when calculating it.
"""

DATA_DICT_MD = """\
# Data Dictionary — Misr Insurance Company
## Digital Transformation Course · BINF 402 · GIU · Spring 2026

---

## Business Story
Misr Insurance Company is one of Egypt's leading non-life (general) insurance providers.
This dataset covers **insurance policies sold** and **claims filed** during 2023–2024.
Products include Motor, Property, Marine, Travel, Engineering, and Corporate Risk insurance.
Your goal as management is to track premium revenue, assess claims risk, and improve operational efficiency.

---

## Files

### `fact_policies.csv` (main fact table)
| Column | Description |
|--------|-------------|
| `policy_id` | Unique policy identifier |
| `date_id` | Foreign key → `dim_date.date_id` (policy issue date) |
| `customer_id` | Foreign key → `dim_customer.customer_id` |
| `product_id` | Foreign key → `dim_product.product_id` |
| `branch_id` | Foreign key → `dim_branch.branch_id` |
| `channel_id` | Foreign key → `dim_channel.channel_id` |
| `premium_egp` | Policy premium charged (EGP) |
| `underwriting_cost` | Cost to assess and underwrite the risk (EGP) |
| `admin_cost` | Administrative cost (EGP) |
| `total_cost` | Total cost (underwriting + admin) |
| `expected_claim_reserve` | Estimated reserve set aside for potential claims (EGP) |
| `term_months` | Policy duration in months |
| `policy_status` | Active, Expired, or Cancelled |
| `customer_type` | Individual or Corporate |
| `is_returning_customer` | Whether customer had a prior policy |

### `fact_claims.csv` (secondary fact table)
| Column | Description |
|--------|-------------|
| `claim_id` | Unique claim identifier |
| `date_id` | Foreign key → `dim_date.date_id` (claim filing date) |
| `policy_id` | Reference to the related policy |
| `customer_id` | Foreign key → `dim_customer.customer_id` |
| `branch_id` | Foreign key → `dim_branch.branch_id` |
| `product_id` | Foreign key → `dim_product.product_id` |
| `claim_amount_egp` | Amount claimed by the customer (EGP) |
| `amount_paid_egp` | Amount actually paid out (EGP; 0 if not approved) |
| `claim_status` | Approved, Rejected, Pending, or Under Review |
| `claim_cause` | Reason for the claim (e.g. Accident, Fire, Theft) |
| `processing_days` | Days taken to process the claim |
| `product_category` | Insurance category for quick filtering |

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
| `product_name` | Product name |
| `product_category` | Motor, Property, Marine, Travel, Engineering, Corporate Risk |
| `customer_type` | Primary target: Individual or Corporate |
| `premium_min_egp` | Typical minimum premium |
| `premium_max_egp` | Typical maximum premium |
| `expected_loss_ratio` | Historical expected claims-to-premium ratio |

### `dim_branch.csv`
| Column | Description |
|--------|-------------|
| `branch_id` | Primary key |
| `branch_name` | Branch name |
| `governorate` | Governorate |
| `region` | Region (Greater Cairo, Alexandria, Delta, Upper Egypt, Canal Zone) |

### `dim_customer.csv`
| Column | Description |
|--------|-------------|
| `customer_id` | Primary key |
| `customer_name` | Synthetic name |
| `customer_type` | Individual or Corporate |
| `age` | Age (individuals only) |
| `gender` | Gender (individuals only) |
| `governorate` | Customer's governorate |
| `region` | Region |
| `home_branch_id` | Primary branch |
| `is_returning` | Whether customer is a returning policyholder |

### `dim_channel.csv`
| Column | Description |
|--------|-------------|
| `channel_id` | Primary key |
| `channel_name` | Branch, Agent, Broker, Online, Call Center |
| `channel_type` | Offline or Digital |

---

## Intended Relationships
- `fact_policies` → `dim_date`, `dim_customer`, `dim_product`, `dim_branch`, `dim_channel`
- `fact_claims` → `dim_date`, `dim_customer`, `dim_product`, `dim_branch`

## Notes for Students
- Clean data types and fix inconsistencies **before** building relationships.
- The **Loss Ratio** (claims paid ÷ premium) is the most important insurance KPI — it spans both fact tables.
- Seasonal patterns exist: Motor claims peak in winter; Travel policies peak in summer.
- Do not create a direct relationship between the two fact tables — connect them through shared dimensions only.
"""

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print("=" * 55)
    print("Misr Insurance Company — Dataset Generator")
    print("=" * 55)
    make_dirs()

    print("\n[1/5] Generating dimension tables...")
    dim_date     = gen_dim_date()
    dim_product  = gen_dim_product()
    dim_branch   = gen_dim_branch()
    dim_channel  = gen_dim_channel()
    dim_customer = gen_dim_customer(n=180)

    print("\n[2/5] Generating fact tables...")
    fact_pol    = gen_fact_policies(dim_date, dim_customer, dim_branch, dim_product, dim_channel)
    fact_claims = gen_fact_claims(dim_date, fact_pol, dim_customer)

    print("\n[3/5] Injecting cleaning issues...")
    fact_pol, fact_claims, dim_customer, dim_branch, dim_product = inject_issues(
        fact_pol, fact_claims, dim_customer, dim_branch, dim_product
    )

    print("\n[4/5] Saving files...")
    save(dim_date,     f"{STUDENT_DIR}/dim_date.csv")
    save(dim_product,  f"{STUDENT_DIR}/dim_product.csv")
    save(dim_branch,   f"{STUDENT_DIR}/dim_branch.csv")
    save(dim_channel,  f"{STUDENT_DIR}/dim_channel.csv")
    save(dim_customer, f"{STUDENT_DIR}/dim_customer.csv")
    save(fact_pol,     f"{STUDENT_DIR}/fact_policies.csv")
    save(fact_claims,  f"{STUDENT_DIR}/fact_claims.csv")

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
    validate(fact_pol, fact_claims, dim_date, dim_branch,
             dim_customer, dim_channel, dim_product)

    print("\n" + "=" * 55)
    print("Done. Output folder: output/misr_insurance/")
    print("  student_dataset/          → share with students")
    print("  data_dictionary.md        → share with students")
    print("  private_instructor_notes/ → instructor only")
    print("=" * 55)

if __name__ == "__main__":
    main()

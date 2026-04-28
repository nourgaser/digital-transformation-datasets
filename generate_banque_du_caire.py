"""
Banque du Caire — Egyptian Commercial Bank
Dataset Generator for Digital Transformation Course - BINF 402, Spring 2026
GIU - Dr. Nourhan Hamdi
Team Coordinator: Abdullah Abouelleil
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

PROJECT_SLUG = "banque_du_caire"
OUTPUT_BASE  = f"output/{PROJECT_SLUG}"
STUDENT_DIR  = f"{OUTPUT_BASE}/student_dataset"
PRIVATE_DIR  = f"{OUTPUT_BASE}/private_instructor_notes"

DATE_START = date(2023, 1, 1)
DATE_END   = date(2024, 12, 31)
TARGET_TXN_ROWS  = 2000
TARGET_LOAN_ROWS = 600

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
# DIM BRANCH
# ─────────────────────────────────────────────
BRANCHES_RAW = [
    # (branch_id, name, governorate, region, tier)
    ("BR01", "Downtown Cairo",         "Cairo",       "Greater Cairo",  "Tier 1"),
    ("BR02", "Heliopolis",             "Cairo",       "Greater Cairo",  "Tier 1"),
    ("BR03", "Maadi",                  "Cairo",       "Greater Cairo",  "Tier 1"),
    ("BR04", "Nasr City",              "Cairo",       "Greater Cairo",  "Tier 1"),
    ("BR05", "6th of October",         "Giza",        "Greater Cairo",  "Tier 2"),
    ("BR06", "Dokki",                  "Giza",        "Greater Cairo",  "Tier 2"),
    ("BR07", "Alexandria Main",        "Alexandria",  "Alexandria",     "Tier 1"),
    ("BR08", "Smouha",                 "Alexandria",  "Alexandria",     "Tier 2"),
    ("BR09", "Mansoura",               "Dakahlia",    "Delta",          "Tier 2"),
    ("BR10", "Tanta",                  "Gharbia",     "Delta",          "Tier 2"),
    ("BR11", "Luxor",                  "Luxor",       "Upper Egypt",    "Tier 3"),
    ("BR12", "Aswan",                  "Aswan",       "Upper Egypt",    "Tier 3"),
    ("BR13", "Asyut",                  "Asyut",       "Upper Egypt",    "Tier 3"),
    ("BR14", "Port Said",              "Port Said",   "Canal Zone",     "Tier 2"),
    ("BR15", "Suez",                   "Suez",        "Canal Zone",     "Tier 2"),
]

def gen_dim_branch():
    rows = []
    for b in BRANCHES_RAW:
        bid, name, gov, region, tier = b
        rows.append({
            "branch_id":    bid,
            "branch_name":  name,
            "governorate":  gov,
            "region":       region,
            "branch_tier":  tier,
        })
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# DIM CUSTOMER
# ─────────────────────────────────────────────
SEGMENTS = ["Retail", "Premium", "SME", "Corporate"]
SEG_WEIGHTS = [55, 20, 15, 10]

def gen_dim_customer(n=200):
    rng  = np.random.default_rng(SEED + 5)
    rows = []
    branch_ids = [b[0] for b in BRANCHES_RAW]

    for i in range(1, n + 1):
        seg = random.choices(SEGMENTS, weights=SEG_WEIGHTS)[0]
        age = int(rng.integers(22, 65)) if seg in ("Retail","Premium") else None
        rows.append({
            "customer_id":       f"CUS{i:04d}",
            "customer_name":     fake_en.name(),
            "segment":           seg,
            "age":               age,
            "gender":            random.choice(["Male","Female"]) if seg in ("Retail","Premium") else None,
            "governorate":       rng.choice([b[2] for b in BRANCHES_RAW]),
            "home_branch_id":    rng.choice(branch_ids),
            "digital_enrolled":  random.choices([True, False], weights=[65, 35])[0],
            "since_year":        int(rng.integers(2005, 2024)),
        })
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# DIM PRODUCT
# ─────────────────────────────────────────────
PRODUCTS_RAW = [
    # (product_id, name, type, category)
    ("P01", "Personal Loan",          "Loan",           "Retail"),
    ("P02", "Car Loan",               "Loan",           "Retail"),
    ("P03", "Mortgage Loan",          "Loan",           "Retail"),
    ("P04", "SME Business Loan",      "Loan",           "SME"),
    ("P05", "Corporate Credit Line",  "Loan",           "Corporate"),
    ("P06", "Credit Card - Classic",  "Credit Card",    "Retail"),
    ("P07", "Credit Card - Gold",     "Credit Card",    "Premium"),
    ("P08", "Credit Card - Platinum", "Credit Card",    "Premium"),
    ("P09", "Savings Account",        "Deposit",        "Retail"),
    ("P10", "Current Account",        "Deposit",        "Retail"),
    ("P11", "Fixed Deposit",          "Deposit",        "Premium"),
    ("P12", "Mobile Banking",         "Digital",        "Retail"),
    ("P13", "Internet Banking",       "Digital",        "Retail"),
    ("P14", "Digital Wallet",         "Digital",        "Retail"),
    ("P15", "Trade Finance",          "Trade Finance",  "Corporate"),
]

def gen_dim_product():
    rows = [{"product_id": pid, "product_name": name,
             "product_type": ptype, "target_segment": seg}
            for pid, name, ptype, seg in PRODUCTS_RAW]
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# DIM CHANNEL
# ─────────────────────────────────────────────
CHANNELS = [
    ("CH01", "In-Branch",       "Physical"),
    ("CH02", "ATM",             "Physical"),
    ("CH03", "Mobile App",      "Digital"),
    ("CH04", "Internet Banking","Digital"),
    ("CH05", "Call Center",     "Digital"),
]

def gen_dim_channel():
    rows = [{"channel_id": cid, "channel_name": name, "channel_type": ctype}
            for cid, name, ctype in CHANNELS]
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# FACT TRANSACTIONS
# ─────────────────────────────────────────────
TXN_TYPES = ["Deposit", "Withdrawal", "Transfer", "Loan Payment",
             "Card Payment", "Bill Payment", "Account Opening Fee"]

# Channel weights shift toward digital over time (2024 more digital than 2023)
def channel_weights(year):
    if year == 2023:
        return {"CH01": 0.35, "CH02": 0.25, "CH03": 0.20, "CH04": 0.12, "CH05": 0.08}
    else:  # 2024 — more digital adoption
        return {"CH01": 0.28, "CH02": 0.20, "CH03": 0.28, "CH04": 0.16, "CH05": 0.08}

BRANCH_TIER_WEIGHT = {"Tier 1": 5, "Tier 2": 3, "Tier 3": 1}

# Transaction amount ranges (EGP) by type
AMOUNT_RANGE = {
    "Deposit":            (500,    50000),
    "Withdrawal":         (200,    20000),
    "Transfer":           (500,   100000),
    "Loan Payment":       (1000,   30000),
    "Card Payment":       (100,    15000),
    "Bill Payment":       (50,      5000),
    "Account Opening Fee":(100,      500),
}

def gen_fact_transactions(dim_date, dim_branch, dim_customer, dim_channel):
    rng        = np.random.default_rng(SEED + 20)
    branch_ids = [b[0] for b in BRANCHES_RAW]
    branch_tier= {b[0]: b[4] for b in BRANCHES_RAW}
    branch_wts = [BRANCH_TIER_WEIGHT[branch_tier[b]] for b in branch_ids]
    ch_ids     = [c[0] for c in CHANNELS]
    cust_ids   = dim_customer["customer_id"].tolist()

    rows = []
    txn_id = 1

    for _ in range(TARGET_TXN_ROWS):
        date_row  = dim_date.sample(1).iloc[0]
        date_id   = date_row["date_id"]
        year      = date_row["year"]
        month     = date_row["month"]

        branch_id  = random.choices(branch_ids, weights=branch_wts)[0]
        customer_id = rng.choice(cust_ids)
        cust_row    = dim_customer[dim_customer["customer_id"] == customer_id].iloc[0]
        segment     = cust_row["segment"]

        # Channel — digital adoption grows in 2024
        cw = channel_weights(year)
        channel_id = random.choices(ch_ids, weights=list(cw.values()))[0]

        # If digital channel, branch may be None (online)
        if channel_id in ("CH03", "CH04", "CH05"):
            effective_branch = None
        else:
            effective_branch = branch_id

        txn_type = random.choice(TXN_TYPES)
        lo, hi   = AMOUNT_RANGE[txn_type]
        # Corporate/Premium transact larger amounts
        if segment in ("Corporate", "SME"):
            lo, hi = lo * 3, hi * 5
        elif segment == "Premium":
            lo, hi = int(lo * 1.5), int(hi * 2)
        amount = round(rng.uniform(lo, hi), 2)

        # Fee revenue: small % of transaction amount
        fee = round(amount * rng.uniform(0.001, 0.005), 2) if txn_type in (
            "Transfer", "Bill Payment", "Account Opening Fee") else 0.0

        rows.append({
            "transaction_id":  f"TXN{txn_id:06d}",
            "date_id":         date_id,
            "customer_id":     customer_id,
            "branch_id":       effective_branch,
            "channel_id":      channel_id,
            "transaction_type": txn_type,
            "amount_egp":      amount,
            "fee_egp":         fee,
            "customer_segment": segment,
            "is_digital":      channel_id in ("CH03", "CH04", "CH05"),
        })
        txn_id += 1

    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# FACT LOANS
# ─────────────────────────────────────────────
LOAN_PRODUCTS = ["P01", "P02", "P03", "P04", "P05"]
LOAN_PRODUCT_INFO = {
    "P01": {"name": "Personal Loan",     "min": 10000,  "max": 500000,   "rate_range": (0.14, 0.22)},
    "P02": {"name": "Car Loan",          "min": 50000,  "max": 1000000,  "rate_range": (0.12, 0.18)},
    "P03": {"name": "Mortgage Loan",     "min": 200000, "max": 5000000,  "rate_range": (0.10, 0.16)},
    "P04": {"name": "SME Business Loan", "min": 100000, "max": 3000000,  "rate_range": (0.14, 0.20)},
    "P05": {"name": "Corporate Credit",  "min": 500000, "max": 20000000, "rate_range": (0.10, 0.15)},
}
RISK_LEVELS   = ["Low", "Medium", "High"]
RISK_WEIGHTS  = [50, 35, 15]
LOAN_STATUSES = ["Approved", "Rejected", "Pending", "Defaulted", "Closed"]
STATUS_WEIGHTS = [55, 20, 8, 10, 7]

def gen_fact_loans(dim_date, dim_customer, dim_branch):
    rng       = np.random.default_rng(SEED + 30)
    cust_ids  = dim_customer["customer_id"].tolist()
    seg_map   = dim_customer.set_index("customer_id")["segment"].to_dict()
    branch_ids = [b[0] for b in BRANCHES_RAW]

    rows = []
    loan_id = 1

    for _ in range(TARGET_LOAN_ROWS):
        date_row    = dim_date.sample(1).iloc[0]
        date_id     = date_row["date_id"]
        customer_id = rng.choice(cust_ids)
        segment     = seg_map[customer_id]

        # Match product to segment
        if segment == "Corporate":
            product_id = random.choices(["P04","P05"], weights=[3,7])[0]
        elif segment == "SME":
            product_id = random.choices(["P01","P04"], weights=[3,7])[0]
        elif segment == "Premium":
            product_id = random.choices(["P01","P02","P03"], weights=[3,3,4])[0]
        else:
            product_id = random.choices(["P01","P02","P03"], weights=[5,3,2])[0]

        pinfo     = LOAN_PRODUCT_INFO[product_id]
        principal = round(rng.uniform(pinfo["min"], pinfo["max"]), -3)  # round to thousands
        rate      = round(rng.uniform(*pinfo["rate_range"]), 4)
        term_months = random.choice([12, 24, 36, 48, 60, 84, 120])

        monthly_payment = round(
            principal * (rate / 12) / (1 - (1 + rate / 12) ** (-term_months)), 2
        )
        risk_level = random.choices(RISK_LEVELS, weights=RISK_WEIGHTS)[0]

        # Defaulted loans tend to have High risk
        if risk_level == "High":
            status = random.choices(LOAN_STATUSES, weights=[40, 15, 5, 30, 10])[0]
        else:
            status = random.choices(LOAN_STATUSES, weights=STATUS_WEIGHTS)[0]

        is_npl = status == "Defaulted"
        branch_id = rng.choice(branch_ids)

        rows.append({
            "loan_id":          f"LN{loan_id:05d}",
            "date_id":          date_id,
            "customer_id":      customer_id,
            "branch_id":        branch_id,
            "product_id":       product_id,
            "principal_egp":    principal,
            "interest_rate":    rate,
            "term_months":      term_months,
            "monthly_payment":  monthly_payment,
            "risk_level":       risk_level,
            "loan_status":      status,
            "is_npl":           is_npl,
            "customer_segment": segment,
        })
        loan_id += 1

    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# INJECT CLEANING ISSUES
# ─────────────────────────────────────────────
def inject_issues(df_txn, df_loans, df_customer, df_branch):
    n   = len(df_txn)
    rng = np.random.default_rng(SEED + 99)

    # ── fact_transactions ──────────────────────
    # 1. ~5% nulls in branch_id (already None for digital — add extra nulls in physical rows)
    phys_idx = df_txn[df_txn["branch_id"].notna()].index.tolist()
    extra_null = rng.choice(phys_idx, size=int(len(phys_idx) * 0.04), replace=False)
    df_txn.loc[extra_null, "branch_id"] = np.nan

    # 2. ~4% nulls in fee_egp
    idx2 = rng.choice(n, size=int(n * 0.04), replace=False)
    df_txn.loc[idx2, "fee_egp"] = np.nan

    # 3. Inconsistent casing in transaction_type (~3%)
    idx3 = rng.choice(n, size=int(n * 0.03), replace=False)
    df_txn.loc[idx3, "transaction_type"] = df_txn.loc[idx3, "transaction_type"].str.lower()

    # 4. amount_egp stored as string in ~3% of rows
    df_txn["amount_egp"] = df_txn["amount_egp"].astype(object)
    idx4 = rng.choice(n, size=int(n * 0.03), replace=False)
    for i in idx4:
        df_txn.at[i, "amount_egp"] = str(df_txn.at[i, "amount_egp"])

    # 5. Negative amount (impossible) — 4 rows
    bad = rng.choice(n, size=4, replace=False)
    for i in bad:
        df_txn.at[i, "amount_egp"] = -abs(float(df_txn.at[i, "amount_egp"]))

    # 6. Duplicate rows (~1.5%)
    dup_idx = rng.choice(n, size=int(n * 0.015), replace=False)
    dups = df_txn.iloc[dup_idx].copy()
    df_txn = pd.concat([df_txn, dups], ignore_index=True)

    # ── fact_loans ─────────────────────────────
    nl = len(df_loans)
    # 7. ~5% nulls in interest_rate
    idx7 = rng.choice(nl, size=int(nl * 0.05), replace=False)
    df_loans.loc[idx7, "interest_rate"] = np.nan

    # 8. Inconsistent casing in risk_level (~3%)
    idx8 = rng.choice(nl, size=int(nl * 0.03), replace=False)
    df_loans.loc[idx8, "risk_level"] = df_loans.loc[idx8, "risk_level"].str.upper()

    # 9. loan_status with leading whitespace (~2%)
    idx9 = rng.choice(nl, size=int(nl * 0.02), replace=False)
    df_loans.loc[idx9, "loan_status"] = " " + df_loans.loc[idx9, "loan_status"]

    # ── dim_customer ───────────────────────────
    # 10. Inconsistent segment casing for 4 rows
    s_idx = df_customer.sample(4, random_state=SEED).index
    df_customer.loc[s_idx, "segment"] = df_customer.loc[s_idx, "segment"].str.lower()

    # 11. branch_tier with trailing whitespace in dim_branch
    df_branch.loc[df_branch["branch_id"].isin(["BR11","BR12","BR13"]), "branch_tier"] = "Tier 3 "

    return df_txn, df_loans, df_customer, df_branch

# ─────────────────────────────────────────────
# VALIDATION
# ─────────────────────────────────────────────
def validate(df_txn, df_loans, dim_date, dim_branch, dim_customer, dim_channel, dim_product):
    print("\nValidation:")
    valid_dates    = set(dim_date["date_id"])
    valid_branches = set(dim_branch["branch_id"]) | {None, np.nan}
    valid_custs    = set(dim_customer["customer_id"])
    valid_channels = set(dim_channel["channel_id"])
    valid_products = set(dim_product["product_id"])

    # FK checks (ignoring nulls)
    bad_date_t  = df_txn[~df_txn["date_id"].isin(valid_dates)]
    bad_cust_t  = df_txn[~df_txn["customer_id"].isin(valid_custs)]
    bad_ch_t    = df_txn[~df_txn["channel_id"].isin(valid_channels)]
    bad_date_l  = df_loans[~df_loans["date_id"].isin(valid_dates)]
    bad_prod_l  = df_loans[~df_loans["product_id"].isin(valid_products)]

    for label, df_bad in [("txn date_id", bad_date_t), ("txn customer_id", bad_cust_t),
                           ("txn channel_id", bad_ch_t), ("loan date_id", bad_date_l),
                           ("loan product_id", bad_prod_l)]:
        if len(df_bad):
            print(f"  FK issue ({label}): {len(df_bad)} rows")

    dups_t = df_txn.duplicated().sum()
    print(f"  fact_transactions rows:    {len(df_txn)}")
    print(f"  Duplicate rows (txn):      {dups_t}")
    print(f"  Null rate fee_egp:         {df_txn['fee_egp'].isna().mean():.1%}")
    print(f"  Null rate txn amount str:  {(df_txn['amount_egp'].apply(lambda x: isinstance(x, str))).mean():.1%}")
    print(f"  fact_loans rows:           {len(df_loans)}")
    print(f"  NPL rate:                  {df_loans['is_npl'].mean():.1%}")
    print(f"  Null rate interest_rate:   {df_loans['interest_rate'].isna().mean():.1%}")

# ─────────────────────────────────────────────
# INSTRUCTOR NOTES
# ─────────────────────────────────────────────
CLEANING_MD = """\
# Expected Cleaning Tasks — Banque du Caire

## fact_transactions.csv

| # | Issue | Column | Approx. Rate |
|---|-------|--------|--------------|
| 1 | Missing values (intentional: digital txns have no branch) | `branch_id` | ~30% null (mix of intentional + injected) |
| 2 | Missing values | `fee_egp` | ~4% nulls |
| 3 | Inconsistent casing | `transaction_type` | ~3% lowercase ("deposit", "withdrawal") |
| 4 | Mixed data type | `amount_egp` | ~3% stored as text strings |
| 5 | Negative impossible values | `amount_egp` | 4 rows with negative amounts |
| 6 | Duplicate rows | all columns | ~1.5% fully duplicated records |

## fact_loans.csv

| # | Issue | Column | Approx. Rate |
|---|-------|--------|--------------|
| 7 | Missing values | `interest_rate` | ~5% nulls |
| 8 | Inconsistent casing | `risk_level` | ~3% uppercase ("HIGH", "MEDIUM") |
| 9 | Leading whitespace | `loan_status` | ~2% with leading space |

## dim_customer.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 10 | Inconsistent casing | `segment` | 4 rows lowercase ("retail", "premium") |

## dim_branch.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 11 | Trailing whitespace | `branch_tier` | "Tier 3 " (trailing space) for BR11, BR12, BR13 |

## dim_date.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 12 | Date stored as string | `date` | Text "YYYY-MM-DD" — must be converted to Date type in Power Query |

## Notes for Instructor
- `branch_id` nulls in fact_transactions are **intentional** for digital channels (no physical branch). Students must understand this is NOT an error for digital rows, but IS an error for the extra injected nulls on physical rows. A good student will filter by `is_digital` before investigating nulls.
- Negative `amount_egp` combined with text-type `amount_egp` in the same column is a compound issue — students must fix the type first, then filter the negatives.
- The loan NPL rate is ~15%, which is realistic for an Egyptian bank and enables meaningful risk analysis.
"""

DAX_MD = """\
# Suggested DAX Measures — Banque du Caire

## Financial Performance
```dax
Total Transaction Volume =
    CALCULATE(
        SUM(fact_transactions[amount_egp]),
        fact_transactions[amount_egp] > 0
    )

Total Fee Revenue =
    SUM(fact_transactions[fee_egp])

Total Loan Portfolio =
    CALCULATE(
        SUM(fact_loans[principal_egp]),
        fact_loans[loan_status] = "Approved"
    )

Total NPL Value =
    CALCULATE(
        SUM(fact_loans[principal_egp]),
        fact_loans[is_npl] = TRUE()
    )

NPL Ratio =
    DIVIDE([Total NPL Value], [Total Loan Portfolio])
```

## Loan & Credit Performance
```dax
Total Loans =
    COUNTROWS(fact_loans)

Loan Approval Rate =
    DIVIDE(
        CALCULATE(COUNTROWS(fact_loans), fact_loans[loan_status] = "Approved"),
        [Total Loans]
    )

Loan Rejection Rate =
    DIVIDE(
        CALCULATE(COUNTROWS(fact_loans), fact_loans[loan_status] = "Rejected"),
        [Total Loans]
    )

Avg Interest Rate =
    AVERAGE(fact_loans[interest_rate])

Avg Loan Size =
    CALCULATE(
        AVERAGE(fact_loans[principal_egp]),
        fact_loans[loan_status] = "Approved"
    )
```

## Customer & Digital KPIs
```dax
Total Customers =
    DISTINCTCOUNT(fact_transactions[customer_id])

Digital Transactions =
    CALCULATE(COUNTROWS(fact_transactions), fact_transactions[is_digital] = TRUE())

Physical Transactions =
    CALCULATE(COUNTROWS(fact_transactions), fact_transactions[is_digital] = FALSE())

Digital Adoption Rate =
    DIVIDE([Digital Transactions], COUNTROWS(fact_transactions))

Avg Transactions per Customer =
    DIVIDE(COUNTROWS(fact_transactions), [Total Customers])
```

## Branch Performance
```dax
Revenue per Branch =
    DIVIDE([Total Fee Revenue], DISTINCTCOUNT(fact_transactions[branch_id]))

Transaction Volume by Branch =
    CALCULATE([Total Transaction Volume],
        ALLEXCEPT(dim_branch, dim_branch[branch_id])
    )
```

## Growth & Time Intelligence
```dax
YTD Transaction Volume =
    TOTALYTD([Total Transaction Volume], dim_date[date])

MoM Volume Growth % =
    VAR Prev = CALCULATE([Total Transaction Volume], DATEADD(dim_date[date], -1, MONTH))
    RETURN DIVIDE([Total Transaction Volume] - Prev, Prev)

YoY Volume Growth % =
    DIVIDE(
        [Total Transaction Volume] - CALCULATE([Total Transaction Volume], SAMEPERIODLASTYEAR(dim_date[date])),
        CALCULATE([Total Transaction Volume], SAMEPERIODLASTYEAR(dim_date[date]))
    )
```
"""

DASHBOARD_MD = """\
# Dashboard Questions & Visual Suggestions — Banque du Caire

## Analytical Questions (student-facing prompts)
1. What is the total transaction volume, and how has it grown year-over-year?
2. How is the loan portfolio distributed across product types and customer segments?
3. What is the Non-Performing Loan (NPL) ratio, and which segments drive it?
4. How does digital transaction adoption compare to in-branch over 2023 vs 2024?
5. Which branches generate the highest transaction volumes and fee revenue?
6. What is the loan approval vs rejection rate, and how does it vary by risk level?
7. Which customer segments (Retail, Premium, SME, Corporate) contribute most to volume?
8. How does transaction volume vary by month — are there seasonal peaks?
9. What share of customers are digitally enrolled, and how does that affect their behavior?
10. Which regions (Cairo, Delta, Upper Egypt) are most active in terms of transactions and loans?

## Suggested Visuals (instructor only)

| Visual | Type | Fields |
|--------|------|--------|
| Total Transaction Volume KPI | Card | [Total Transaction Volume] |
| NPL Ratio KPI | Card/Gauge | [NPL Ratio] |
| Loan Approval Rate KPI | Card | [Loan Approval Rate] |
| Digital Adoption Rate KPI | Card | [Digital Adoption Rate] |
| Transaction Volume over Time | Line | dim_date[month_name], [Total Transaction Volume] |
| Digital vs Physical Trend | Line (dual) | dim_date[month], [Digital Transactions] + [Physical Transactions] |
| Volume by Branch | Bar | dim_branch[branch_name], [Total Transaction Volume] |
| Volume by Region | Map / Bar | dim_branch[region], [Total Transaction Volume] |
| Loan Portfolio by Type | Donut | dim_product[product_name], [Total Loan Portfolio] |
| Loan Status Breakdown | Stacked bar | fact_loans[loan_status], count |
| NPL by Customer Segment | Bar | dim_customer[segment], [NPL Ratio] |
| Risk Level Distribution | Pie | fact_loans[risk_level], count |
| Transactions by Type | Treemap | fact_transactions[transaction_type], [Total Transaction Volume] |
| Digital Adoption YoY | Clustered bar | dim_date[year], [Digital Adoption Rate] |

## Suggested Slicers
- Year / Quarter
- Branch / Region
- Customer Segment
- Channel Type (Digital / Physical)
- Product Type
- Loan Status
"""

MODEL_MD = """\
# Star Schema Relationships — Banque du Caire

## Tables
- **fact_transactions** — main fact table: banking transactions (~2,000+ rows)
- **fact_loans** — secondary fact table: loan applications and performance (~600 rows)
- **dim_date** — date dimension (shared)
- **dim_branch** — branch dimension (shared)
- **dim_customer** — customer dimension
- **dim_channel** — channel dimension (transactions only)
- **dim_product** — product dimension (loans only)

## Relationships

### fact_transactions
| Fact Column | → | Dimension | PK | Cardinality | Filter |
|-------------|---|-----------|----|-------------|--------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single |
| `branch_id` | → | `dim_branch` | `branch_id` | Many-to-One | Single |
| `customer_id` | → | `dim_customer` | `customer_id` | Many-to-One | Single |
| `channel_id` | → | `dim_channel` | `channel_id` | Many-to-One | Single |

### fact_loans
| Fact Column | → | Dimension | PK | Cardinality | Filter |
|-------------|---|-----------|----|-------------|--------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single |
| `branch_id` | → | `dim_branch` | `branch_id` | Many-to-One | Single |
| `customer_id` | → | `dim_customer` | `customer_id` | Many-to-One | Single |
| `product_id` | → | `dim_product` | `product_id` | Many-to-One | Single |

## Notes
- `branch_id` in `fact_transactions` is nullable — digital transactions have no branch. Students must handle this in visuals (e.g., use ISBLANK checks).
- Both fact tables share `dim_date`, `dim_branch`, and `dim_customer`. Power BI handles this correctly; do NOT create cross-fact relationships.
- Mark `dim_date[date]` as a **Date Table** after converting from string to Date type.
- `dim_channel` is only relevant to `fact_transactions`; `dim_product` only to `fact_loans`.
"""

DATA_DICT_MD = """\
# Data Dictionary — Banque du Caire
## Digital Transformation Course · BINF 402 · GIU · Spring 2026

---

## Business Story
Banque du Caire is an Egyptian commercial bank offering retail, SME, and corporate banking services.
This dataset covers **banking transactions** and **loan applications** for 2023–2024 across 15 branches nationwide.
Your goal as management is to monitor financial performance, assess loan risk, and track the bank's shift toward digital channels.

---

## Files

### `fact_transactions.csv` (main fact table)
| Column | Description |
|--------|-------------|
| `transaction_id` | Unique transaction identifier |
| `date_id` | Foreign key → `dim_date.date_id` |
| `customer_id` | Foreign key → `dim_customer.customer_id` |
| `branch_id` | Foreign key → `dim_branch.branch_id` (null for digital channels) |
| `channel_id` | Foreign key → `dim_channel.channel_id` |
| `transaction_type` | Type: Deposit, Withdrawal, Transfer, Loan Payment, etc. |
| `amount_egp` | Transaction value (EGP) |
| `fee_egp` | Fee charged for the transaction (EGP) |
| `customer_segment` | Customer segment at time of transaction |
| `is_digital` | True if transaction was through a digital channel |

### `fact_loans.csv` (secondary fact table)
| Column | Description |
|--------|-------------|
| `loan_id` | Unique loan identifier |
| `date_id` | Foreign key → `dim_date.date_id` (application date) |
| `customer_id` | Foreign key → `dim_customer.customer_id` |
| `branch_id` | Foreign key → `dim_branch.branch_id` |
| `product_id` | Foreign key → `dim_product.product_id` |
| `principal_egp` | Loan principal amount (EGP) |
| `interest_rate` | Annual interest rate (decimal, e.g. 0.14 = 14%) |
| `term_months` | Loan duration in months |
| `monthly_payment` | Calculated monthly installment (EGP) |
| `risk_level` | Risk assessment: Low, Medium, or High |
| `loan_status` | Approved, Rejected, Pending, Defaulted, or Closed |
| `is_npl` | True if loan is Non-Performing (Defaulted) |
| `customer_segment` | Customer segment |

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

### `dim_branch.csv`
| Column | Description |
|--------|-------------|
| `branch_id` | Primary key |
| `branch_name` | Branch name/area |
| `governorate` | Governorate location |
| `region` | Broader region (Greater Cairo, Alexandria, Delta, etc.) |
| `branch_tier` | Tier 1 (high volume), Tier 2, or Tier 3 |

### `dim_customer.csv`
| Column | Description |
|--------|-------------|
| `customer_id` | Primary key |
| `customer_name` | Synthetic customer name |
| `segment` | Retail, Premium, SME, or Corporate |
| `age` | Age (individuals only; blank for companies) |
| `gender` | Gender (individuals only) |
| `governorate` | Customer's governorate |
| `home_branch_id` | Primary branch |
| `digital_enrolled` | Whether customer is enrolled in digital banking |
| `since_year` | Year customer joined the bank |

### `dim_channel.csv`
| Column | Description |
|--------|-------------|
| `channel_id` | Primary key |
| `channel_name` | In-Branch, ATM, Mobile App, Internet Banking, Call Center |
| `channel_type` | Physical or Digital |

### `dim_product.csv`
| Column | Description |
|--------|-------------|
| `product_id` | Primary key |
| `product_name` | Product name |
| `product_type` | Loan, Credit Card, Deposit, Digital, Trade Finance |
| `target_segment` | Primary target customer segment |

---

## Intended Relationships
- `fact_transactions` → `dim_date`, `dim_branch`, `dim_customer`, `dim_channel`
- `fact_loans` → `dim_date`, `dim_branch`, `dim_customer`, `dim_product`

## Notes for Students
- `branch_id` is intentionally null for digital transactions — this is not always an error.
- Clean data types before building relationships (especially `amount_egp` and `date`).
- Both fact tables share `dim_date`, `dim_branch`, and `dim_customer` — connect each separately.
"""

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print("=" * 55)
    print("Banque du Caire — Dataset Generator")
    print("=" * 55)
    make_dirs()

    print("\n[1/5] Generating dimension tables...")
    dim_date     = gen_dim_date()
    dim_branch   = gen_dim_branch()
    dim_customer = gen_dim_customer(n=200)
    dim_channel  = gen_dim_channel()
    dim_product  = gen_dim_product()

    print("\n[2/5] Generating fact tables...")
    fact_txn   = gen_fact_transactions(dim_date, dim_branch, dim_customer, dim_channel)
    fact_loans = gen_fact_loans(dim_date, dim_customer, dim_branch)

    print("\n[3/5] Injecting cleaning issues...")
    fact_txn, fact_loans, dim_customer, dim_branch = inject_issues(
        fact_txn, fact_loans, dim_customer, dim_branch
    )

    print("\n[4/5] Saving files...")
    save(dim_date,     f"{STUDENT_DIR}/dim_date.csv")
    save(dim_branch,   f"{STUDENT_DIR}/dim_branch.csv")
    save(dim_customer, f"{STUDENT_DIR}/dim_customer.csv")
    save(dim_channel,  f"{STUDENT_DIR}/dim_channel.csv")
    save(dim_product,  f"{STUDENT_DIR}/dim_product.csv")
    save(fact_txn,     f"{STUDENT_DIR}/fact_transactions.csv")
    save(fact_loans,   f"{STUDENT_DIR}/fact_loans.csv")

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
    validate(fact_txn, fact_loans, dim_date, dim_branch, dim_customer, dim_channel, dim_product)

    print("\n" + "=" * 55)
    print("Done. Output folder: output/banque_du_caire/")
    print("  student_dataset/          → share with students")
    print("  data_dictionary.md        → share with students")
    print("  private_instructor_notes/ → instructor only")
    print("=" * 55)

if __name__ == "__main__":
    main()

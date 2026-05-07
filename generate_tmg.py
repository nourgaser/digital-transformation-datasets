"""
Talaat Moustafa Group (TMG) — Egyptian Real Estate Developer
Dataset Generator for Digital Transformation Course - BINF 402, Spring 2026
GIU - Dr. Nourhan Hamdi
Team: Judi Walaa, Habiba Mostafa, Omar Ahmed Abdelaziz, Ali Ahmed Kawas, Omar Ehab

Notes:
- PD1 emphasizes TMG's integrated cities (Madinaty, Al Rehab, Noor City),
  hospitality (Four Seasons), TMG Life app for residents, and IoT/smart-city tech.
- Dashboard KPIs were not specified by the team, so the dataset covers two areas:
  (1) Unit sales — core property revenue
  (2) Community services — TMG Life app activity (utility payments, maintenance,
      QR security, club bookings) — reflects TMG's digital transformation story.
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

PROJECT_SLUG = "tmg"
OUTPUT_BASE  = f"output/{PROJECT_SLUG}"
STUDENT_DIR  = f"{OUTPUT_BASE}/student_dataset"
PRIVATE_DIR  = f"{OUTPUT_BASE}/private_instructor_notes"

DATE_START = date(2023, 1, 1)
DATE_END   = date(2024, 12, 31)
TARGET_SALES_ROWS    = 2000
TARGET_SERVICE_ROWS  = 800

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
            "date":        d.strftime("%Y-%m-%d"),   # text — cleaning task
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
    # (id, name, location, area, type, launch_year, total_units, status)
    ("PJ01", "Madinaty",            "East Cairo",  "New Cairo",        "Integrated City", 2006, 4500, "Delivered+Ongoing"),
    ("PJ02", "Al Rehab",            "East Cairo",  "New Cairo",        "Integrated City", 1997, 2800, "Delivered"),
    ("PJ03", "Celia",               "East Cairo",  "New Capital",      "Residential",     2020, 1500, "Under Construction"),
    ("PJ04", "Privado",             "East Cairo",  "Madinaty",         "Residential",     2018,  800, "Delivered+Ongoing"),
    ("PJ05", "Mayfair",             "East Cairo",  "Madinaty",         "Residential",     2019,  600, "Delivered+Ongoing"),
    ("PJ06", "Noor City",           "East Cairo",  "New Capital Axis", "Smart City",      2022, 3000, "Early Stage"),
    ("PJ07", "The Spine",           "East Cairo",  "New Cairo",        "Commercial",      2024,  400, "Early Stage"),
    ("PJ08", "Four Seasons Cairo",  "Greater Cairo","Garden City",     "Hospitality",     2002,  100, "Delivered"),
    ("PJ09", "Four Seasons Alex",   "Alexandria",  "San Stefano",      "Hospitality",     2007,  120, "Delivered"),
    ("PJ10", "Four Seasons Sharm",  "South Sinai", "Sharm El Sheikh",  "Hospitality",     2002,  140, "Delivered"),
]

def gen_dim_project():
    rows = [{
        "project_id":     p[0],
        "project_name":   p[1],
        "location":       p[2],
        "sub_area":       p[3],
        "project_type":   p[4],
        "launch_year":    p[5],
        "total_units":    p[6],
        "delivery_status":p[7],
    } for p in PROJECTS_RAW]
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# DIM UNIT TYPE
# ─────────────────────────────────────────────
UNIT_TYPES_RAW = [
    # (id, type, min_sqm, max_sqm, bedrooms, base_price_per_sqm)
    ("UT01", "Studio",       40,   65,  0, 30000),
    ("UT02", "Apartment 1BR",70,  100,  1, 28000),
    ("UT03", "Apartment 2BR",115, 170,  2, 26000),
    ("UT04", "Apartment 3BR",170, 250,  3, 25000),
    ("UT05", "Penthouse",    200, 380,  4, 33000),
    ("UT06", "Twin House",   240, 360,  4, 22000),
    ("UT07", "Villa",        320, 600,  5, 20000),
    ("UT08", "Hotel Suite",   45,  90,  1, 45000),   # for hospitality projects
]

def gen_dim_unit_type():
    rows = [{
        "unit_type_id":       u[0],
        "unit_type":          u[1],
        "min_area_sqm":       u[2],
        "max_area_sqm":       u[3],
        "bedrooms":           u[4],
        "base_price_per_sqm": u[5],
    } for u in UNIT_TYPES_RAW]
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# DIM CHANNEL
# ─────────────────────────────────────────────
CHANNELS = [
    ("CH01", "TMG Sales Center", "Direct"),
    ("CH02", "Broker",           "Indirect"),
    ("CH03", "TMG Website",      "Digital"),
    ("CH04", "TMG Life App",     "Digital"),
    ("CH05", "Referral",         "Indirect"),
]

def gen_dim_channel():
    rows = [{"channel_id": c[0], "channel_name": c[1], "channel_type": c[2]}
            for c in CHANNELS]
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# DIM CUSTOMER
# ─────────────────────────────────────────────
BUYER_TYPES   = ["Egyptian Local", "Egyptian Diaspora", "Arab Investor", "Foreign Investor"]
BUYER_WEIGHTS = [60, 22, 12, 6]

def gen_dim_customer(n=180):
    rng  = np.random.default_rng(SEED + 5)
    rows = []
    gov_pool = ["Cairo", "Giza", "Alexandria", "Overseas", "Gulf", "UAE", "KSA", "UK", "USA"]
    gov_wts  = [35, 22, 8, 8, 8, 7, 6, 4, 2]

    for i in range(1, n + 1):
        btype = random.choices(BUYER_TYPES, weights=BUYER_WEIGHTS)[0]
        if btype == "Foreign Investor":
            name = fake_en.name()
            gov  = random.choice(["UK","USA","Germany","Canada"])
        elif btype == "Arab Investor":
            name = fake_en.name()
            gov  = random.choice(["UAE","KSA","Kuwait","Qatar"])
        else:
            name = fake_en.name()
            gov  = random.choices(gov_pool, weights=gov_wts)[0]

        rows.append({
            "customer_id":      f"CUS{i:04d}",
            "customer_name":    name,
            "buyer_type":       btype,
            "nationality":      "Egyptian" if "Egyptian" in btype else
                                ("Arab" if btype == "Arab Investor" else "Foreign"),
            "governorate":      gov,
            "age":              int(rng.integers(28, 65)),
            "gender":           random.choice(["Male","Female"]),
            "is_resident":      random.choices([True, False], weights=[55, 45])[0],
            "tmg_life_user":    random.choices([True, False], weights=[70, 30])[0],
            "registered_year":  int(rng.integers(2010, 2025)),
        })
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# DIM SERVICE TYPE (for fact_community_services)
# ─────────────────────────────────────────────
SERVICE_TYPES = [
    # (id, name, category, avg_amount_egp, has_payment)
    ("ST01", "Electricity Payment",  "Utility",     650,  True),
    ("ST02", "Water Payment",        "Utility",     200,  True),
    ("ST03", "Internet Payment",     "Utility",     450,  True),
    ("ST04", "Gas Payment",          "Utility",     180,  True),
    ("ST05", "Maintenance Request",  "Maintenance",  0,   False),
    ("ST06", "Security QR Access",   "Security",     0,   False),
    ("ST07", "Club Booking",         "Recreation",  300,  True),
    ("ST08", "Gym Membership",       "Recreation", 1200,  True),
    ("ST09", "Concierge Request",    "Concierge",   0,   False),
    ("ST10", "Internal Transport",   "Transport",   100,  True),
]

def gen_dim_service_type():
    rows = [{
        "service_type_id":  s[0],
        "service_name":     s[1],
        "service_category": s[2],
        "avg_amount_egp":   s[3],
        "is_payment":       s[4],
    } for s in SERVICE_TYPES]
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# FACT UNIT SALES
# ─────────────────────────────────────────────

# Project × unit type compatibility
PROJ_UNIT_COMPAT = {
    "PJ01": ["UT02","UT03","UT04","UT05","UT06","UT07"],   # Madinaty — full mix
    "PJ02": ["UT02","UT03","UT04","UT05","UT07"],          # Al Rehab — apartments + villas
    "PJ03": ["UT02","UT03","UT04","UT05"],                 # Celia — apartments
    "PJ04": ["UT04","UT05","UT06","UT07"],                 # Privado — premium
    "PJ05": ["UT03","UT04","UT05"],                        # Mayfair — apartments
    "PJ06": ["UT01","UT02","UT03","UT04","UT05"],          # Noor City — smart city, all sizes
    "PJ07": ["UT01"],                                      # The Spine — commercial only
    "PJ08": ["UT08"],                                      # Four Seasons Cairo
    "PJ09": ["UT08"],                                      # Four Seasons Alex
    "PJ10": ["UT08"],                                      # Four Seasons Sharm
}

PROJ_WEIGHT = {
    "PJ01":18,"PJ02":10,"PJ03":8,"PJ04":7,"PJ05":5,
    "PJ06":12,"PJ07":3,"PJ08":4,"PJ09":3,"PJ10":4,
}

def channel_weights(year):
    if year == 2023:
        return {"CH01":0.40,"CH02":0.30,"CH03":0.10,"CH04":0.10,"CH05":0.10}
    else:  # 2024 — TMG Life app and website grow
        return {"CH01":0.35,"CH02":0.25,"CH03":0.15,"CH04":0.18,"CH05":0.07}

def sales_seasonality(month):
    return {1:0.95, 2:0.9, 3:1.05, 4:1.0, 5:1.0, 6:0.95,
            7:1.05, 8:1.1, 9:1.0, 10:1.1, 11:1.2, 12:1.3}.get(month, 1.0)

UNIT_TYPE_LOOKUP = {u[0]: u for u in UNIT_TYPES_RAW}

CONTRACT_STATUSES = ["Signed", "Under Review", "Cancelled"]
CONTRACT_WEIGHTS  = [87, 8, 5]

PAYMENT_PLANS = ["Off-Plan 8-Year", "Off-Plan 10-Year", "5-Year Installment", "Cash"]
PAYMENT_WEIGHTS = [35, 30, 25, 10]

def gen_fact_unit_sales(dim_date, dim_project, dim_unit_type, dim_customer, dim_channel):
    rng       = np.random.default_rng(SEED + 20)
    proj_ids  = [p[0] for p in PROJECTS_RAW]
    proj_wts  = [PROJ_WEIGHT[p] for p in proj_ids]
    ch_ids    = [c[0] for c in CHANNELS]
    cust_ids  = dim_customer["customer_id"].tolist()
    is_inv_map = {cid: dim_customer[dim_customer["customer_id"] == cid]["buyer_type"].iloc[0]
                  for cid in cust_ids}

    rows    = []
    sale_id = 1

    for _ in range(TARGET_SALES_ROWS):
        proj_id      = random.choices(proj_ids, weights=proj_wts)[0]
        compat       = PROJ_UNIT_COMPAT[proj_id]
        unit_type_id = random.choice(compat)
        ut           = UNIT_TYPE_LOOKUP[unit_type_id]
        min_sqm, max_sqm, base_psm = ut[2], ut[3], ut[5]

        # Date with seasonality
        date_row = dim_date.sample(1,
            weights=dim_date["month"].map(sales_seasonality)).iloc[0]
        date_id  = date_row["date_id"]
        year     = date_row["year"]
        month    = date_row["month"]

        area_sqm = round(rng.uniform(min_sqm, max_sqm), 1)

        # Project premium reflects positioning
        proj_premium = {
            "PJ01":1.10,"PJ02":1.00,"PJ03":1.15,"PJ04":1.25,"PJ05":1.20,
            "PJ06":1.30,"PJ07":1.40,"PJ08":1.80,"PJ09":1.60,"PJ10":1.70,
        }[proj_id]
        # 2024 price increase due to EGP devaluation
        year_factor  = 1.0 if year == 2023 else 1.18
        psm_actual   = round(base_psm * proj_premium * year_factor * rng.uniform(0.95, 1.05))
        contract_val = round(psm_actual * area_sqm, -3)

        # Down payment + plan
        dp_pct = random.choice([10, 15, 20, 25, 30, 100])
        if dp_pct == 100:
            payment_plan = "Cash"
        else:
            payment_plan = random.choices(
                ["Off-Plan 8-Year", "Off-Plan 10-Year", "5-Year Installment"],
                weights=[40, 35, 25]
            )[0]

        down_payment = round(contract_val * dp_pct / 100, -3)
        remaining    = contract_val - down_payment

        channel_id = random.choices(ch_ids,
                                    weights=list(channel_weights(year).values()))[0]

        commission_pct = 0.0
        if channel_id == "CH02":      # Broker
            commission_pct = round(rng.uniform(0.02, 0.04), 3)
        elif channel_id == "CH05":    # Referral
            commission_pct = round(rng.uniform(0.005, 0.015), 3)
        commission_amt = round(contract_val * commission_pct, -2)

        customer_id = rng.choice(cust_ids)
        contract_status = random.choices(CONTRACT_STATUSES, weights=CONTRACT_WEIGHTS)[0]
        if contract_status == "Cancelled":
            contract_val   = 0
            down_payment   = 0
            commission_amt = 0
            remaining      = 0

        is_off_plan = "Off-Plan" in payment_plan

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
            "is_off_plan":      is_off_plan,
            "commission_pct":   commission_pct,
            "commission_amount":commission_amt,
            "contract_status":  contract_status,
        })
        sale_id += 1

    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# FACT COMMUNITY SERVICES (TMG Life app activity)
# ─────────────────────────────────────────────

# Only resident projects support community services (skip hospitality + commercial)
RESIDENT_PROJECTS = ["PJ01","PJ02","PJ03","PJ04","PJ05","PJ06"]

def gen_fact_community_services(dim_date, dim_project, dim_customer, dim_service_type):
    rng = np.random.default_rng(SEED + 30)

    # Filter to residents and TMG Life users
    residents = dim_customer[
        (dim_customer["is_resident"] == True) &
        (dim_customer["tmg_life_user"] == True)
    ]["customer_id"].tolist()
    if len(residents) == 0:
        residents = dim_customer["customer_id"].tolist()[:50]

    service_ids = [s[0] for s in SERVICE_TYPES]
    service_wts = [25, 15, 18, 12, 10, 20, 8, 4, 6, 5]   # utilities most frequent
    service_lookup = {s[0]: s for s in SERVICE_TYPES}

    rows  = []
    sv_id = 1

    for _ in range(TARGET_SERVICE_ROWS):
        # Date — uniform but slightly higher in summer (utilities peak)
        month_wts = {1:0.9,2:0.85,3:1.0,4:1.0,5:1.1,6:1.3,
                     7:1.4,8:1.4,9:1.1,10:1.0,11:0.95,12:1.0}
        date_row = dim_date.sample(1,
            weights=dim_date["month"].map(month_wts)).iloc[0]
        date_id  = date_row["date_id"]

        customer_id = rng.choice(residents)
        proj_id     = random.choice(RESIDENT_PROJECTS)
        service_id  = random.choices(service_ids, weights=service_wts)[0]
        sv          = service_lookup[service_id]
        sv_name, sv_cat, avg_amt, is_pay = sv[1], sv[2], sv[3], sv[4]

        # Amount: vary around average for paid services; 0 for non-payment
        if is_pay:
            amount = round(avg_amt * rng.uniform(0.7, 1.4), 2)
        else:
            amount = 0.0

        # Status
        status = random.choices(
            ["Completed", "Pending", "Cancelled", "Failed"],
            weights=[85, 8, 4, 3]
        )[0]
        if status in ("Cancelled", "Failed"):
            amount = 0.0

        # Service rating (1-5) — only for completed
        rating = int(rng.integers(3, 6)) if status == "Completed" else None

        # Resolution time for non-payment requests (in hours)
        if sv_cat in ("Maintenance", "Concierge", "Security"):
            resolution_hrs = int(rng.integers(1, 72)) if status == "Completed" else None
        else:
            resolution_hrs = None

        rows.append({
            "service_log_id":   f"SVL{sv_id:05d}",
            "date_id":          date_id,
            "customer_id":      customer_id,
            "project_id":       proj_id,
            "service_type_id":  service_id,
            "amount_paid_egp":  amount,
            "service_status":   status,
            "rating":           rating,
            "resolution_hours": resolution_hrs,
            "via_app":          True,
        })
        sv_id += 1

    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# INJECT CLEANING ISSUES
# ─────────────────────────────────────────────
def inject_issues(df_sales, df_services, df_customer, df_project, df_unit_type):
    n   = len(df_sales)
    ns  = len(df_services)
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
    df_sales.loc[idx3, "contract_status"] = df_sales.loc[idx3, "contract_status"].str.lower()

    # 4. contract_value stored as string in ~3% of rows
    df_sales["contract_value"] = df_sales["contract_value"].astype(object)
    idx4 = rng.choice(n, size=int(n * 0.03), replace=False)
    for i in idx4:
        df_sales.at[i, "contract_value"] = str(df_sales.at[i, "contract_value"])

    # 5. Negative impossible values — 3 rows
    bad = rng.choice(n, size=3, replace=False)
    for i in bad:
        df_sales.at[i, "contract_value"] = -abs(float(df_sales.at[i, "contract_value"]))

    # 6. Trailing whitespace in payment_plan (~2%)
    idx6 = rng.choice(n, size=int(n * 0.02), replace=False)
    df_sales.loc[idx6, "payment_plan"] = df_sales.loc[idx6, "payment_plan"] + " "

    # 7. Duplicate rows (~1.5%)
    dup_idx = rng.choice(n, size=int(n * 0.015), replace=False)
    dups    = df_sales.iloc[dup_idx].copy()
    df_sales = pd.concat([df_sales, dups], ignore_index=True)

    # ── fact_community_services ───────────────
    # 8. ~5% nulls in rating
    idx8 = rng.choice(ns, size=int(ns * 0.05), replace=False)
    df_services.loc[idx8, "rating"] = np.nan

    # 9. Inconsistent casing in service_status (~3%)
    idx9 = rng.choice(ns, size=int(ns * 0.03), replace=False)
    df_services.loc[idx9, "service_status"] = df_services.loc[idx9, "service_status"].str.upper()

    # 10. Impossible negative resolution_hours — 3 rows
    valid_idx = df_services[df_services["resolution_hours"].notna()].index
    if len(valid_idx) >= 3:
        bad_res = rng.choice(valid_idx, size=3, replace=False)
        df_services.loc[bad_res, "resolution_hours"] = -rng.integers(1, 10, size=3).astype(float)

    # ── dim_customer ───────────────────────────
    # 11. Inconsistent buyer_type casing for 4 rows
    s_idx = df_customer.sample(4, random_state=SEED).index
    df_customer.loc[s_idx, "buyer_type"] = df_customer.loc[s_idx, "buyer_type"].str.lower()

    # ── dim_project ────────────────────────────
    # 12. Trailing whitespace in project_type for 3 hospitality rows
    df_project.loc[df_project["project_id"].isin(["PJ08","PJ09","PJ10"]), "project_type"] = "Hospitality "

    # ── dim_unit_type ──────────────────────────
    # 13. Lowercase unit_type for 2 rows
    df_unit_type.loc[df_unit_type["unit_type_id"].isin(["UT06","UT07"]), "unit_type"] = \
        df_unit_type.loc[df_unit_type["unit_type_id"].isin(["UT06","UT07"]), "unit_type"].str.lower()

    return df_sales, df_services, df_customer, df_project, df_unit_type

# ─────────────────────────────────────────────
# VALIDATION
# ─────────────────────────────────────────────
def validate(df_sales, df_services, dim_date, dim_project, dim_unit_type,
             dim_customer, dim_channel, dim_service_type):
    print("\nValidation:")
    valid_dates    = set(dim_date["date_id"])
    valid_proj     = set(dim_project["project_id"])
    valid_ut       = set(dim_unit_type["unit_type_id"])
    valid_cust     = set(dim_customer["customer_id"])
    valid_ch       = set(dim_channel["channel_id"])
    valid_st       = set(dim_service_type["service_type_id"])

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
        ("date_id",         valid_dates, "service date_id"),
        ("project_id",      valid_proj,  "service project_id"),
        ("customer_id",     valid_cust,  "service customer_id"),
        ("service_type_id", valid_st,    "service service_type_id"),
    ]:
        bad = df_services[~df_services[col].isin(valid)]
        if len(bad): errors.append(f"  FK issue ({lbl}): {len(bad)} rows")

    for e in errors: print(e)
    if not errors: print("  FK checks passed.")

    dups = df_sales.duplicated().sum()
    str_cv = (df_sales["contract_value"].apply(lambda x: isinstance(x, str))).mean()
    print(f"  fact_unit_sales rows (incl. dupes): {len(df_sales)}")
    print(f"  Duplicate rows:                     {dups}")
    print(f"  Null rate commission_pct:           {df_sales['commission_pct'].isna().mean():.1%}")
    print(f"  contract_value as string:           {str_cv:.1%}")
    print(f"  fact_community_services rows:       {len(df_services)}")
    print(f"  Null rate rating:                   {df_services['rating'].isna().mean():.1%}")

# ─────────────────────────────────────────────
# INSTRUCTOR NOTES
# ─────────────────────────────────────────────
CLEANING_MD = """\
# Expected Cleaning Tasks — TMG (Talaat Moustafa Group)

## fact_unit_sales.csv

| # | Issue | Column | Approx. Rate |
|---|-------|--------|--------------|
| 1 | Missing values | `commission_pct` | ~5% nulls |
| 2 | Missing values | `down_payment_pct` | ~4% nulls |
| 3 | Inconsistent casing | `contract_status` | ~3% lowercase ("signed", "cancelled") |
| 4 | Mixed data type | `contract_value` | ~3% stored as text strings |
| 5 | Impossible negative values | `contract_value` | 3 rows with negative values |
| 6 | Trailing whitespace | `payment_plan` | ~2% with trailing space |
| 7 | Duplicate rows | all columns | ~1.5% fully duplicated records |

## fact_community_services.csv

| # | Issue | Column | Approx. Rate |
|---|-------|--------|--------------|
| 8 | Missing values | `rating` | ~5% nulls (in addition to the natural nulls for non-completed services) |
| 9 | Inconsistent casing | `service_status` | ~3% uppercase ("COMPLETED", "PENDING") |
| 10 | Impossible negative values | `resolution_hours` | 3 rows with negative values |

## dim_customer.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 11 | Inconsistent casing | `buyer_type` | 4 rows lowercase ("egyptian local") |

## dim_project.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 12 | Trailing whitespace | `project_type` | "Hospitality " (trailing space) for PJ08, PJ09, PJ10 |

## dim_unit_type.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 13 | Inconsistent casing | `unit_type` | "twin house", "villa" (lowercase) for UT06, UT07 |

## dim_date.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 14 | Date stored as string | `date` | Text "YYYY-MM-DD" — must be converted to Date type in Power Query |

## Notes for Instructor
- The `payment_plan` trailing whitespace splits "Off-Plan 8-Year" and "Off-Plan 8-Year " into two groups in charts — a realistic, subtle data quality lesson.
- `rating` has a natural null pattern (only completed services have ratings) — students must NOT treat all nulls as errors. The instructor should highlight the difference between expected and injected nulls.
- TMG's "Off-Plan" financing is a key differentiator — the `is_off_plan` column lets students measure its share of revenue, which the PD1 explicitly mentions as a strategic gain.
"""

DAX_MD = """\
# Suggested DAX Measures — TMG

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

Off-Plan Sales % =
    DIVIDE(
        CALCULATE([Total Contract Value], fact_unit_sales[is_off_plan] = TRUE()),
        [Total Contract Value]
    )

Total Down Payments Collected =
    CALCULATE(
        SUM(fact_unit_sales[down_payment]),
        fact_unit_sales[contract_status] = "Signed"
    )
```

## Channel Performance
```dax
Digital Channel Revenue =
    CALCULATE([Total Contract Value],
        RELATED(dim_channel[channel_type]) = "Digital"
    )

Direct Sales Revenue =
    CALCULATE([Total Contract Value],
        RELATED(dim_channel[channel_type]) = "Direct"
    )

Digital Sales % =
    DIVIDE([Digital Channel Revenue], [Total Contract Value])
```

## Community Services (TMG Life App)
```dax
Total Service Activities =
    COUNTROWS(fact_community_services)

Total Service Revenue =
    SUM(fact_community_services[amount_paid_egp])

Avg Service Rating =
    CALCULATE(
        AVERAGE(fact_community_services[rating]),
        fact_community_services[service_status] = "Completed"
    )

Avg Resolution Hours =
    CALCULATE(
        AVERAGE(fact_community_services[resolution_hours]),
        fact_community_services[resolution_hours] > 0
    )

Service Completion Rate =
    DIVIDE(
        CALCULATE(COUNTROWS(fact_community_services),
                  fact_community_services[service_status] = "Completed"),
        [Total Service Activities]
    )

Active App Users =
    DISTINCTCOUNT(fact_community_services[customer_id])
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

Diaspora Buyers % =
    DIVIDE(
        CALCULATE(DISTINCTCOUNT(fact_unit_sales[customer_id]),
            RELATED(dim_customer[buyer_type]) = "Egyptian Diaspora"),
        [Total Buyers]
    )

Foreign + Arab Investor % =
    DIVIDE(
        CALCULATE(DISTINCTCOUNT(fact_unit_sales[customer_id]),
            RELATED(dim_customer[buyer_type]) IN { "Arab Investor", "Foreign Investor" }),
        [Total Buyers]
    )
```
"""

DASHBOARD_MD = """\
# Dashboard Questions & Visual Suggestions — TMG

## Analytical Questions (student-facing prompts)
1. Which TMG projects generate the highest total contract value (Madinaty, Al Rehab, Noor City, others)?
2. How does Off-Plan financing contribute to total revenue, and how does it compare to cash + standard installments?
3. Which unit types drive the most revenue and volume across the portfolio?
4. How does sales volume change month-over-month and year-over-year?
5. How does the channel mix differ between 2023 and 2024 — is the TMG Life app gaining share?
6. What is the average price per sqm by project, and how has it changed from 2023 to 2024 (EGP devaluation impact)?
7. What share of buyers are Egyptian Diaspora or foreign investors?
8. How active are residents on the TMG Life app? Which service categories are most used?
9. What is the average service resolution time, and which service categories take longest?
10. What is the average customer rating for completed services?
11. Which projects have the highest community service activity (a proxy for resident engagement)?
12. What is the cancellation rate by project and channel?

## Suggested Visuals (instructor only)

| Visual | Type | Fields |
|--------|------|--------|
| Total Contract Value KPI | Card | [Total Contract Value] |
| Total Units Sold KPI | Card | [Total Units Sold] |
| Off-Plan Sales % KPI | Card | [Off-Plan Sales %] |
| Avg Service Rating KPI | Card | [Avg Service Rating] |
| Sales by Project | Bar | dim_project[project_name], [Total Contract Value] |
| Sales by Unit Type | Bar/Donut | dim_unit_type[unit_type], [Total Units Sold] |
| Contract Value over Time | Line | dim_date[month_name], [Total Contract Value] |
| YoY Comparison | Line (dual) | dim_date[month], current vs prior year |
| Channel Mix 2023 vs 2024 | Clustered bar | dim_channel[channel_name], year slicer |
| Sales by Buyer Type | Donut | dim_customer[buyer_type], [Total Contract Value] |
| Off-Plan vs Cash | Stacked bar | fact[is_off_plan], [Total Contract Value] |
| Service Activity by Category | Bar | dim_service_type[service_category], count |
| Service Status Breakdown | Donut | fact_community_services[service_status] |
| Avg Resolution Hours by Category | Bar | dim_service_type[service_category], [Avg Resolution Hours] |
| Service Activity by Project | Bar | dim_project[project_name], [Total Service Activities] |
| Payment Plan Distribution | Pie | fact_unit_sales[payment_plan], count |
| Cancellation Rate by Project | Bar | dim_project[project_name], [Cancellation Rate] |

## Suggested Slicers
- Year / Quarter / Month
- Project Name / Project Type
- Unit Type
- Sales Channel / Channel Type
- Buyer Type
- Service Category
- Contract Status
"""

MODEL_MD = """\
# Star Schema Relationships — TMG

## Tables
- **fact_unit_sales** — main fact: property unit contracts (~2,000+ rows)
- **fact_community_services** — secondary fact: TMG Life app activity (~800 rows)
- **dim_date** — date dimension (shared)
- **dim_project** — project/community dimension (shared)
- **dim_unit_type** — unit type dimension (sales only)
- **dim_customer** — customer dimension (shared)
- **dim_channel** — sales channel dimension (sales only)
- **dim_service_type** — service category dimension (services only)

## Relationships

### fact_unit_sales
| Fact Column | → | Dimension | PK | Cardinality | Filter |
|-------------|---|-----------|----|-------------|--------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single |
| `project_id` | → | `dim_project` | `project_id` | Many-to-One | Single |
| `unit_type_id` | → | `dim_unit_type` | `unit_type_id` | Many-to-One | Single |
| `customer_id` | → | `dim_customer` | `customer_id` | Many-to-One | Single |
| `channel_id` | → | `dim_channel` | `channel_id` | Many-to-One | Single |

### fact_community_services
| Fact Column | → | Dimension | PK | Cardinality | Filter |
|-------------|---|-----------|----|-------------|--------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single |
| `customer_id` | → | `dim_customer` | `customer_id` | Many-to-One | Single |
| `project_id` | → | `dim_project` | `project_id` | Many-to-One | Single |
| `service_type_id` | → | `dim_service_type` | `service_type_id` | Many-to-One | Single |

## Notes
- Both fact tables share `dim_date`, `dim_project`, and `dim_customer` — connect each separately, do NOT create cross-fact relationships.
- `dim_unit_type` and `dim_channel` connect only to `fact_unit_sales`.
- `dim_service_type` connects only to `fact_community_services`.
- Mark `dim_date[date]` as a **Date Table** after converting from string to Date type.
- `contract_value` must be a numeric type (Decimal Number) before any SUM measure will work.
- Filter direction should be **single** (dimension → fact) for all relationships.
"""

DATA_DICT_MD = """\
# Data Dictionary — Talaat Moustafa Group (TMG)
## Digital Transformation Course · BINF 402 · GIU · Spring 2026

---

## Business Story
Talaat Moustafa Group (TMG) is one of Egypt's largest real estate developers, known for integrated cities like **Madinaty**, **Al Rehab**, and the upcoming **Noor City**. Beyond property sales, TMG operates Four Seasons hotels and runs **TMG Life**, a mobile app that handles community services for over a million residents — utility payments, maintenance, security access, and recreation bookings.

This dataset covers two areas for 2023–2024:
1. **Property unit sales** — contracts across TMG's projects
2. **Community service activity** — residents' use of the TMG Life app

Your goal as management is to track sales performance across projects, monitor the shift to digital channels, measure off-plan financing impact, and evaluate resident engagement and satisfaction with community services.

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
| `down_payment` | Initial down payment (EGP) |
| `remaining_balance` | Remaining installment balance (EGP) |
| `down_payment_pct` | Down payment as % of contract value |
| `payment_plan` | Off-Plan 8-Year, Off-Plan 10-Year, 5-Year Installment, or Cash |
| `is_off_plan` | True if contract uses off-plan financing |
| `commission_pct` | Broker/referral commission rate |
| `commission_amount` | Total commission paid (EGP) |
| `contract_status` | Signed, Under Review, or Cancelled |

### `fact_community_services.csv` (secondary fact table)
| Column | Description |
|--------|-------------|
| `service_log_id` | Unique service activity identifier |
| `date_id` | Foreign key → `dim_date.date_id` |
| `customer_id` | Foreign key → `dim_customer.customer_id` |
| `project_id` | Foreign key → `dim_project.project_id` |
| `service_type_id` | Foreign key → `dim_service_type.service_type_id` |
| `amount_paid_egp` | Amount paid via the app (EGP); 0 for non-payment services |
| `service_status` | Completed, Pending, Cancelled, or Failed |
| `rating` | Customer rating (1–5); only for completed services |
| `resolution_hours` | Hours to resolve the request (Maintenance, Concierge, Security only) |
| `via_app` | Always True — this fact tracks app activity |

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
| `project_name` | Project name (Madinaty, Al Rehab, Noor City, Four Seasons hotels, etc.) |
| `location` | Greater Cairo, East Cairo, Alexandria, South Sinai |
| `sub_area` | Specific sub-area |
| `project_type` | Integrated City, Residential, Smart City, Commercial, Hospitality |
| `launch_year` | Year project was launched |
| `total_units` | Total number of units |
| `delivery_status` | Delivered, Delivered+Ongoing, Under Construction, Early Stage |

### `dim_unit_type.csv`
| Column | Description |
|--------|-------------|
| `unit_type_id` | Primary key |
| `unit_type` | Studio, Apartment 1BR/2BR/3BR, Penthouse, Twin House, Villa, Hotel Suite |
| `min_area_sqm` / `max_area_sqm` | Size range |
| `bedrooms` | Number of bedrooms |
| `base_price_per_sqm` | Reference base price (EGP) |

### `dim_customer.csv`
| Column | Description |
|--------|-------------|
| `customer_id` | Primary key |
| `customer_name` | Synthetic buyer name |
| `buyer_type` | Egyptian Local, Egyptian Diaspora, Arab Investor, Foreign Investor |
| `nationality` | Nationality category |
| `governorate` | Buyer's location (or country if abroad) |
| `age` | Age |
| `gender` | Gender |
| `is_resident` | True if buyer lives in a TMG community |
| `tmg_life_user` | True if user is registered on the TMG Life app |
| `registered_year` | Year customer registered |

### `dim_channel.csv`
| Column | Description |
|--------|-------------|
| `channel_id` | Primary key |
| `channel_name` | TMG Sales Center, Broker, TMG Website, TMG Life App, Referral |
| `channel_type` | Direct, Indirect, or Digital |

### `dim_service_type.csv`
| Column | Description |
|--------|-------------|
| `service_type_id` | Primary key |
| `service_name` | Specific service (Electricity Payment, Maintenance Request, etc.) |
| `service_category` | Utility, Maintenance, Security, Recreation, Concierge, Transport |
| `avg_amount_egp` | Reference average amount for paid services |
| `is_payment` | True if service involves a payment |

---

## Intended Relationships
- `fact_unit_sales` → `dim_date`, `dim_project`, `dim_unit_type`, `dim_customer`, `dim_channel`
- `fact_community_services` → `dim_date`, `dim_customer`, `dim_project`, `dim_service_type`

## Notes for Students
- Clean data types and fix inconsistencies **before** building relationships in Power BI.
- TMG's **Off-Plan financing** is a strategic differentiator — use the `is_off_plan` column to measure its share of revenue.
- The **TMG Life app** activity (fact_community_services) reflects resident engagement — this is a unique TMG digital transformation outcome.
- 2024 prices are higher than 2023 due to EGP devaluation — surface this in average price/sqm comparisons.
- The two fact tables share dimensions but are not directly connected — use shared dimensions for cross-table analysis.
"""

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print("=" * 55)
    print("Talaat Moustafa Group (TMG) — Dataset Generator")
    print("=" * 55)
    make_dirs()

    print("\n[1/5] Generating dimension tables...")
    dim_date         = gen_dim_date()
    dim_project      = gen_dim_project()
    dim_unit_type    = gen_dim_unit_type()
    dim_channel      = gen_dim_channel()
    dim_customer     = gen_dim_customer(n=180)
    dim_service_type = gen_dim_service_type()

    print("\n[2/5] Generating fact tables...")
    fact_sales    = gen_fact_unit_sales(dim_date, dim_project, dim_unit_type,
                                        dim_customer, dim_channel)
    fact_services = gen_fact_community_services(dim_date, dim_project, dim_customer,
                                                 dim_service_type)

    print("\n[3/5] Injecting cleaning issues...")
    fact_sales, fact_services, dim_customer, dim_project, dim_unit_type = inject_issues(
        fact_sales, fact_services, dim_customer, dim_project, dim_unit_type
    )

    print("\n[4/5] Saving files...")
    save(dim_date,         f"{STUDENT_DIR}/dim_date.csv")
    save(dim_project,      f"{STUDENT_DIR}/dim_project.csv")
    save(dim_unit_type,    f"{STUDENT_DIR}/dim_unit_type.csv")
    save(dim_channel,      f"{STUDENT_DIR}/dim_channel.csv")
    save(dim_customer,     f"{STUDENT_DIR}/dim_customer.csv")
    save(dim_service_type, f"{STUDENT_DIR}/dim_service_type.csv")
    save(fact_sales,       f"{STUDENT_DIR}/fact_unit_sales.csv")
    save(fact_services,    f"{STUDENT_DIR}/fact_community_services.csv")

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
    validate(fact_sales, fact_services, dim_date, dim_project, dim_unit_type,
             dim_customer, dim_channel, dim_service_type)

    print("\n" + "=" * 55)
    print("Done. Output folder: output/tmg/")
    print("  student_dataset/          → share with students")
    print("  data_dictionary.md        → share with students")
    print("  private_instructor_notes/ → instructor only")
    print("=" * 55)

if __name__ == "__main__":
    main()

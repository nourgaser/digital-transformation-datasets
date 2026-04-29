"""
Al-Ahram Newspapers Company
Media & Publishing, Cairo, Egypt
Dataset Generator — BINF 402, Digital Transformation, GIU, Spring 2026
Dr. Nourhan Hamdi
Team: YMahmoud et al.
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

PROJECT_SLUG = "alahram"
OUTPUT_BASE  = f"output/{PROJECT_SLUG}"
STUDENT_DIR  = f"{OUTPUT_BASE}/student_dataset"
PRIVATE_DIR  = f"{OUTPUT_BASE}/private_instructor_notes"

DATE_START = date(2019, 1, 1)
DATE_END   = date(2024, 12, 31)
TARGET_AD_ROWS      = 2000
TARGET_MONTHLY_ROWS = 72   # 6 years × 12 months

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
# DIM DATE  (2019–2024)
# ─────────────────────────────────────────────
EGYPTIAN_HOLIDAYS = set()
for _yr in range(2019, 2025):
    for _md in [(1, 7), (4, 25), (5, 1), (6, 30), (7, 23), (10, 6)]:
        EGYPTIAN_HOLIDAYS.add(date(_yr, _md[0], _md[1]))

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
# DIM PLATFORM
# ─────────────────────────────────────────────
PLATFORMS_RAW = [
    # (id, name, medium, description)
    ("PF01", "Al-Ahram Daily",      "Print",   "Flagship daily Arabic newspaper"),
    ("PF02", "Al-Ahram Weekly",     "Print",   "English weekly edition"),
    ("PF03", "Al-Masaa Evening",    "Print",   "Evening Arabic daily edition"),
    ("PF04", "ahram.org.eg",        "Digital", "Main Arabic news portal"),
    ("PF05", "Al-Ahram Mobile App", "Digital", "iOS & Android news application"),
    ("PF06", "Al-Ahram YouTube",    "Digital", "Official YouTube video channel"),
]

def gen_dim_platform():
    rows = [{
        "platform_id":   p[0],
        "platform_name": p[1],
        "medium":        p[2],
        "description":   p[3],
    } for p in PLATFORMS_RAW]
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# DIM AD FORMAT
# ─────────────────────────────────────────────
AD_FORMATS_RAW = [
    # (id, name, medium, base_rate_egp, rate_basis)
    # Print — rate per insertion (duration_days = 1)
    ("AF01", "Full Page",           "Print",   55000, "per insertion"),
    ("AF02", "Half Page",           "Print",   30000, "per insertion"),
    ("AF03", "Quarter Page",        "Print",   16000, "per insertion"),
    ("AF04", "Front Page Strip",    "Print",   78000, "per insertion"),
    ("AF05", "Classified",          "Print",     650, "per insertion"),
    # Digital — rate per day (duration_days varies)
    ("AF06", "Display Banner",      "Digital",  6500, "per day"),
    ("AF07", "Leaderboard",         "Digital",  9500, "per day"),
    ("AF08", "Video Pre-roll 15s",  "Digital",  5000, "per day"),
    ("AF09", "Video Pre-roll 30s",  "Digital",  8000, "per day"),
    ("AF10", "Sponsored Article",   "Digital", 20000, "per placement"),
    ("AF11", "Newsletter Banner",   "Digital",  5500, "per placement"),
    ("AF12", "Social Media Boost",  "Digital",  4000, "per day"),
]

# Platform → compatible ad format IDs
PLATFORM_FORMAT_COMPAT = {
    "PF01": ["AF01", "AF02", "AF03", "AF04", "AF05"],
    "PF02": ["AF01", "AF02", "AF03", "AF05"],
    "PF03": ["AF02", "AF03", "AF05"],
    "PF04": ["AF06", "AF07", "AF10", "AF11", "AF12"],
    "PF05": ["AF06", "AF10", "AF11", "AF12"],
    "PF06": ["AF08", "AF09"],
}

PLATFORM_FORMAT_WEIGHTS = {
    "PF01": [0.28, 0.33, 0.22, 0.07, 0.10],
    "PF02": [0.28, 0.38, 0.24, 0.10],
    "PF03": [0.40, 0.42, 0.18],
    "PF04": [0.25, 0.20, 0.28, 0.15, 0.12],
    "PF05": [0.38, 0.35, 0.17, 0.10],
    "PF06": [0.60, 0.40],
}

AD_FORMAT_LOOKUP = {f[0]: f for f in AD_FORMATS_RAW}
PLATFORM_MEDIUM  = {p[0]: p[2] for p in PLATFORMS_RAW}

def gen_dim_ad_format():
    rows = [{
        "format_id":    f[0],
        "format_name":  f[1],
        "medium":       f[2],
        "base_rate_egp":f[3],
        "rate_basis":   f[4],
    } for f in AD_FORMATS_RAW]
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# DIM ADVERTISER
# ─────────────────────────────────────────────
ADV_CATEGORIES = [
    ("Government",      15, "Print_Heavy"),
    ("Banking/Finance", 20, "Mixed"),
    ("Telecom",         10, "Digital_Heavy"),
    ("Real Estate",     15, "Print_Heavy"),
    ("FMCG",            15, "Mixed"),
    ("Automotive",      10, "Print_Heavy"),
    ("Healthcare",       5, "Mixed"),
    ("Education",        5, "Digital_Heavy"),
    ("Retail",           5, "Mixed"),
]

ADV_TIERS   = ["Premium", "Standard", "Budget"]
ADV_T_WGTS  = [0.20, 0.60, 0.20]

def gen_dim_advertiser():
    rows = []
    adv_id = 1
    for cat, count, pref in ADV_CATEGORIES:
        for _ in range(count):
            tier = random.choices(ADV_TIERS, weights=ADV_T_WGTS)[0]
            rows.append({
                "advertiser_id":          f"ADV{adv_id:04d}",
                "advertiser_name":        fake_en.company(),
                "advertiser_category":    cat,
                "platform_preference":    pref,
                "advertiser_tier":        tier,
            })
            adv_id += 1
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# FACT AD REVENUE
# ─────────────────────────────────────────────

# Print vs digital mix shifts year-on-year (print decline narrative)
YEAR_PRINT_FRAC = {2019: 0.68, 2020: 0.58, 2021: 0.52,
                   2022: 0.45, 2023: 0.38, 2024: 0.32}

# Within digital platforms, mobile share grows year-on-year
DIGITAL_PF_WEIGHTS = {
    2019: {"PF04": 0.70, "PF05": 0.20, "PF06": 0.10},
    2020: {"PF04": 0.65, "PF05": 0.25, "PF06": 0.10},
    2021: {"PF04": 0.62, "PF05": 0.28, "PF06": 0.10},
    2022: {"PF04": 0.58, "PF05": 0.33, "PF06": 0.09},
    2023: {"PF04": 0.55, "PF05": 0.36, "PF06": 0.09},
    2024: {"PF04": 0.52, "PF05": 0.40, "PF06": 0.08},
}

# Year price inflation on ad rates (EGP devaluation + market conditions)
YEAR_RATE_FACTOR = {
    2019: 1.00,
    2020: 0.88,   # COVID — ad market contracted
    2021: 1.10,
    2022: 1.28,
    2023: 1.62,   # major EGP devaluation
    2024: 1.95,
}

# Advertiser tier multiplier on ad rates
TIER_RATE = {"Premium": 1.40, "Standard": 1.00, "Budget": 0.70}

# Seasonality: Ramadan season (Mar–May) + Q4 peaks
def ad_seasonality(month):
    return {
        1: 1.00, 2: 0.95, 3: 1.20, 4: 1.35, 5: 1.25, 6: 0.90,
        7: 0.85, 8: 0.85, 9: 1.00, 10: 1.15, 11: 1.20, 12: 1.30,
    }.get(month, 1.0)

PRINT_PF_IDS     = ["PF01", "PF02", "PF03"]
PRINT_PF_WEIGHTS = [0.65, 0.25, 0.10]

BOOKING_STATUSES = ["Confirmed", "Under Review", "Cancelled"]
BOOKING_WEIGHTS  = [85, 9, 6]

DIGITAL_DURATION_DAYS = [7, 14, 21, 30, 60]
DIGITAL_DUR_WEIGHTS   = [0.20, 0.30, 0.20, 0.22, 0.08]

def gen_fact_ad_revenue(dim_date, dim_advertiser, dim_platform, dim_ad_format):
    rng = np.random.default_rng(SEED + 20)
    adv_ids  = dim_advertiser["advertiser_id"].tolist()
    tier_map = dim_advertiser.set_index("advertiser_id")["advertiser_tier"].to_dict()
    pref_map = dim_advertiser.set_index("advertiser_id")["platform_preference"].to_dict()

    rows    = []
    sale_id = 1

    for _ in range(TARGET_AD_ROWS):
        # Date weighted by seasonality — sample across full 6-year range
        date_df  = dim_date.copy()
        date_df["w"] = date_df["month"].map(ad_seasonality)
        date_row = date_df.sample(1, weights="w").iloc[0]
        date_id  = date_row["date_id"]
        year     = int(date_row["year"])
        month    = int(date_row["month"])

        # Print vs digital split for this year
        print_frac = YEAR_PRINT_FRAC[year]

        # Advertiser — platform preference modifies the print/digital split
        adv_id   = str(rng.choice(adv_ids))
        pref     = pref_map[adv_id]
        tier     = tier_map[adv_id]

        if pref == "Print_Heavy":
            adj_print_frac = min(0.90, print_frac + 0.15)
        elif pref == "Digital_Heavy":
            adj_print_frac = max(0.10, print_frac - 0.20)
        else:
            adj_print_frac = print_frac

        medium = "Print" if random.random() < adj_print_frac else "Digital"

        # Platform
        if medium == "Print":
            platform_id = random.choices(PRINT_PF_IDS, weights=PRINT_PF_WEIGHTS)[0]
        else:
            dpw = DIGITAL_PF_WEIGHTS[year]
            platform_id = random.choices(list(dpw.keys()), weights=list(dpw.values()))[0]

        # Ad format (compatible with platform)
        compat  = PLATFORM_FORMAT_COMPAT[platform_id]
        fwts    = PLATFORM_FORMAT_WEIGHTS[platform_id]
        fmt_id  = random.choices(compat, weights=fwts)[0]
        fmt     = AD_FORMAT_LOOKUP[fmt_id]
        base_rate = fmt[3]

        # Duration
        if medium == "Print":
            duration_days = 1
        elif platform_id == "PF06":   # YouTube
            duration_days = random.choices([7, 14, 30], weights=[0.30, 0.45, 0.25])[0]
        elif fmt_id in ("AF10", "AF11"):  # placement-based
            duration_days = 1
        else:
            duration_days = random.choices(
                DIGITAL_DURATION_DAYS, weights=DIGITAL_DUR_WEIGHTS
            )[0]

        # Revenue
        rate_factor  = YEAR_RATE_FACTOR[year] * TIER_RATE[tier] * float(rng.uniform(0.90, 1.10))
        gross_revenue = round(base_rate * duration_days * rate_factor, -2)

        # Discount
        if tier == "Premium":
            discount_pct = round(float(rng.uniform(0.05, 0.15)), 3)
        elif pref == "Government":
            discount_pct = round(float(rng.uniform(0.08, 0.20)), 3)
        else:
            discount_pct = round(float(rng.uniform(0.00, 0.08)), 3)

        net_revenue = round(gross_revenue * (1 - discount_pct), -2)

        # Digital impressions (null for print — by design)
        if medium == "Digital":
            if platform_id == "PF06":   # YouTube views
                impressions_k = round(float(rng.uniform(15, 250)), 1)
            else:
                impressions_k = round(float(rng.uniform(50, 800)), 1)
        else:
            impressions_k = None   # print has no digital impression data

        # Booking status
        booking_status = random.choices(BOOKING_STATUSES, weights=BOOKING_WEIGHTS)[0]
        if booking_status == "Cancelled":
            net_revenue   = 0
            gross_revenue = 0

        rows.append({
            "booking_id":       f"BK{sale_id:05d}",
            "date_id":          date_id,
            "advertiser_id":    adv_id,
            "platform_id":      platform_id,
            "format_id":        fmt_id,
            "ad_medium":        medium,
            "duration_days":    duration_days,
            "gross_revenue_egp":gross_revenue,
            "discount_pct":     discount_pct,
            "net_revenue_egp":  net_revenue,
            "impressions_k":    impressions_k,
            "booking_status":   booking_status,
        })
        sale_id += 1

    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# FACT MONTHLY METRICS
# ─────────────────────────────────────────────
def gen_fact_monthly_metrics(dim_date):
    rng = np.random.default_rng(SEED + 30)
    months = (dim_date[dim_date["day"] == 1][["date_id", "month", "year"]]
              .copy().reset_index(drop=True))

    rows   = []
    row_id = 1

    prev_visitors = None

    for _, mrow in months.iterrows():
        yr  = int(mrow["year"])
        mo  = int(mrow["month"])
        t   = (yr - 2019) * 12 + (mo - 1)   # 0–71

        # ── Print Circulation ──────────────────
        # Declining from ~175K in Jan 2019 to ~100K by Dec 2024 (~6.2%/yr)
        base_circ = 175 * (0.938 ** (t / 12))
        # Seasonal: slightly higher in Jan (new year), lower in summer
        circ_seasonal = {1:1.04, 2:1.02, 3:1.05, 4:1.03, 5:1.00,
                         6:0.93, 7:0.90, 8:0.92, 9:1.00, 10:1.05, 11:1.03, 12:1.02}
        print_circulation_k = round(base_circ * circ_seasonal.get(mo, 1.0)
                                    * float(rng.uniform(0.97, 1.03)), 1)

        # ── Website Unique Visitors ────────────
        # Growing from ~2,400K in Jan 2019 to ~7,500K by Dec 2024 (~20%/yr)
        # 2020 COVID spike: people read news online more
        covid_boost = 1.25 if yr == 2020 else 1.0
        base_visitors = 2400 * (1.195 ** (t / 12)) * covid_boost
        # Summer slightly lower (travel), Ramadan season higher
        vis_seasonal = {1:1.00, 2:0.98, 3:1.10, 4:1.15, 5:1.08, 6:0.95,
                        7:0.90, 8:0.92, 9:1.02, 10:1.05, 11:1.05, 12:1.02}
        unique_visitors_k = round(base_visitors * vis_seasonal.get(mo, 1.0)
                                  * float(rng.uniform(0.96, 1.04)), 1)

        # ── Page Views ────────────────────────
        pv_ratio    = float(rng.uniform(3.0, 4.5))
        page_views_k = round(unique_visitors_k * pv_ratio, 1)

        # ── Bounce Rate (%) — improving UX ────
        # 2019: ~62%, 2024: ~44%
        base_bounce = 62 - t * (18 / 71)
        bounce_rate_pct = round(base_bounce + float(rng.uniform(-1.5, 1.5)), 1)

        # ── Avg Session Duration (min) ─────────
        # 2019: ~2.2 min, 2024: ~4.8 min
        base_session = 2.2 + t * (2.6 / 71)
        avg_session_min = round(base_session + float(rng.uniform(-0.2, 0.2)), 2)

        # ── Traffic trend (string) ─────────────
        if prev_visitors is None or unique_visitors_k > prev_visitors * 1.01:
            traffic_trend = "Growing"
        elif unique_visitors_k < prev_visitors * 0.99:
            traffic_trend = "Declining"
        else:
            traffic_trend = "Stable"
        prev_visitors = unique_visitors_k

        # ── Archive Licensing Revenue ──────────
        # Growing from ~400K EGP/mo (2019) to ~950K EGP/mo (2024)
        base_archive = 400 * (1.155 ** (t / 12))
        archive_licensing_egp = round(base_archive * float(rng.uniform(0.90, 1.10)), -2)

        # ── Commercial Printing Revenue ────────
        # Steady (~2,500K) growing with inflation: ~2,500K → ~6,000K
        infl = {2019:1.00, 2020:0.95, 2021:1.08, 2022:1.22, 2023:1.55, 2024:1.88}[yr]
        commercial_printing_egp = round(2500_000 * infl * float(rng.uniform(0.88, 1.12)), -3)

        # ── Operating Costs ───────────────────
        # Printing cost: high fixed cost, growing with inflation but declining volume
        printing_cost_egp = round(
            9_000_000 * infl * (0.96 ** (t / 12)) * float(rng.uniform(0.95, 1.05)), -3
        )
        # Distribution cost: declining as fewer copies printed
        distribution_cost_egp = round(
            3_500_000 * (0.92 ** (t / 12)) * float(rng.uniform(0.93, 1.07)), -3
        )
        # IT/Digital infrastructure: growing rapidly
        it_cost_egp = round(
            800_000 * (1.28 ** (t / 12)) * float(rng.uniform(0.92, 1.08)), -3
        )

        # ── Social Media ──────────────────────
        # Facebook: ~3,000K → ~9,500K
        fb_followers_k = round(3000 * (1.21 ** (t / 12)) * float(rng.uniform(0.98, 1.02)), 0)
        # Twitter/X: ~1,200K → ~3,800K
        tw_followers_k = round(1200 * (1.22 ** (t / 12)) * float(rng.uniform(0.98, 1.02)), 0)
        # Post engagement rate: declining as follower base grows
        post_engagement_pct = round(
            max(1.2, 4.5 - t * (3.0 / 71)) + float(rng.uniform(-0.3, 0.3)), 2
        )

        # ── Digital Upskilling ────────────────
        # Cumulative staff trained: ramps from 0 to ~850 over 6 years
        staff_trained_cumulative = int(min(850, t * 12 + int(rng.integers(0, 15))))

        rows.append({
            "metric_id":                f"MK{row_id:04d}",
            "date_id":                  mrow["date_id"],
            "print_circulation_k":      print_circulation_k,
            "unique_visitors_k":        unique_visitors_k,
            "page_views_k":             page_views_k,
            "bounce_rate_pct":          bounce_rate_pct,
            "avg_session_min":          avg_session_min,
            "traffic_trend":            traffic_trend,
            "archive_licensing_egp":    archive_licensing_egp,
            "commercial_printing_egp":  commercial_printing_egp,
            "printing_cost_egp":        printing_cost_egp,
            "distribution_cost_egp":    distribution_cost_egp,
            "it_cost_egp":              it_cost_egp,
            "fb_followers_k":           fb_followers_k,
            "tw_followers_k":           tw_followers_k,
            "post_engagement_pct":      post_engagement_pct,
            "staff_trained_cumulative": staff_trained_cumulative,
        })
        row_id += 1

    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# INJECT CLEANING ISSUES
# ─────────────────────────────────────────────
def inject_issues(df_ad, df_metrics, df_advertiser, df_platform, df_format):
    n   = len(df_ad)
    nm  = len(df_metrics)
    rng = np.random.default_rng(SEED + 99)

    # ── fact_ad_revenue ───────────────────────
    # 1. ~5% nulls in discount_pct
    idx1 = rng.choice(n, size=int(n * 0.05), replace=False)
    df_ad.loc[idx1, "discount_pct"] = np.nan

    # 2. ~4% nulls in duration_days
    idx2 = rng.choice(n, size=int(n * 0.04), replace=False)
    df_ad.loc[idx2, "duration_days"] = np.nan

    # 3. Inconsistent casing in booking_status (~3%)
    idx3 = rng.choice(n, size=int(n * 0.03), replace=False)
    df_ad.loc[idx3, "booking_status"] = df_ad.loc[idx3, "booking_status"].str.upper()

    # 4. net_revenue_egp stored as string in ~3% of rows
    df_ad["net_revenue_egp"] = df_ad["net_revenue_egp"].astype(object)
    idx4 = rng.choice(n, size=int(n * 0.03), replace=False)
    for i in idx4:
        df_ad.at[i, "net_revenue_egp"] = str(df_ad.at[i, "net_revenue_egp"])

    # 5. Negative net_revenue_egp (impossible) — 4 rows
    bad = rng.choice(n, size=4, replace=False)
    for i in bad:
        val = df_ad.at[i, "net_revenue_egp"]
        df_ad.at[i, "net_revenue_egp"] = -abs(float(val))

    # 6. Trailing whitespace in ad_medium (~2%)
    idx6 = rng.choice(n, size=int(n * 0.02), replace=False)
    df_ad.loc[idx6, "ad_medium"] = df_ad.loc[idx6, "ad_medium"] + " "

    # 7. Duplicate rows (~1.5%)
    dup_idx = rng.choice(n, size=int(n * 0.015), replace=False)
    dups    = df_ad.iloc[dup_idx].copy()
    df_ad   = pd.concat([df_ad, dups], ignore_index=True)

    # ── fact_monthly_metrics ──────────────────
    # 8. ~5% nulls in avg_session_min
    idx8 = rng.choice(nm, size=int(nm * 0.05), replace=False)
    df_metrics.loc[idx8, "avg_session_min"] = np.nan

    # 9. Inconsistent casing in traffic_trend (~3 rows — small table)
    idx9 = rng.choice(nm, size=max(2, int(nm * 0.03)), replace=False)
    df_metrics.loc[idx9, "traffic_trend"] = df_metrics.loc[idx9, "traffic_trend"].str.upper()

    # ── dim_advertiser ────────────────────────
    # 10. Inconsistent casing in advertiser_category for 4 rows
    s_idx = df_advertiser.sample(4, random_state=SEED).index
    df_advertiser.loc[s_idx, "advertiser_category"] = \
        df_advertiser.loc[s_idx, "advertiser_category"].str.lower()

    # ── dim_platform ──────────────────────────
    # 11. Trailing whitespace in medium for 2 rows
    df_platform.loc[df_platform["platform_id"].isin(["PF05", "PF06"]), "medium"] = "Digital "

    # ── dim_ad_format ─────────────────────────
    # 12. Inconsistent casing in medium for 2 rows
    df_format.loc[df_format["format_id"].isin(["AF08", "AF09"]), "medium"] = "digital"

    return df_ad, df_metrics, df_advertiser, df_platform, df_format

# ─────────────────────────────────────────────
# VALIDATION
# ─────────────────────────────────────────────
def validate(df_ad, df_metrics, dim_date, dim_advertiser, dim_platform, dim_format):
    print("\nValidation:")
    valid_dates = set(dim_date["date_id"])
    valid_adv   = set(dim_advertiser["advertiser_id"])
    valid_pf    = set(dim_platform["platform_id"])
    valid_fmt   = set(dim_format["format_id"])

    errors = []
    for col, valid, lbl in [
        ("date_id",      valid_dates, "ad date_id"),
        ("advertiser_id",valid_adv,   "ad advertiser_id"),
        ("platform_id",  valid_pf,    "ad platform_id"),
        ("format_id",    valid_fmt,   "ad format_id"),
    ]:
        bad = df_ad[~df_ad[col].isin(valid)]
        if len(bad): errors.append(f"  FK issue ({lbl}): {len(bad)} rows")

    bad_m = df_metrics[~df_metrics["date_id"].isin(valid_dates)]
    if len(bad_m): errors.append(f"  FK issue (metrics date_id): {len(bad_m)} rows")

    for e in errors: print(e)
    if not errors: print("  FK checks passed.")

    dups    = df_ad.duplicated().sum()
    str_rev = df_ad["net_revenue_egp"].apply(lambda x: isinstance(x, str)).mean()
    print_frac = (df_ad["ad_medium"].str.strip() == "Print").mean()
    print(f"  fact_ad_revenue rows (incl. dupes): {len(df_ad)}")
    print(f"  Duplicate rows:                     {dups}")
    print(f"  Null rate discount_pct:             {df_ad['discount_pct'].isna().mean():.1%}")
    print(f"  net_revenue_egp as string:          {str_rev:.1%}")
    print(f"  Print ad share:                     {print_frac:.1%}")
    print(f"  fact_monthly_metrics rows:          {len(df_metrics)}")
    print(f"  Null rate avg_session_min:          {df_metrics['avg_session_min'].isna().mean():.1%}")

# ─────────────────────────────────────────────
# INSTRUCTOR NOTES
# ─────────────────────────────────────────────
CLEANING_MD = """\
# Expected Cleaning Tasks — Al-Ahram Newspapers Company

## fact_ad_revenue.csv

| # | Issue | Column | Approx. Rate |
|---|-------|--------|--------------|
| 1 | Missing values | `discount_pct` | ~5% nulls |
| 2 | Missing values | `duration_days` | ~4% nulls |
| 3 | Inconsistent casing | `booking_status` | ~3% uppercase ("CONFIRMED", "CANCELLED") |
| 4 | Mixed data type | `net_revenue_egp` | ~3% stored as text strings |
| 5 | Impossible negative values | `net_revenue_egp` | 4 rows with negative values |
| 6 | Trailing whitespace | `ad_medium` | ~2% with trailing space ("Print ", "Digital ") |
| 7 | Duplicate rows | all columns | ~1.5% fully duplicated records |

**Note for instructor:** `impressions_k` is NULL for all print ad rows — this is intentional and by design (print ads have no digital impression tracking). Students should NOT treat this as a cleaning issue; they should filter by `ad_medium = "Digital"` before analysing impressions.

## fact_monthly_metrics.csv

| # | Issue | Column | Approx. Rate |
|---|-------|--------|--------------|
| 8 | Missing values | `avg_session_min` | ~5% nulls (~3–4 rows in this 72-row table) |
| 9 | Inconsistent casing | `traffic_trend` | ~3% uppercase ("GROWING", "DECLINING") |

## dim_advertiser.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 10 | Inconsistent casing | `advertiser_category` | 4 rows lowercase ("banking/finance", "fmcg") |

## dim_platform.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 11 | Trailing whitespace | `medium` | "Digital " (trailing space) for PF05, PF06 |

## dim_ad_format.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 12 | Inconsistent casing | `medium` | "digital" (lowercase) for AF08, AF09 |

## dim_date.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 13 | Date stored as string | `date` | Text "YYYY-MM-DD" — must be converted to Date type in Power Query |

## Notes for Instructor
- The `ad_medium` trailing whitespace issue means "Print" and "Print " act as separate filter values — very realistic and commonly encountered in analytics exports.
- Negative `net_revenue_egp` + string-type rows require the correct fix order: convert type first, then filter negatives.
- The `traffic_trend` casing issue distorts any "Growing months %" calculation directly.
- The `impressions_k` design null for print rows is an intentional teaching moment: not all null values are data quality errors.
"""

DAX_MD = """\
# Suggested DAX Measures — Al-Ahram Newspapers Company

## Ad Revenue
```dax
Total Net Revenue =
    CALCULATE(
        SUM(fact_ad_revenue[net_revenue_egp]),
        fact_ad_revenue[booking_status] = "Confirmed",
        fact_ad_revenue[net_revenue_egp] > 0
    )

Total Confirmed Bookings =
    CALCULATE(
        COUNTROWS(fact_ad_revenue),
        fact_ad_revenue[booking_status] = "Confirmed"
    )

Average Booking Value =
    DIVIDE([Total Net Revenue], [Total Confirmed Bookings])

Cancellation Rate =
    DIVIDE(
        CALCULATE(COUNTROWS(fact_ad_revenue),
                  fact_ad_revenue[booking_status] = "Cancelled"),
        COUNTROWS(fact_ad_revenue)
    )
```

## Print vs Digital Revenue
```dax
Print Revenue =
    CALCULATE([Total Net Revenue], fact_ad_revenue[ad_medium] = "Print")

Digital Revenue =
    CALCULATE([Total Net Revenue], fact_ad_revenue[ad_medium] = "Digital")

Digital Revenue % =
    DIVIDE([Digital Revenue], [Total Net Revenue])

Print Revenue % =
    DIVIDE([Print Revenue], [Total Net Revenue])
```

## Digital Engagement (from fact_monthly_metrics)
```dax
Avg Unique Visitors K =
    AVERAGE(fact_monthly_metrics[unique_visitors_k])

Avg Bounce Rate =
    AVERAGE(fact_monthly_metrics[bounce_rate_pct])

Avg Session Duration =
    CALCULATE(
        AVERAGE(fact_monthly_metrics[avg_session_min]),
        NOT(ISBLANK(fact_monthly_metrics[avg_session_min]))
    )

Total Archive Licensing Revenue =
    SUM(fact_monthly_metrics[archive_licensing_egp])
```

## Cost & Profitability
```dax
Total Printing Cost =
    SUM(fact_monthly_metrics[printing_cost_egp])

Total IT Cost =
    SUM(fact_monthly_metrics[it_cost_egp])

Total Distribution Cost =
    SUM(fact_monthly_metrics[distribution_cost_egp])

IT Cost Growth % =
    DIVIDE(
        [Total IT Cost] - CALCULATE([Total IT Cost], SAMEPERIODLASTYEAR(dim_date[date])),
        CALCULATE([Total IT Cost], SAMEPERIODLASTYEAR(dim_date[date]))
    )
```

## Growth & Time Intelligence
```dax
YTD Net Revenue =
    TOTALYTD([Total Net Revenue], dim_date[date])

MoM Revenue Growth % =
    VAR Prev = CALCULATE([Total Net Revenue], DATEADD(dim_date[date], -1, MONTH))
    RETURN DIVIDE([Total Net Revenue] - Prev, Prev)

YoY Revenue Growth % =
    DIVIDE(
        [Total Net Revenue] - CALCULATE([Total Net Revenue], SAMEPERIODLASTYEAR(dim_date[date])),
        CALCULATE([Total Net Revenue], SAMEPERIODLASTYEAR(dim_date[date]))
    )

YoY Digital Revenue Growth % =
    DIVIDE(
        [Digital Revenue] - CALCULATE([Digital Revenue], SAMEPERIODLASTYEAR(dim_date[date])),
        CALCULATE([Digital Revenue], SAMEPERIODLASTYEAR(dim_date[date]))
    )

YoY Print Circulation Change % =
    DIVIDE(
        AVERAGE(fact_monthly_metrics[print_circulation_k]) -
        CALCULATE(AVERAGE(fact_monthly_metrics[print_circulation_k]),
                  SAMEPERIODLASTYEAR(dim_date[date])),
        CALCULATE(AVERAGE(fact_monthly_metrics[print_circulation_k]),
                  SAMEPERIODLASTYEAR(dim_date[date]))
    )
```

## Social Media
```dax
Latest FB Followers K =
    LASTNONBLANK(fact_monthly_metrics[fb_followers_k],
                 AVERAGE(fact_monthly_metrics[fb_followers_k]))

Avg Post Engagement % =
    AVERAGE(fact_monthly_metrics[post_engagement_pct])
```
"""

DASHBOARD_MD = """\
# Dashboard Questions & Visual Suggestions — Al-Ahram Newspapers Company

## Analytical Questions (student-facing prompts)
1. How has total ad revenue split between Print and Digital changed from 2019 to 2024?
2. Which year showed the biggest acceleration in digital ad revenue — and can you link it to external events (COVID 2020, EGP devaluation 2023)?
3. Which advertiser category spends the most on digital ads? Which still prefers print?
4. How has website traffic (unique visitors) grown from 2019 to 2024, and what is the seasonal pattern?
5. How have bounce rate and average session duration changed over 6 years — is engagement improving?
6. How does archive licensing revenue trend compare to print circulation decline?
7. What is the operating cost structure — how do printing, distribution, and IT costs compare over time?
8. Which platform (Daily, Weekly, Evening, ahram.org.eg, Mobile App) generates the most ad revenue?
9. Which ad format has the highest average booking value?
10. How have Facebook and Twitter follower counts grown, and is engagement rate keeping pace?

## Suggested Visuals (instructor only)

| Visual | Type | Fields |
|--------|------|--------|
| Total Net Revenue KPI | Card | [Total Net Revenue] |
| Digital Revenue % KPI | Card | [Digital Revenue %] |
| Total Confirmed Bookings KPI | Card | [Total Confirmed Bookings] |
| Avg Unique Visitors KPI | Card | [Avg Unique Visitors K] |
| Print vs Digital Revenue Over Time | Area/Line | dim_date[year], Print vs Digital (stacked) |
| Revenue by Platform | Bar | dim_platform[platform_name], [Total Net Revenue] |
| Revenue by Ad Format | Bar | dim_ad_format[format_name], [Total Net Revenue] |
| Revenue by Advertiser Category | Bar | dim_advertiser[advertiser_category], [Total Net Revenue] |
| YoY Revenue Growth | Line | dim_date[year], [YoY Revenue Growth %] |
| Unique Visitors Trend | Line | dim_date[month_name], [Avg Unique Visitors K] |
| Bounce Rate & Session Duration | Dual-line | dim_date[year], bounce_rate + avg_session |
| Print Circulation Decline | Line | dim_date[year], print_circulation_k |
| Operating Cost Breakdown | Stacked bar | dim_date[year], printing + distribution + IT |
| Social Followers Growth | Line | dim_date[year], fb + twitter followers |
| Cancellation Rate | Card/Bar | [Cancellation Rate] |

## Suggested Slicers
- Year / Quarter / Month
- Ad Medium (Print / Digital)
- Platform
- Advertiser Category / Tier
- Booking Status
- Ad Format

## Dashboard Pages Suggestion
1. **Revenue Overview** — total revenue, print vs digital trend, top advertisers
2. **Digital Transformation** — digital revenue %, mobile share, e-commerce channel
3. **Audience & Engagement** — unique visitors, bounce rate, session duration, social media
4. **Operations & Costs** — printing, distribution, IT costs over time; circulation decline
"""

MODEL_MD = """\
# Star Schema Relationships — Al-Ahram Newspapers Company

## Tables
- **fact_ad_revenue** — main fact: advertisement bookings (~2,000+ rows, 2019–2024)
- **fact_monthly_metrics** — secondary fact: monthly company-wide KPI snapshot (72 rows)
- **dim_date** — date dimension shared by both facts (2019–2024, 2,192 rows)
- **dim_advertiser** — advertiser dimension (100 rows)
- **dim_platform** — publication/platform dimension (6 rows)
- **dim_ad_format** — ad format dimension (12 rows)

## Relationships

### fact_ad_revenue
| Fact Column | → | Dimension | PK | Cardinality | Filter |
|-------------|---|-----------|----|-------------|--------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single |
| `advertiser_id` | → | `dim_advertiser` | `advertiser_id` | Many-to-One | Single |
| `platform_id` | → | `dim_platform` | `platform_id` | Many-to-One | Single |
| `format_id` | → | `dim_ad_format` | `format_id` | Many-to-One | Single |

### fact_monthly_metrics
| Fact Column | → | Dimension | PK | Cardinality | Filter |
|-------------|---|-----------|----|-------------|--------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single |

## Notes
- Both fact tables share `dim_date` — Power BI handles this correctly.
- `fact_monthly_metrics` has no dimension other than `dim_date`; it is a company-level aggregate scorecard. Do not connect it to dim_platform or dim_advertiser.
- `impressions_k` in `fact_ad_revenue` is NULL for all print ad rows — this is intentional. Students should filter to `ad_medium = "Digital"` before using this column.
- Mark `dim_date[date]` as a **Date Table** after converting from string to Date type.
- `net_revenue_egp` must be converted to Decimal Number (fixing type and removing negatives) before any SUM will work.
- The `ad_medium` column is a convenience denormalisation from `dim_platform[medium]` — either works for filtering.
"""

DATA_DICT_MD = """\
# Data Dictionary — Al-Ahram Newspapers Company
## Digital Transformation Course · BINF 402 · GIU · Spring 2026

---

## Business Story
Al-Ahram, founded in 1875, is Egypt's oldest and most prominent media company. It operates Egypt's flagship daily Arabic newspaper, an English weekly, an evening edition, the leading Arabic news portal (ahram.org.eg), a mobile news app, and one of the most-watched Egyptian YouTube channels.

This dataset covers **advertisement bookings** and **monthly company performance metrics** for 2019–2024 — a period of dramatic digital transformation, with EGP devaluation, COVID-19, and the global shift from print to digital media all shaping business outcomes. Your goal as a Media Executive is to track how ad revenue is shifting from print to digital, whether audience growth is compensating for print circulation decline, and how the cost structure is evolving.

---

## Files

### `fact_ad_revenue.csv` (main fact table)
| Column | Description |
|--------|-------------|
| `booking_id` | Unique advertisement booking identifier |
| `date_id` | Foreign key → `dim_date.date_id` (booking date) |
| `advertiser_id` | Foreign key → `dim_advertiser.advertiser_id` |
| `platform_id` | Foreign key → `dim_platform.platform_id` |
| `format_id` | Foreign key → `dim_ad_format.format_id` |
| `ad_medium` | Print or Digital (convenience column) |
| `duration_days` | Number of days the ad ran (1 for print insertions) |
| `gross_revenue_egp` | Revenue before discount (EGP) |
| `discount_pct` | Discount applied (decimal, e.g. 0.10 = 10%) |
| `net_revenue_egp` | Final billed revenue after discount (EGP) |
| `impressions_k` | Estimated digital impressions/views (thousands) — **NULL for print ads by design** |
| `booking_status` | Confirmed, Under Review, or Cancelled |

### `fact_monthly_metrics.csv` (secondary fact table — monthly KPI scorecard)
| Column | Description |
|--------|-------------|
| `metric_id` | Unique row identifier |
| `date_id` | Foreign key → `dim_date.date_id` (first day of the month) |
| `print_circulation_k` | Average daily print copies distributed (thousands) |
| `unique_visitors_k` | Monthly unique website visitors (thousands) |
| `page_views_k` | Monthly page views across digital platforms (thousands) |
| `bounce_rate_pct` | Website bounce rate (%) |
| `avg_session_min` | Average visitor session duration (minutes) |
| `traffic_trend` | Growing, Stable, or Declining (vs prior month) |
| `archive_licensing_egp` | Monthly revenue from digital archive licensing (EGP) |
| `commercial_printing_egp` | Monthly revenue from external commercial printing services (EGP) |
| `printing_cost_egp` | Monthly newspaper printing cost (EGP) |
| `distribution_cost_egp` | Monthly newspaper distribution cost (EGP) |
| `it_cost_egp` | Monthly IT & digital infrastructure cost (EGP) |
| `fb_followers_k` | Facebook page followers at month-end (thousands) |
| `tw_followers_k` | Twitter/X followers at month-end (thousands) |
| `post_engagement_pct` | Average engagement rate across social posts (%) |
| `staff_trained_cumulative` | Cumulative number of staff who completed digital upskilling programmes |

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

### `dim_advertiser.csv`
| Column | Description |
|--------|-------------|
| `advertiser_id` | Primary key |
| `advertiser_name` | Synthetic company name |
| `advertiser_category` | Government, Banking/Finance, Telecom, Real Estate, FMCG, Automotive, Healthcare, Education, or Retail |
| `platform_preference` | Print_Heavy, Mixed, or Digital_Heavy |
| `advertiser_tier` | Premium, Standard, or Budget |

### `dim_platform.csv`
| Column | Description |
|--------|-------------|
| `platform_id` | Primary key |
| `platform_name` | Al-Ahram Daily, Al-Ahram Weekly, Al-Masaa Evening, ahram.org.eg, Al-Ahram Mobile App, Al-Ahram YouTube |
| `medium` | Print or Digital |
| `description` | Brief platform description |

### `dim_ad_format.csv`
| Column | Description |
|--------|-------------|
| `format_id` | Primary key |
| `format_name` | Full Page, Half Page, Display Banner, Video Pre-roll 15s, etc. |
| `medium` | Print or Digital |
| `base_rate_egp` | Reference base rate (EGP, in 2019 terms) |
| `rate_basis` | per insertion (print) or per day / per placement (digital) |

---

## Intended Relationships
- `fact_ad_revenue` → `dim_date`, `dim_advertiser`, `dim_platform`, `dim_ad_format`
- `fact_monthly_metrics` → `dim_date`

## Notes for Students
- `net_revenue_egp` must be converted to a numeric type before any SUM measure will work.
- `impressions_k` is NULL for all print ad rows — this is **by design**, not a data error. Only use this column when filtering to Digital ads.
- The dataset spans 2019–2024: print ad revenue will show a clear decline while digital grows — this is the central insight to explore.
- Ad prices in 2023–2024 are significantly higher in EGP terms due to currency devaluation — compare prices across years carefully.
- `fact_monthly_metrics` contains one row per month (72 rows total). Connect it to `dim_date` to enable time-series analysis of traffic, costs, and social media.
- Clean all data in Power Query before building any measures or visuals.
"""

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print("=" * 60)
    print("Al-Ahram Newspapers Company — Dataset Generator")
    print("=" * 60)
    make_dirs()

    print("\n[1/5] Generating dimension tables...")
    dim_date       = gen_dim_date()
    dim_platform   = gen_dim_platform()
    dim_ad_format  = gen_dim_ad_format()
    dim_advertiser = gen_dim_advertiser()

    print("\n[2/5] Generating fact tables...")
    fact_ad      = gen_fact_ad_revenue(dim_date, dim_advertiser, dim_platform, dim_ad_format)
    fact_metrics = gen_fact_monthly_metrics(dim_date)

    print("\n[3/5] Injecting cleaning issues...")
    fact_ad, fact_metrics, dim_advertiser, dim_platform, dim_ad_format = inject_issues(
        fact_ad, fact_metrics, dim_advertiser, dim_platform, dim_ad_format
    )

    print("\n[4/5] Saving files...")
    save(dim_date,       f"{STUDENT_DIR}/dim_date.csv")
    save(dim_platform,   f"{STUDENT_DIR}/dim_platform.csv")
    save(dim_ad_format,  f"{STUDENT_DIR}/dim_ad_format.csv")
    save(dim_advertiser, f"{STUDENT_DIR}/dim_advertiser.csv")
    save(fact_ad,        f"{STUDENT_DIR}/fact_ad_revenue.csv")
    save(fact_metrics,   f"{STUDENT_DIR}/fact_monthly_metrics.csv")

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
    validate(fact_ad, fact_metrics, dim_date, dim_advertiser, dim_platform, dim_ad_format)

    print("\n" + "=" * 60)
    print("Done. Output folder: output/alahram/")
    print("  student_dataset/          → share with students")
    print("  data_dictionary.md        → share with students")
    print("  private_instructor_notes/ → instructor only")
    print("=" * 60)


if __name__ == "__main__":
    main()

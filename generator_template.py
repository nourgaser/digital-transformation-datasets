"""
<COMPANY NAME> — <Brief description>
Dataset Generator for Digital Transformation Course - BINF 402, Spring 2026
GIU - Dr. Nourhan Hamdi
Team: <list team members>

HOW TO USE THIS TEMPLATE
─────────────────────────
1. Copy this file: cp generator_template.py generate_<slug>.py
2. Replace every <PLACEHOLDER> with company-specific values
3. Add/remove dim and fact functions to match the schema you designed
4. Run: source .venv/bin/activate && python generate_<slug>.py
5. Verify output and fix any validation errors

See AGENTS.md for full conventions, ratios, and design patterns.
"""

import os
import random
import numpy as np
import pandas as pd
from faker import Faker
from datetime import date, timedelta

# ─────────────────────────────────────────────
# CONSTANTS  ← change these first
# ─────────────────────────────────────────────
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
fake_en = Faker("en_US")
fake_en.seed_instance(SEED)

PROJECT_SLUG = "<slug>"              # e.g. "abc_company"
OUTPUT_BASE  = f"output/{PROJECT_SLUG}"
STUDENT_DIR  = f"{OUTPUT_BASE}/student_dataset"
PRIVATE_DIR  = f"{OUTPUT_BASE}/private_instructor_notes"

DATE_START = date(2023, 1, 1)
DATE_END   = date(2024, 12, 31)
TARGET_FACT_ROWS = 2000              # main fact table before duplicate injection
TARGET_SECONDARY_ROWS = 400         # secondary fact table if you have one (else delete)

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
# DIM DATE  ← keep this exactly as-is
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
            "date":        d.strftime("%Y-%m-%d"),   # intentionally text — cleaning task
            "day":         d.day,
            "month":       d.month,
            "month_name":  d.strftime("%B"),
            "quarter":     (d.month - 1) // 3 + 1,
            "year":        d.year,
            "day_of_week": d.strftime("%A"),
            "is_weekend":  d.weekday() >= 4,          # Fri + Sat
            "is_holiday":  d in EGYPTIAN_HOLIDAYS,
        })
        d += timedelta(days=1)
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# DIM <ENTITY_1>  ← e.g. dim_product, dim_branch
# Replace with your first dimension
# ─────────────────────────────────────────────
# <ENTITY_1>_RAW = [
#     # (id, name, category, ...)
#     ("E01", "Example A", "Cat 1", ...),
# ]

def gen_dim_entity1():
    # rows = [{"entity1_id": r[0], "name": r[1], ...} for r in <ENTITY_1>_RAW]
    # return pd.DataFrame(rows)
    raise NotImplementedError("Replace this with your first dimension")

# ─────────────────────────────────────────────
# DIM <ENTITY_2>  ← e.g. dim_customer, dim_channel
# ─────────────────────────────────────────────
def gen_dim_entity2(n=150):
    rng  = np.random.default_rng(SEED + 10)
    rows = []
    for i in range(1, n + 1):
        rows.append({
            "entity2_id":  f"E2{i:04d}",
            "name":        fake_en.name(),
            # add more fields...
        })
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# SEASONALITY HELPER  ← customise per business
# ─────────────────────────────────────────────
def seasonality_weight(month: int) -> float:
    """Return a relative weight for sampling dates by month.
    Adjust these values to match your company's business cycles."""
    weights = {
        1: 1.0, 2: 0.9,  3: 1.0,  4: 1.0,
        5: 1.0, 6: 0.85, 7: 0.85, 8: 1.1,
        9: 1.1, 10: 1.1, 11: 1.1, 12: 1.3,
    }
    return weights.get(month, 1.0)

# ─────────────────────────────────────────────
# FACT <MAIN>  ← rename and fill in
# ─────────────────────────────────────────────
def gen_fact_main(dim_date, dim_entity1, dim_entity2):
    rng = np.random.default_rng(SEED + 20)

    # entity1_ids = dim_entity1["entity1_id"].tolist()
    # entity2_ids = dim_entity2["entity2_id"].tolist()

    rows   = []
    row_id = 1

    for _ in range(TARGET_FACT_ROWS):
        # 1. Sample date with seasonality
        date_row = dim_date.sample(1,
            weights=dim_date["month"].map(seasonality_weight)).iloc[0]
        date_id = date_row["date_id"]
        year    = date_row["year"]

        # 2. Pick dimension FKs
        # entity1_id = random.choice(entity1_ids)
        # entity2_id = rng.choice(entity2_ids)

        # 3. Compute numeric fields — use realistic distributions
        # value = round(rng.uniform(min_val, max_val), 2)

        # 4. Append row dict
        rows.append({
            "fact_id":   f"F{row_id:05d}",
            "date_id":   date_id,
            # "entity1_id": entity1_id,
            # "entity2_id": entity2_id,
            # "value":      value,
            # ... more fields ...
        })
        row_id += 1

    return pd.DataFrame(rows)

# ─────────────────────────────────────────────
# INJECT CLEANING ISSUES  ← follow standard recipe from AGENTS.md
# ─────────────────────────────────────────────
def inject_issues(df_main, dim_entity1, dim_entity2):
    n   = len(df_main)
    rng = np.random.default_rng(SEED + 99)

    # 1. ~5% nulls in a numeric column
    idx1 = rng.choice(n, size=int(n * 0.05), replace=False)
    # df_main.loc[idx1, "some_numeric_col"] = np.nan

    # 2. ~4% nulls in another column
    idx2 = rng.choice(n, size=int(n * 0.04), replace=False)
    # df_main.loc[idx2, "another_col"] = np.nan

    # 3. ~3% inconsistent casing in a status/category column
    idx3 = rng.choice(n, size=int(n * 0.03), replace=False)
    # df_main.loc[idx3, "status_col"] = df_main.loc[idx3, "status_col"].str.upper()

    # 4. ~3% main revenue column stored as string (type mismatch)
    # df_main["revenue_col"] = df_main["revenue_col"].astype(object)
    idx4 = rng.choice(n, size=int(n * 0.03), replace=False)
    # for i in idx4:
    #     df_main.at[i, "revenue_col"] = str(df_main.at[i, "revenue_col"])

    # 5. 3–4 rows with impossible negative values in revenue column
    bad = rng.choice(n, size=4, replace=False)
    # for i in bad:
    #     df_main.at[i, "revenue_col"] = -abs(float(df_main.at[i, "revenue_col"]))

    # 6. ~2% trailing/leading whitespace in a string column
    idx6 = rng.choice(n, size=int(n * 0.02), replace=False)
    # df_main.loc[idx6, "string_col"] = df_main.loc[idx6, "string_col"] + " "

    # 7. ~1.5% duplicate rows
    dup_idx = rng.choice(n, size=int(n * 0.015), replace=False)
    dups    = df_main.iloc[dup_idx].copy()
    df_main = pd.concat([df_main, dups], ignore_index=True)

    # 8. Dim table issues — target 2–5 specific rows by ID
    # dim_entity1.loc[dim_entity1["entity1_id"].isin(["E01","E02"]), "category"] = "category "
    # dim_entity2.loc[dim_entity2.sample(4, random_state=SEED).index, "type_col"] = \
    #     dim_entity2.loc[...]["type_col"].str.lower()

    return df_main, dim_entity1, dim_entity2

# ─────────────────────────────────────────────
# VALIDATION  ← always include FK checks
# ─────────────────────────────────────────────
def validate(df_main, dim_date, dim_entity1, dim_entity2):
    print("\nValidation:")
    valid_dates = set(dim_date["date_id"])
    # valid_e1    = set(dim_entity1["entity1_id"])
    # valid_e2    = set(dim_entity2["entity2_id"])

    errors = []
    bad_dates = df_main[~df_main["date_id"].isin(valid_dates)]
    if len(bad_dates): errors.append(f"  FK issue (date_id): {len(bad_dates)} rows")
    # repeat for other FK columns ...

    for e in errors: print(e)
    if not errors: print("  FK checks passed.")

    dups = df_main.duplicated().sum()
    print(f"  Fact rows (incl. dupes): {len(df_main)}")
    print(f"  Duplicate rows:          {dups}")
    # print(f"  Null rate <col>:         {df_main['col'].isna().mean():.1%}")

# ─────────────────────────────────────────────
# INSTRUCTOR NOTE STRINGS  ← fill these in
# ─────────────────────────────────────────────
CLEANING_MD = """\
# Expected Cleaning Tasks — <COMPANY NAME>

## fact_<main>.csv

| # | Issue | Column | Approx. Rate |
|---|-------|--------|--------------|
| 1 | Missing values | `<col>` | ~5% nulls |
| 2 | Missing values | `<col>` | ~4% nulls |
| 3 | Inconsistent casing | `<status_col>` | ~3% |
| 4 | Mixed data type | `<revenue_col>` | ~3% stored as text |
| 5 | Impossible values | `<revenue_col>` | 4 rows with negative values |
| 6 | Whitespace | `<string_col>` | ~2% |
| 7 | Duplicate rows | all columns | ~1.5% |

## dim_<x>.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 8 | Inconsistent casing | `<col>` | ... |

## dim_date.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 9 | Date stored as string | `date` | Must be converted to Date type in Power Query |

## Notes for Instructor
- <add pedagogical notes here>
"""

DAX_MD = """\
# Suggested DAX Measures — <COMPANY NAME>

## Core KPIs
```dax
Total Revenue =
    CALCULATE(
        SUM(fact_main[revenue_col]),
        fact_main[status_col] = "Active"
    )

Total Records =
    COUNTROWS(fact_main)

Average Value =
    DIVIDE([Total Revenue], [Total Records])
```

## Growth
```dax
YTD Revenue =
    TOTALYTD([Total Revenue], dim_date[date])

MoM Growth % =
    VAR Prev = CALCULATE([Total Revenue], DATEADD(dim_date[date], -1, MONTH))
    RETURN DIVIDE([Total Revenue] - Prev, Prev)

YoY Growth % =
    DIVIDE(
        [Total Revenue] - CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(dim_date[date])),
        CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(dim_date[date]))
    )
```

## <Add more measures matching the team's requested KPIs>
"""

DASHBOARD_MD = """\
# Dashboard Questions & Visual Suggestions — <COMPANY NAME>

## Analytical Questions (student-facing)
1. <question>
2. <question>
...

## Suggested Visuals (instructor only)

| Visual | Type | Fields |
|--------|------|--------|
| <KPI name> | Card | [<measure>] |
| <chart name> | Bar | dim_x[col], [measure] |
...

## Suggested Slicers
- Year / Quarter
- <other relevant slicers>
"""

MODEL_MD = """\
# Star Schema Relationships — <COMPANY NAME>

## Tables
- **fact_main** — <description>
- **dim_date** — date dimension
- **dim_entity1** — <description>
- **dim_entity2** — <description>

## Relationships

| Fact Column | → | Dimension | PK | Cardinality | Filter Direction |
|-------------|---|-----------|----|-------------|-----------------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single |
| `entity1_id` | → | `dim_entity1` | `entity1_id` | Many-to-One | Single |
| `entity2_id` | → | `dim_entity2` | `entity2_id` | Many-to-One | Single |

## Notes
- Mark `dim_date[date]` as a Date Table after converting from string.
- <add any caveats about nullable FKs, shared dimensions, etc.>
"""

DATA_DICT_MD = """\
# Data Dictionary — <COMPANY NAME>
## Digital Transformation Course · BINF 402 · GIU · Spring 2026

---

## Business Story
<2–3 sentences describing the company and what the data represents.>

---

## Files

### `fact_main.csv` (main fact table)
| Column | Description |
|--------|-------------|
| `fact_id` | Unique identifier |
| `date_id` | Foreign key → `dim_date.date_id` |
| ... | ... |

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

### `dim_entity1.csv`
| Column | Description |
|--------|-------------|
| `entity1_id` | Primary key |
| ... | ... |

---

## Intended Relationships
- `fact_main.date_id` → `dim_date.date_id`
- `fact_main.entity1_id` → `dim_entity1.entity1_id`
- `fact_main.entity2_id` → `dim_entity2.entity2_id`

## Notes for Students
- Clean data types and fix inconsistencies **before** building relationships in Power BI.
- Mark `dim_date` as a Date Table after converting the `date` column from text to Date.
"""

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print("=" * 55)
    print("<COMPANY NAME> — Dataset Generator")
    print("=" * 55)
    make_dirs()

    print("\n[1/5] Generating dimension tables...")
    dim_date    = gen_dim_date()
    dim_entity1 = gen_dim_entity1()
    dim_entity2 = gen_dim_entity2(n=150)

    print("\n[2/5] Generating fact table(s)...")
    fact_main = gen_fact_main(dim_date, dim_entity1, dim_entity2)

    print("\n[3/5] Injecting cleaning issues...")
    fact_main, dim_entity1, dim_entity2 = inject_issues(
        fact_main, dim_entity1, dim_entity2
    )

    print("\n[4/5] Saving files...")
    save(dim_date,    f"{STUDENT_DIR}/dim_date.csv")
    save(dim_entity1, f"{STUDENT_DIR}/dim_entity1.csv")
    save(dim_entity2, f"{STUDENT_DIR}/dim_entity2.csv")
    save(fact_main,   f"{STUDENT_DIR}/fact_main.csv")

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
    validate(fact_main, dim_date, dim_entity1, dim_entity2)

    print("\n" + "=" * 55)
    print(f"Done. Output folder: output/{PROJECT_SLUG}/")
    print("  student_dataset/          → share with students")
    print("  data_dictionary.md        → share with students")
    print("  private_instructor_notes/ → instructor only")
    print("=" * 55)

if __name__ == "__main__":
    main()

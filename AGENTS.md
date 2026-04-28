# AGENTS.md — Full Specification for Dataset Generation
## Digital Transformation Course · BINF 402 · GIU · Spring 2026

This file is written for **any AI agent** (Claude, GPT, Codex, Gemini, or any future model) that needs to generate a synthetic dataset package for a new student team. It is fully self-contained — no prior conversation context is needed.

---

## 1. What you are doing and why

Students at GIU take a course called Digital Transformation (BINF 402). Each team picks a real Egyptian company and submits a Project Deliverable 1 (PD1) document describing that company's digital transformation journey. Teams also send an email specifying what kind of data and dashboard they want to build in Power BI.

Your job is to:
1. Read the team's PD1 and/or email from `inputs/<slug>/`
2. Understand the actual business story, products, KPIs, and dashboard goals
3. Write a Python script (`generate_<slug>.py`) that produces a realistic synthetic dataset
4. Run the script, verify it works, and confirm the output is correct

The dataset will be used by students to practice data cleaning, Power BI data modeling, DAX measures, and dashboard building. It must be educational, realistic, and free of real personal data.

---

## 2. Input file locations and formats

```
inputs/
  <company_slug>/
    mail.md         # student email — always present; contains company description,
                    # dashboard goals, KPIs, and data requests
    *.pdf           # PD1 document — sometimes present; more detailed company analysis
```

**Always read both files if they exist.** The email is usually more specific about what data fields they want. The PD1 has more business context.

If only one file exists, work with what you have and note assumptions.

---

## 3. Output structure — exactly what to produce

For each team, produce these files:

```
output/<slug>/
  student_dataset/
    dim_date.csv
    dim_<x>.csv          (2–4 more dimension tables)
    fact_<main>.csv      (main fact table, 2000–2030 rows after dupe injection)
    fact_<secondary>.csv (optional second fact table, 200–700 rows)
  data_dictionary.md
  private_instructor_notes/
    expected_cleaning_tasks.md
    suggested_dax_measures.md
    dashboard_questions.md
    model_relationships.md
```

And one script at the root:
```
generate_<slug>.py
```

---

## 4. Schema rules — star schema for beginners

- One central fact table, optionally one secondary fact table
- All dimension tables have a simple primary key (`<dim>_id`)
- All fact tables reference those keys as foreign keys
- **No snowflake schemas** — keep dimensions flat
- **No many-to-many** relationships
- If two fact tables share dimensions, that is fine — Power BI handles it correctly

### Standard dim_date columns (always include this table)

| Column | Type | Notes |
|--------|------|-------|
| `date_id` | string | YYYYMMDD — primary key |
| `date` | string | "YYYY-MM-DD" — intentionally stored as text (cleaning task) |
| `day` | int | |
| `month` | int | |
| `month_name` | string | |
| `quarter` | int | 1–4 |
| `year` | int | |
| `day_of_week` | string | |
| `is_weekend` | bool | Friday + Saturday for Egypt |
| `is_holiday` | bool | Egyptian public holidays |

### Egyptian public holidays to use

```python
EGYPTIAN_HOLIDAYS = {
    date(YEAR, 1, 7),   # Coptic Christmas
    date(YEAR, 4, 25),  # Sinai Liberation Day
    date(YEAR, 5, 1),   # Labour Day
    date(YEAR, 6, 30),  # June 30 Revolution
    date(YEAR, 7, 23),  # Revolution Day
    date(YEAR, 10, 6),  # Armed Forces Day
}
# Repeat for each year in your date range
```

---

## 5. Fact table design rules

### Size
- Main fact table: **2,000 rows before duplicate injection** → ends up ~2,030 rows
- Secondary fact table: 200–700 rows depending on what it represents

### Required realism — do not make purely random data

Every fact table must have at least three of these patterns:

| Pattern | How to implement |
|---------|-----------------|
| Seasonality | Weight date sampling by month using a dict of weights |
| Product/category popularity | Use `random.choices(ids, weights=wts)` |
| Customer segment × behavior | Different quantity ranges / discount profiles per segment |
| Geographic variation | Different weights per branch/region |
| Channel shift over time | Different channel weights for 2023 vs 2024 |
| Price inflation | Multiply prices by ~1.15–1.20 for year 2024 vs 2023 (EGP devaluation) |
| Cancellation / returns | ~4–8% of records with zero-revenue status |

### Date sampling with seasonality

```python
def seasonality_weight(month):
    weights = {1:1.0, 2:0.9, ..., 12:1.3}
    return weights.get(month, 1.0)

# Sample a date row weighted by month
date_row = dim_date.sample(1, weights=dim_date["month"].map(seasonality_weight)).iloc[0]
```

---

## 6. Cleaning issues — exactly what to inject and at what rates

Every dataset must have **light-to-moderate** dirty data. Do not overdo it.

### Standard injection recipe

Apply these in `inject_issues()` using `np.random.default_rng(SEED + 99)`:

| # | Issue | Target column(s) | Rate | How |
|---|-------|-----------------|------|-----|
| 1 | Null values | One numeric col in main fact | ~5% | `df.loc[idx, col] = np.nan` |
| 2 | Null values | Another col in main fact | ~4% | same |
| 3 | Inconsistent casing | Status/category string col | ~3% | `.str.upper()` or `.str.lower()` |
| 4 | Mixed data type | Main revenue/value column | ~3% | cast subset to `str(value)` |
| 5 | Impossible values | Same revenue col or a numeric | 3–4 rows | negate the value |
| 6 | Whitespace | A string col in main fact | ~2% | `" " + col` or `col + " "` |
| 7 | Duplicate rows | Main fact table | ~1.5% | `pd.concat([df, df.iloc[dup_idx]])` |
| 8 | Null values | A col in secondary fact | ~5% | |
| 9 | Casing | A col in secondary fact | ~3% | |
| 10 | Casing/whitespace | A dim table col | 4–5 rows | targeted by ID |
| 11 | Casing/whitespace | Another dim table col | 2–3 rows | targeted by ID |
| 12 | Date as string | `dim_date.date` | 100% | intentional — always leave this as text |

### Critical: the revenue/value column compound issue

Always make the **main revenue column** have two simultaneous issues:
1. ~3% of values stored as `str(value)` (type issue)
2. A few rows with negative values (impossible values)

This forces students to fix the type first, then filter the negatives — the correct order.

### Always leave `dim_date.date` as a text string

This forces students to convert it to a Date type in Power Query, which is required for time intelligence DAX to work.

---

## 7. Python code conventions

### File structure (top to bottom)

```python
"""
<Company Name>
Dataset Generator — BINF 402, Digital Transformation, GIU, Spring 2026
Dr. Nourhan Hamdi
Team: <names>
"""

import os, random
import numpy as np
import pandas as pd
from faker import Faker
from datetime import date, timedelta

# 1. CONSTANTS (SEED, paths, date range, row targets)
# 2. HELPERS (make_dirs, save)
# 3. DIM DATE
# 4. COMPANY-SPECIFIC DIMENSIONS (each in its own function)
# 5. FACT TABLES (each in its own function)
# 6. inject_issues()
# 7. validate()
# 8. INSTRUCTOR NOTE STRINGS (as module-level string constants)
# 9. main()
```

### Always use a fixed seed everywhere

```python
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
fake_en = Faker("en_US")
fake_en.seed_instance(SEED)
# For numpy operations inside functions:
rng = np.random.default_rng(SEED + <offset>)  # use different offsets per function
```

### Standard save function

```python
def save(df: pd.DataFrame, path: str):
    df.to_csv(path, index=False, encoding="utf-8")
    print(f"  Saved {path}  ({len(df)} rows)")
```

### Standard validation function — always include

Check that every FK in every fact table exists in the corresponding dimension table. Report row counts, null rates for injected columns, and duplicate count. Print warnings if something is wrong.

### Avoid these common mistakes

- Do **not** use `pd.DataFrame.sample()` with `random_state` inside loops — use `np.random.default_rng` instead for reproducibility
- Do **not** use `PRODUCTS_RAW = [...]` closed with `)` — use `]` (easy typo)
- Do **not** hardcode hundreds of rows — use Python loops and distributions
- Do **not** put `np` as a variable name when you also `import numpy as np`
- When casting a column to `object` for mixed-type injection, do it **before** the loop: `df["col"] = df["col"].astype(object)`

---

## 8. Instructor notes — what each file must contain

### `expected_cleaning_tasks.md`
A markdown table listing every injected issue: column name, issue type, approximate rate, and a note for the instructor on why it matters pedagogically.

### `suggested_dax_measures.md`
8–15 DAX measures appropriate for the project. Must include:
- A core revenue/volume measure with a status filter (e.g. only "Signed" or "Approved" records)
- At least one `DIVIDE()` ratio measure
- At least one time intelligence measure: `TOTALYTD`, `DATEADD`, or `SAMEPERIODLASTYEAR`
- At least one growth % measure (MoM or YoY)
- KPIs that match what the team asked for in their email

### `dashboard_questions.md`
- 8–10 analytical questions the students should be able to answer
- A table of suggested Power BI visuals (type + fields) — **instructor-only, not in data dictionary**
- Suggested slicers

### `model_relationships.md`
A table for every fact→dimension relationship:
- Fact column → Dimension table → Dimension PK
- Cardinality (always Many-to-One)
- Filter direction (always Single: dimension → fact)
- Any caveats (nullable FKs, shared dimensions, etc.)

### `data_dictionary.md` (student-facing)
- Short business story paragraph
- A table for every CSV: each column with a plain-English description
- The intended relationships (just list them, don't explain the full solution)
- A "Notes for Students" section reminding them to clean before modeling

---

## 9. Dimension design patterns by industry

Use these as starting points — adapt based on what the PD1/email actually describes.

### Retail / Sales / Publishing
- `dim_product` — product_id, name, category, price, cost
- `dim_customer` — customer_id, name, type (Individual/Corporate/Wholesale), governorate, region
- `dim_channel` — channel_id, name (Online/Retail/Wholesale/Agent), type (B2C/B2B)
- `dim_branch` — optional if multi-location

### Banking / Finance
- `dim_branch` — branch_id, name, governorate, region, tier
- `dim_customer` — segment (Retail/Premium/SME/Corporate), age, digital_enrolled
- `dim_product` — banking products (Loan/Deposit/Card/Digital)
- `dim_channel` — In-Branch/ATM/Mobile App/Internet Banking/Call Center

### Insurance
- `dim_product` — insurance lines (Motor/Property/Marine/Travel/Engineering)
- `dim_customer` — customer_id, type (Individual/Corporate), age, gender, region
- `dim_branch` — branch_id, location
- `dim_channel` — Branch/Agent/Broker/Online/Call Center

### Transportation / Logistics
- `dim_route` — origin, destination, distance, type (express/standard)
- `dim_vehicle` — train/bus/truck type, capacity by class
- `dim_channel` — booking channels (Online/Offline/App/Vending)
- `dim_station` / `dim_branch` — if relevant

### Real Estate
- `dim_project` — project_id, name, location, type (Residential/Commercial/Resort), launch year
- `dim_unit_type` — Studio/1BR/2BR/3BR/Twin House/Villa/Commercial with area ranges and base price/sqm
- `dim_customer` — buyer_type (Local/Diaspora/Expat/Corporate Investor), is_investor
- `dim_channel` — Broker/Direct Sales/Digital Platform/Referral

### Healthcare / Hospital
- `dim_department` — department_id, name, type (Inpatient/Outpatient/Emergency)
- `dim_doctor` — doctor_id, name, specialty, department
- `dim_patient` — segment (Insured/Cash), age group, governorate
- `dim_service` — service_id, name, category, base cost

---

## 10. Realistic Egyptian context to use

### Governorates to use in dim_customer / dim_branch
Cairo, Giza, Alexandria, Luxor, Aswan, Mansoura, Tanta, Suez, Port Said, Asyut, Minya, Sohag, Fayoum, Beni Suef, Qena, Ismailia, Dakahlia, Gharbia, Dakahlia

### Regions
- Greater Cairo (Cairo + Giza)
- Alexandria
- Delta (Mansoura, Tanta, Damanhur, Dakahlia, Gharbia)
- Upper Egypt (Luxor, Aswan, Asyut, Minya, Sohag, Qena, Fayoum, Beni Suef)
- Canal Zone (Suez, Port Said, Ismailia)

### Pricing context (EGP, 2023–2024)
- Apply ~15–20% price increase from 2023 to 2024 to reflect EGP devaluation
- Egyptian banking interest rates: 10–22% p.a. depending on product
- Real estate: 20,000–40,000 EGP/sqm for premium Cairo compounds
- Insurance premiums: 200 EGP (travel) to 500,000 EGP (corporate risk)

### Synthetic names
Use `Faker("en_US")` for English names. Do not use `Faker("ar_EG")` for customer names — it produces inconsistent Arabic transliterations that confuse students.

### Digital channel adoption pattern (2023 → 2024)
In almost every Egyptian company dataset, model a shift toward digital channels:
- 2023: physical/offline channels ~60–70%, digital ~20–30%
- 2024: physical ~50–60%, digital ~30–40%

---

## 11. Complete workflow checklist

When assigned a new team, follow these steps in order:

- [ ] Read `inputs/<slug>/mail.md` (or `email.md`)
- [ ] Read `inputs/<slug>/*.pdf` if present
- [ ] Identify: company type, products/services, target dashboard user, KPIs requested, data fields requested
- [ ] Design schema: decide on fact table(s) and 3–5 dimensions
- [ ] Copy `generator_template.py` → `generate_<slug>.py`
- [ ] Fill in `PROJECT_SLUG`, `OUTPUT_BASE`, constants
- [ ] Write `gen_dim_*()` functions
- [ ] Write `gen_fact_*()` function(s) with realistic patterns
- [ ] Write `inject_issues()` following the standard recipe (Section 6)
- [ ] Write `validate()` — FK checks + null rate + dupe count
- [ ] Write all 4 instructor note strings + data dictionary string
- [ ] Write `main()` following the 5-step pattern
- [ ] Run the script: `source .venv/bin/activate && python generate_<slug>.py`
- [ ] Confirm: validation passes, row counts correct, no Python errors
- [ ] Spot-check one CSV to confirm cleaning issues are present

---

## 12. What NOT to do

- Do not hardcode hundreds of rows in lists — generate them programmatically
- Do not use real customer names, real phone numbers, or real IDs
- Do not claim the data is real
- Do not create a snowflake schema (nested dimensions)
- Do not make the dataset so dirty that it is frustrating — light-to-moderate only
- Do not skip the validation step
- Do not make all data uniformly random — patterns and correlations are required
- Do not add columns that have no business meaning just to increase size
- Do not make the main fact table exceed 3,000 rows (before duplicates)
- Do not forget to put `dim_date.date` as a string (not datetime) — this is always intentional

---

## 13. Reference: completed projects

Study these generators to understand the conventions before writing a new one:

| File | Industry | Fact Tables | Notable patterns |
|------|----------|-------------|-----------------|
| `generate_enr_t07.py` | Railway transport | `fact_ticket_sales` | Seasonality, train×route compatibility, class pricing by train type |
| `generate_dar_al_maaref.py` | Publishing | `fact_sales`, `fact_inventory` | B2B vs B2C quantities, back-to-school seasonality, inventory reorder alerts |
| `generate_banque_du_caire.py` | Banking | `fact_transactions`, `fact_loans` | Digital adoption shift 2023→2024, NPL rate, nullable branch_id for digital txns |
| `generate_misr_insurance.py` | Insurance | `fact_policies`, `fact_claims` | Loss ratio, seasonal claim patterns by product, claim cause per product |
| `generate_sodic.py` | Real estate | `fact_unit_sales`, `fact_project_progress` | Price/sqm inflation 2024, North Coast summer peak, channel shift to Sakneen |

---

## 14. Environment

```bash
# Always activate the virtual environment first
source .venv/bin/activate

# Dependencies (already installed)
# pandas, numpy, faker, openpyxl, pyarrow

# Run a generator
python generate_<slug>.py

# Output lands in
output/<slug>/student_dataset/      # CSVs
output/<slug>/data_dictionary.md
output/<slug>/private_instructor_notes/
```

Python version: 3.x (any modern version ≥ 3.9)  
All generators use only stdlib + pandas + numpy + faker.

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

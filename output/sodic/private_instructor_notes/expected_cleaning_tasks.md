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

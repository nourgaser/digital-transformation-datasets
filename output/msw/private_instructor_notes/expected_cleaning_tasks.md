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

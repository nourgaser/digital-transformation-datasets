# Expected Cleaning Tasks — Dar Al Maaref

## fact_sales.csv

| # | Issue | Column | Approx. Rate |
|---|-------|--------|--------------|
| 1 | Missing values | `discount_pct` | ~5% nulls |
| 2 | Missing values | `processing_days` | ~4% nulls |
| 3 | Inconsistent casing | `order_status` | ~3% stored as uppercase ("DELIVERED") |
| 4 | Mixed data type | `total_revenue` | ~3% stored as text strings |
| 5 | Leading whitespace | `channel_id` | ~2% have a leading space — causes FK lookup failure |
| 6 | Impossible values | `processing_days` | 3 rows with negative values |
| 7 | Duplicate rows | all columns | ~1.5% fully duplicated records |

## dim_book.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 8 | Inconsistent casing | `category` | "novel" (lowercase) for B011, B012, B013 — should be "Novel" |

## dim_customer.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 9 | Trailing whitespace | `customer_type` | 5 rows with trailing space — causes group-by errors |

## dim_date.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 10 | Date stored as string | `date` | Column is text "YYYY-MM-DD" — must be converted to Date type in Power Query |

## Notes for Instructor
- The whitespace in `channel_id` (fact) is the trickiest: a simple relationship in Power BI will silently fail for those rows, producing blanks. Students must use Trim in Power Query.
- Negative `processing_days` are subtle — students need to filter or flag these as data quality issues.
- Category casing in dim_book affects pie/bar charts (two "Novel" slices appear).

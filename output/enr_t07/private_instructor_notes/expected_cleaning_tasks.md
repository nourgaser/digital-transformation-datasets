# Expected Cleaning Tasks — ENR T07

## fact_ticket_sales.csv

| # | Issue | Column | Approx. Rate |
|---|-------|--------|--------------|
| 1 | Missing values | `discount_pct` | ~5% nulls |
| 2 | Missing values | `payment_method` | ~4% nulls |
| 3 | Inconsistent casing | `ticket_class` | ~3% stored as lowercase ("first", "second") |
| 4 | Leading/trailing whitespace | `booking_status` | ~2% |
| 5 | Mixed data type | `total_revenue` | ~3% stored as text strings instead of numeric |
| 6 | Negative impossible values | `ticket_price` | 4 rows with negative prices |
| 7 | Duplicate rows | all columns | ~1.5% fully duplicated records |

## dim_route.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 8 | Inconsistent casing | `region` | "canal zone" (lowercase) for R04, R05 — should be "Canal Zone" |

## dim_train.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 9 | Leading whitespace | `train_type` | " Standard" (space before) for T08, T09 |

## dim_date.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 10 | Date stored as string | `date` | Column is text "YYYY-MM-DD", not a Date type — students must convert in Power Query |

## Notes for Instructor
- `total_revenue` type mismatch (string vs number) is the trickiest issue — students must use "Replace Errors" or "Change Type" in Power Query.
- Negative `ticket_price` values look subtle — students should catch them with a Min check or a filter visual.
- Duplicate rows have no `sale_id` collision — they are exact row duplicates, so students must use "Remove Duplicates" on all columns.

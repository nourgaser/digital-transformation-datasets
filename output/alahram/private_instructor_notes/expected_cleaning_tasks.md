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

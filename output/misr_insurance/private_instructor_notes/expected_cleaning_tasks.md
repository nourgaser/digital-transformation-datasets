# Expected Cleaning Tasks — Misr Insurance Company

## fact_policies.csv

| # | Issue | Column | Approx. Rate |
|---|-------|--------|--------------|
| 1 | Missing values | `admin_cost` | ~5% nulls |
| 2 | Missing values | `term_months` | ~4% nulls |
| 3 | Inconsistent casing | `policy_status` | ~3% uppercase ("ACTIVE", "EXPIRED") |
| 4 | Mixed data type | `premium_egp` | ~3% stored as text strings |
| 5 | Impossible negative values | `premium_egp` | 3 rows with negative premiums |
| 6 | Duplicate rows | all columns | ~1.5% fully duplicated records |

## fact_claims.csv

| # | Issue | Column | Approx. Rate |
|---|-------|--------|--------------|
| 7 | Missing values | `processing_days` | ~5% nulls |
| 8 | Inconsistent casing | `claim_status` | ~3% lowercase ("approved", "rejected") |
| 9 | Leading whitespace | `claim_cause` | ~2% with leading space |
| 10 | Impossible negative values | `processing_days` | 3 rows with negative values |

## dim_customer.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 11 | Inconsistent casing | `customer_type` | 4 rows lowercase ("individual", "corporate") |

## dim_product.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 12 | Inconsistent casing | `product_category` | "travel" (lowercase) for PR07, PR08 |

## dim_branch.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 13 | Trailing whitespace | `region` | "Upper Egypt " (trailing space) for BR07, BR08, BR11 |

## dim_date.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 14 | Date stored as string | `date` | Text "YYYY-MM-DD" — must be converted to Date type in Power Query |

## Notes for Instructor
- Negative `premium_egp` combined with text-type rows in the same column is a compound type issue — students must handle "Change Type" errors before filtering negatives.
- `claim_cause` whitespace causes grouping issues on the Claims by Cause chart — a very realistic, practical cleaning lesson.
- The `policy_status` uppercase issue will silently skew Active vs Cancelled ratios if uncleaned.
- Loss Ratio (claims paid / premium) is a key derived metric — it only works correctly after both fact tables are cleaned.

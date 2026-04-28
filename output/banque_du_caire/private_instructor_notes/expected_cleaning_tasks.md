# Expected Cleaning Tasks — Banque du Caire

## fact_transactions.csv

| # | Issue | Column | Approx. Rate |
|---|-------|--------|--------------|
| 1 | Missing values (intentional: digital txns have no branch) | `branch_id` | ~30% null (mix of intentional + injected) |
| 2 | Missing values | `fee_egp` | ~4% nulls |
| 3 | Inconsistent casing | `transaction_type` | ~3% lowercase ("deposit", "withdrawal") |
| 4 | Mixed data type | `amount_egp` | ~3% stored as text strings |
| 5 | Negative impossible values | `amount_egp` | 4 rows with negative amounts |
| 6 | Duplicate rows | all columns | ~1.5% fully duplicated records |

## fact_loans.csv

| # | Issue | Column | Approx. Rate |
|---|-------|--------|--------------|
| 7 | Missing values | `interest_rate` | ~5% nulls |
| 8 | Inconsistent casing | `risk_level` | ~3% uppercase ("HIGH", "MEDIUM") |
| 9 | Leading whitespace | `loan_status` | ~2% with leading space |

## dim_customer.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 10 | Inconsistent casing | `segment` | 4 rows lowercase ("retail", "premium") |

## dim_branch.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 11 | Trailing whitespace | `branch_tier` | "Tier 3 " (trailing space) for BR11, BR12, BR13 |

## dim_date.csv

| # | Issue | Column | Detail |
|---|-------|--------|--------|
| 12 | Date stored as string | `date` | Text "YYYY-MM-DD" — must be converted to Date type in Power Query |

## Notes for Instructor
- `branch_id` nulls in fact_transactions are **intentional** for digital channels (no physical branch). Students must understand this is NOT an error for digital rows, but IS an error for the extra injected nulls on physical rows. A good student will filter by `is_digital` before investigating nulls.
- Negative `amount_egp` combined with text-type `amount_egp` in the same column is a compound issue — students must fix the type first, then filter the negatives.
- The loan NPL rate is ~15%, which is realistic for an Egyptian bank and enables meaningful risk analysis.

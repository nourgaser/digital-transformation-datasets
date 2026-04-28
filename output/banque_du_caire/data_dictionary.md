# Data Dictionary — Banque du Caire
## Digital Transformation Course · BINF 402 · GIU · Spring 2026

---

## Business Story
Banque du Caire is an Egyptian commercial bank offering retail, SME, and corporate banking services.
This dataset covers **banking transactions** and **loan applications** for 2023–2024 across 15 branches nationwide.
Your goal as management is to monitor financial performance, assess loan risk, and track the bank's shift toward digital channels.

---

## Files

### `fact_transactions.csv` (main fact table)
| Column | Description |
|--------|-------------|
| `transaction_id` | Unique transaction identifier |
| `date_id` | Foreign key → `dim_date.date_id` |
| `customer_id` | Foreign key → `dim_customer.customer_id` |
| `branch_id` | Foreign key → `dim_branch.branch_id` (null for digital channels) |
| `channel_id` | Foreign key → `dim_channel.channel_id` |
| `transaction_type` | Type: Deposit, Withdrawal, Transfer, Loan Payment, etc. |
| `amount_egp` | Transaction value (EGP) |
| `fee_egp` | Fee charged for the transaction (EGP) |
| `customer_segment` | Customer segment at time of transaction |
| `is_digital` | True if transaction was through a digital channel |

### `fact_loans.csv` (secondary fact table)
| Column | Description |
|--------|-------------|
| `loan_id` | Unique loan identifier |
| `date_id` | Foreign key → `dim_date.date_id` (application date) |
| `customer_id` | Foreign key → `dim_customer.customer_id` |
| `branch_id` | Foreign key → `dim_branch.branch_id` |
| `product_id` | Foreign key → `dim_product.product_id` |
| `principal_egp` | Loan principal amount (EGP) |
| `interest_rate` | Annual interest rate (decimal, e.g. 0.14 = 14%) |
| `term_months` | Loan duration in months |
| `monthly_payment` | Calculated monthly installment (EGP) |
| `risk_level` | Risk assessment: Low, Medium, or High |
| `loan_status` | Approved, Rejected, Pending, Defaulted, or Closed |
| `is_npl` | True if loan is Non-Performing (Defaulted) |
| `customer_segment` | Customer segment |

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

### `dim_branch.csv`
| Column | Description |
|--------|-------------|
| `branch_id` | Primary key |
| `branch_name` | Branch name/area |
| `governorate` | Governorate location |
| `region` | Broader region (Greater Cairo, Alexandria, Delta, etc.) |
| `branch_tier` | Tier 1 (high volume), Tier 2, or Tier 3 |

### `dim_customer.csv`
| Column | Description |
|--------|-------------|
| `customer_id` | Primary key |
| `customer_name` | Synthetic customer name |
| `segment` | Retail, Premium, SME, or Corporate |
| `age` | Age (individuals only; blank for companies) |
| `gender` | Gender (individuals only) |
| `governorate` | Customer's governorate |
| `home_branch_id` | Primary branch |
| `digital_enrolled` | Whether customer is enrolled in digital banking |
| `since_year` | Year customer joined the bank |

### `dim_channel.csv`
| Column | Description |
|--------|-------------|
| `channel_id` | Primary key |
| `channel_name` | In-Branch, ATM, Mobile App, Internet Banking, Call Center |
| `channel_type` | Physical or Digital |

### `dim_product.csv`
| Column | Description |
|--------|-------------|
| `product_id` | Primary key |
| `product_name` | Product name |
| `product_type` | Loan, Credit Card, Deposit, Digital, Trade Finance |
| `target_segment` | Primary target customer segment |

---

## Intended Relationships
- `fact_transactions` → `dim_date`, `dim_branch`, `dim_customer`, `dim_channel`
- `fact_loans` → `dim_date`, `dim_branch`, `dim_customer`, `dim_product`

## Notes for Students
- `branch_id` is intentionally null for digital transactions — this is not always an error.
- Clean data types before building relationships (especially `amount_egp` and `date`).
- Both fact tables share `dim_date`, `dim_branch`, and `dim_customer` — connect each separately.

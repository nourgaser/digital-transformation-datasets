# Data Dictionary — Misr Insurance Company
## Digital Transformation Course · BINF 402 · GIU · Spring 2026

---

## Business Story
Misr Insurance Company is one of Egypt's leading non-life (general) insurance providers.
This dataset covers **insurance policies sold** and **claims filed** during 2023–2024.
Products include Motor, Property, Marine, Travel, Engineering, and Corporate Risk insurance.
Your goal as management is to track premium revenue, assess claims risk, and improve operational efficiency.

---

## Files

### `fact_policies.csv` (main fact table)
| Column | Description |
|--------|-------------|
| `policy_id` | Unique policy identifier |
| `date_id` | Foreign key → `dim_date.date_id` (policy issue date) |
| `customer_id` | Foreign key → `dim_customer.customer_id` |
| `product_id` | Foreign key → `dim_product.product_id` |
| `branch_id` | Foreign key → `dim_branch.branch_id` |
| `channel_id` | Foreign key → `dim_channel.channel_id` |
| `premium_egp` | Policy premium charged (EGP) |
| `underwriting_cost` | Cost to assess and underwrite the risk (EGP) |
| `admin_cost` | Administrative cost (EGP) |
| `total_cost` | Total cost (underwriting + admin) |
| `expected_claim_reserve` | Estimated reserve set aside for potential claims (EGP) |
| `term_months` | Policy duration in months |
| `policy_status` | Active, Expired, or Cancelled |
| `customer_type` | Individual or Corporate |
| `is_returning_customer` | Whether customer had a prior policy |

### `fact_claims.csv` (secondary fact table)
| Column | Description |
|--------|-------------|
| `claim_id` | Unique claim identifier |
| `date_id` | Foreign key → `dim_date.date_id` (claim filing date) |
| `policy_id` | Reference to the related policy |
| `customer_id` | Foreign key → `dim_customer.customer_id` |
| `branch_id` | Foreign key → `dim_branch.branch_id` |
| `product_id` | Foreign key → `dim_product.product_id` |
| `claim_amount_egp` | Amount claimed by the customer (EGP) |
| `amount_paid_egp` | Amount actually paid out (EGP; 0 if not approved) |
| `claim_status` | Approved, Rejected, Pending, or Under Review |
| `claim_cause` | Reason for the claim (e.g. Accident, Fire, Theft) |
| `processing_days` | Days taken to process the claim |
| `product_category` | Insurance category for quick filtering |

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

### `dim_product.csv`
| Column | Description |
|--------|-------------|
| `product_id` | Primary key |
| `product_name` | Product name |
| `product_category` | Motor, Property, Marine, Travel, Engineering, Corporate Risk |
| `customer_type` | Primary target: Individual or Corporate |
| `premium_min_egp` | Typical minimum premium |
| `premium_max_egp` | Typical maximum premium |
| `expected_loss_ratio` | Historical expected claims-to-premium ratio |

### `dim_branch.csv`
| Column | Description |
|--------|-------------|
| `branch_id` | Primary key |
| `branch_name` | Branch name |
| `governorate` | Governorate |
| `region` | Region (Greater Cairo, Alexandria, Delta, Upper Egypt, Canal Zone) |

### `dim_customer.csv`
| Column | Description |
|--------|-------------|
| `customer_id` | Primary key |
| `customer_name` | Synthetic name |
| `customer_type` | Individual or Corporate |
| `age` | Age (individuals only) |
| `gender` | Gender (individuals only) |
| `governorate` | Customer's governorate |
| `region` | Region |
| `home_branch_id` | Primary branch |
| `is_returning` | Whether customer is a returning policyholder |

### `dim_channel.csv`
| Column | Description |
|--------|-------------|
| `channel_id` | Primary key |
| `channel_name` | Branch, Agent, Broker, Online, Call Center |
| `channel_type` | Offline or Digital |

---

## Intended Relationships
- `fact_policies` → `dim_date`, `dim_customer`, `dim_product`, `dim_branch`, `dim_channel`
- `fact_claims` → `dim_date`, `dim_customer`, `dim_product`, `dim_branch`

## Notes for Students
- Clean data types and fix inconsistencies **before** building relationships.
- The **Loss Ratio** (claims paid ÷ premium) is the most important insurance KPI — it spans both fact tables.
- Seasonal patterns exist: Motor claims peak in winter; Travel policies peak in summer.
- Do not create a direct relationship between the two fact tables — connect them through shared dimensions only.

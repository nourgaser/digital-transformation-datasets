# Data Dictionary — SODIC
## Digital Transformation Course · BINF 402 · GIU · Spring 2026

---

## Business Story
SODIC (Sixth of October Development and Investment Company) is one of Egypt's leading real estate developers, operating across West Cairo, East Cairo, and North Coast communities.
This dataset covers **property unit sales contracts** and **monthly project construction progress** for 2023–2024.
Your goal as management is to track sales performance, monitor project delivery, analyse channel effectiveness, and understand buyer behaviour.

---

## Files

### `fact_unit_sales.csv` (main fact table)
| Column | Description |
|--------|-------------|
| `sale_id` | Unique contract identifier |
| `date_id` | Foreign key → `dim_date.date_id` (contract date) |
| `project_id` | Foreign key → `dim_project.project_id` |
| `unit_type_id` | Foreign key → `dim_unit_type.unit_type_id` |
| `customer_id` | Foreign key → `dim_customer.customer_id` |
| `channel_id` | Foreign key → `dim_channel.channel_id` |
| `area_sqm` | Unit size in square meters |
| `price_per_sqm` | Selling price per sqm (EGP) |
| `contract_value` | Total contract value (EGP) |
| `down_payment` | Initial down payment amount (EGP) |
| `remaining_balance` | Remaining installment balance (EGP) |
| `down_payment_pct` | Down payment as % of contract value |
| `payment_plan` | Installment plan selected (e.g. 7-Year Installment) |
| `commission_pct` | Broker/referral commission rate |
| `commission_amount` | Total commission paid (EGP) |
| `contract_status` | Signed, Under Review, or Cancelled |
| `is_investor_buyer` | True if buyer is purchasing for investment |

### `fact_project_progress.csv` (secondary fact table)
| Column | Description |
|--------|-------------|
| `progress_id` | Unique snapshot identifier |
| `date_id` | Foreign key → `dim_date.date_id` (month start) |
| `project_id` | Foreign key → `dim_project.project_id` |
| `completion_pct` | % of construction completed at month end |
| `budget_total_mEGP` | Total approved project budget (millions EGP) |
| `budget_spent_mEGP` | Cumulative spend to date (millions EGP) |
| `cost_overrun_pct` | % difference between spend and completion |
| `units_completed` | Number of units fully delivered |
| `units_under_construction` | Units currently being built |
| `delivery_status` | On Track, Delivered, or Early Stage |
| `is_ahead_of_schedule` | True if progressing ahead of plan |

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

### `dim_project.csv`
| Column | Description |
|--------|-------------|
| `project_id` | Primary key |
| `project_name` | Community/compound name |
| `location` | West Cairo / East Cairo / North Coast |
| `sub_area` | More specific area |
| `project_type` | Residential, Mixed-Use, Resort, Commercial |
| `launch_year` | Year project was launched |
| `total_units` | Total number of units in the development |
| `target_delivery_year` | Planned delivery completion year |

### `dim_unit_type.csv`
| Column | Description |
|--------|-------------|
| `unit_type_id` | Primary key |
| `unit_type` | Studio, Apartment 1BR, Twin House, Villa, etc. |
| `min_area_sqm` | Minimum unit size |
| `max_area_sqm` | Maximum unit size |
| `bedrooms` | Number of bedrooms |
| `base_price_per_sqm` | Reference base price per sqm (EGP) |

### `dim_customer.csv`
| Column | Description |
|--------|-------------|
| `customer_id` | Primary key |
| `customer_name` | Synthetic buyer name |
| `buyer_type` | Egyptian Local, Egyptian Diaspora, Arab Expat, Corporate Investor |
| `nationality` | Nationality |
| `governorate` | Buyer's location (or Overseas/Gulf) |
| `age` | Age (individuals only) |
| `gender` | Gender (individuals only) |
| `is_investor` | True if purchasing for investment purposes |

### `dim_channel.csv`
| Column | Description |
|--------|-------------|
| `channel_id` | Primary key |
| `channel_name` | Broker, Direct Sales, Sakneen Digital, Corporate/B2B, Referral |
| `channel_type` | Offline or Online |

---

## Intended Relationships
- `fact_unit_sales` → `dim_date`, `dim_project`, `dim_unit_type`, `dim_customer`, `dim_channel`
- `fact_project_progress` → `dim_date`, `dim_project`

## Notes for Students
- `contract_value` must be converted to a numeric type before any SUM measure will work.
- The digital channel (Sakneen) shows growing share from 2023 to 2024 — this is a key insight to surface.
- North Coast projects (Ogami, Caesar) follow a summer seasonality pattern — look at monthly breakdowns.
- SODIC's 91% ahead-of-schedule delivery record is reflected in the `is_ahead_of_schedule` column.

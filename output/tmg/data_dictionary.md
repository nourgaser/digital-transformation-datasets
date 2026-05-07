# Data Dictionary — Talaat Moustafa Group (TMG)
## Digital Transformation Course · BINF 402 · GIU · Spring 2026

---

## Business Story
Talaat Moustafa Group (TMG) is one of Egypt's largest real estate developers, known for integrated cities like **Madinaty**, **Al Rehab**, and the upcoming **Noor City**. Beyond property sales, TMG operates Four Seasons hotels and runs **TMG Life**, a mobile app that handles community services for over a million residents — utility payments, maintenance, security access, and recreation bookings.

This dataset covers two areas for 2023–2024:
1. **Property unit sales** — contracts across TMG's projects
2. **Community service activity** — residents' use of the TMG Life app

Your goal as management is to track sales performance across projects, monitor the shift to digital channels, measure off-plan financing impact, and evaluate resident engagement and satisfaction with community services.

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
| `down_payment` | Initial down payment (EGP) |
| `remaining_balance` | Remaining installment balance (EGP) |
| `down_payment_pct` | Down payment as % of contract value |
| `payment_plan` | Off-Plan 8-Year, Off-Plan 10-Year, 5-Year Installment, or Cash |
| `is_off_plan` | True if contract uses off-plan financing |
| `commission_pct` | Broker/referral commission rate |
| `commission_amount` | Total commission paid (EGP) |
| `contract_status` | Signed, Under Review, or Cancelled |

### `fact_community_services.csv` (secondary fact table)
| Column | Description |
|--------|-------------|
| `service_log_id` | Unique service activity identifier |
| `date_id` | Foreign key → `dim_date.date_id` |
| `customer_id` | Foreign key → `dim_customer.customer_id` |
| `project_id` | Foreign key → `dim_project.project_id` |
| `service_type_id` | Foreign key → `dim_service_type.service_type_id` |
| `amount_paid_egp` | Amount paid via the app (EGP); 0 for non-payment services |
| `service_status` | Completed, Pending, Cancelled, or Failed |
| `rating` | Customer rating (1–5); only for completed services |
| `resolution_hours` | Hours to resolve the request (Maintenance, Concierge, Security only) |
| `via_app` | Always True — this fact tracks app activity |

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
| `project_name` | Project name (Madinaty, Al Rehab, Noor City, Four Seasons hotels, etc.) |
| `location` | Greater Cairo, East Cairo, Alexandria, South Sinai |
| `sub_area` | Specific sub-area |
| `project_type` | Integrated City, Residential, Smart City, Commercial, Hospitality |
| `launch_year` | Year project was launched |
| `total_units` | Total number of units |
| `delivery_status` | Delivered, Delivered+Ongoing, Under Construction, Early Stage |

### `dim_unit_type.csv`
| Column | Description |
|--------|-------------|
| `unit_type_id` | Primary key |
| `unit_type` | Studio, Apartment 1BR/2BR/3BR, Penthouse, Twin House, Villa, Hotel Suite |
| `min_area_sqm` / `max_area_sqm` | Size range |
| `bedrooms` | Number of bedrooms |
| `base_price_per_sqm` | Reference base price (EGP) |

### `dim_customer.csv`
| Column | Description |
|--------|-------------|
| `customer_id` | Primary key |
| `customer_name` | Synthetic buyer name |
| `buyer_type` | Egyptian Local, Egyptian Diaspora, Arab Investor, Foreign Investor |
| `nationality` | Nationality category |
| `governorate` | Buyer's location (or country if abroad) |
| `age` | Age |
| `gender` | Gender |
| `is_resident` | True if buyer lives in a TMG community |
| `tmg_life_user` | True if user is registered on the TMG Life app |
| `registered_year` | Year customer registered |

### `dim_channel.csv`
| Column | Description |
|--------|-------------|
| `channel_id` | Primary key |
| `channel_name` | TMG Sales Center, Broker, TMG Website, TMG Life App, Referral |
| `channel_type` | Direct, Indirect, or Digital |

### `dim_service_type.csv`
| Column | Description |
|--------|-------------|
| `service_type_id` | Primary key |
| `service_name` | Specific service (Electricity Payment, Maintenance Request, etc.) |
| `service_category` | Utility, Maintenance, Security, Recreation, Concierge, Transport |
| `avg_amount_egp` | Reference average amount for paid services |
| `is_payment` | True if service involves a payment |

---

## Intended Relationships
- `fact_unit_sales` → `dim_date`, `dim_project`, `dim_unit_type`, `dim_customer`, `dim_channel`
- `fact_community_services` → `dim_date`, `dim_customer`, `dim_project`, `dim_service_type`

## Notes for Students
- Clean data types and fix inconsistencies **before** building relationships in Power BI.
- TMG's **Off-Plan financing** is a strategic differentiator — use the `is_off_plan` column to measure its share of revenue.
- The **TMG Life app** activity (fact_community_services) reflects resident engagement — this is a unique TMG digital transformation outcome.
- 2024 prices are higher than 2023 due to EGP devaluation — surface this in average price/sqm comparisons.
- The two fact tables share dimensions but are not directly connected — use shared dimensions for cross-table analysis.

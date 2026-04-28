# Data Dictionary — Egyptian National Railways (ENR)
## Digital Transformation Course · BINF 402 · GIU · Spring 2026

---

## Business Story
This dataset represents **ticket sales transactions** for Egyptian National Railways (ENR) over 2023–2024.
The data covers passenger journeys across key Egyptian routes, split by train type, ticket class, and booking channel.
Your goal as a Sales Manager is to understand revenue trends, identify high-performing routes and channels, and track occupancy.

---

## Files

### `fact_ticket_sales.csv` (main fact table)
| Column | Description |
|--------|-------------|
| `sale_id` | Unique transaction identifier |
| `date_id` | Foreign key → `dim_date.date_id` (format: YYYYMMDD) |
| `route_id` | Foreign key → `dim_route.route_id` |
| `train_id` | Foreign key → `dim_train.train_id` |
| `channel_id` | Foreign key → `dim_channel.channel_id` |
| `ticket_class` | Class of service: First, Second, or Third |
| `tickets_sold` | Number of tickets in this transaction |
| `ticket_price` | Price per single ticket (EGP) |
| `discount_pct` | Discount percentage applied (0–20%) |
| `discount_amount` | Total discount value (EGP) |
| `total_revenue` | Net revenue for this transaction (EGP) |
| `payment_method` | Payment method used |
| `booking_status` | Completed or Cancelled |

### `dim_date.csv`
| Column | Description |
|--------|-------------|
| `date_id` | Primary key (YYYYMMDD) |
| `date` | Full date string (YYYY-MM-DD) |
| `day` | Day of month |
| `month` | Month number |
| `month_name` | Month name |
| `quarter` | Quarter (1–4) |
| `year` | Year |
| `day_of_week` | Weekday name |
| `is_weekend` | True if Friday or Saturday |
| `is_holiday` | True if Egyptian public holiday |

### `dim_route.csv`
| Column | Description |
|--------|-------------|
| `route_id` | Primary key |
| `origin_city` | Departure city |
| `destination_city` | Arrival city |
| `distance_km` | Route distance in kilometers |
| `region` | Geographic region served |
| `is_express` | Whether the route has express service |
| `estimated_duration_hrs` | Approximate travel time |

### `dim_train.csv`
| Column | Description |
|--------|-------------|
| `train_id` | Primary key |
| `train_name` | Train service name |
| `train_type` | Type: Spanish Express, Talgo, Air-Conditioned, Standard |
| `first_class_capacity` | Number of First Class seats |
| `second_class_capacity` | Number of Second Class seats |
| `third_class_capacity` | Number of Third Class seats |
| `total_capacity` | Total seats across all classes |

### `dim_channel.csv`
| Column | Description |
|--------|-------------|
| `channel_id` | Primary key |
| `channel_name` | Specific channel (e.g. Website, Fawry) |
| `channel_category` | Online or Offline |

---

## Intended Relationships
- `fact_ticket_sales.date_id` → `dim_date.date_id`
- `fact_ticket_sales.route_id` → `dim_route.route_id`
- `fact_ticket_sales.train_id` → `dim_train.train_id`
- `fact_ticket_sales.channel_id` → `dim_channel.channel_id`

## Notes for Students
- The data **requires cleaning** before analysis — check for inconsistencies, wrong types, and missing values.
- Build a **star schema** in Power BI with `fact_ticket_sales` at the center.
- Use the date table for **time intelligence** measures (MoM, YTD, YoY).

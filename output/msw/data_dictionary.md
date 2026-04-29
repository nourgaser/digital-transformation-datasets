# Data Dictionary — Misr Spinning and Weaving Company (MSW)
## Digital Transformation Course · BINF 402 · GIU · Spring 2026

---

## Business Story
Misr Spinning and Weaving Company (MSW), founded in 1927 in El Mahalla El Kubra, Egypt, is one of the largest textile manufacturers in the Middle East and Africa. The company specialises in spinning, weaving, and garment production using high-quality Egyptian cotton.

This dataset covers **product sales orders** and **monthly production line performance** for 2023–2024 — a period when MSW undertook major digital transformation: implementing ERP systems, automating production lines, adopting CRM tools, and expanding its digital sales presence. Your goal as management is to track sales performance by product and customer segment, monitor export vs domestic revenue trends, measure production efficiency across factory departments, and identify quality improvement opportunities.

---

## Files

### `fact_sales.csv` (main fact table)
| Column | Description |
|--------|-------------|
| `sale_id` | Unique order identifier |
| `date_id` | Foreign key → `dim_date.date_id` (order date) |
| `product_id` | Foreign key → `dim_product.product_id` |
| `customer_id` | Foreign key → `dim_customer.customer_id` |
| `channel_id` | Foreign key → `dim_channel.channel_id` |
| `quantity` | Quantity ordered (units depend on product — kg, meter, or piece) |
| `unit_price_egp` | Price per unit (EGP) |
| `discount_pct` | Discount applied (decimal, e.g. 0.10 = 10%) |
| `total_revenue_egp` | Net revenue after discount (EGP) |
| `order_status` | Completed, Pending, Cancelled, or Returned |
| `market` | Domestic or Export |

### `fact_production.csv` (secondary fact table)
| Column | Description |
|--------|-------------|
| `production_id` | Unique snapshot identifier |
| `date_id` | Foreign key → `dim_date.date_id` (first day of month) |
| `line_id` | Foreign key → `dim_production_line.line_id` |
| `working_days` | Number of working days in the month |
| `planned_output_kg` | Target output for the month (kg) |
| `actual_output_kg` | Actual production achieved (kg) |
| `efficiency_pct` | Actual as % of planned output |
| `defect_qty_kg` | Quantity rejected due to quality defects (kg) |
| `defect_rate_pct` | Defect quantity as % of actual output |
| `downtime_hours` | Unplanned machine downtime (hours) |
| `production_status` | Normal, Under Maintenance, or At Capacity |

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
| `product_name` | Full product name |
| `category` | Yarn, Grey Fabric, Finished Fabric, or Garment |
| `fiber_type` | 100% Egyptian Cotton or Cotton Blend |
| `unit_of_measure` | kg, meter, or piece |
| `base_price_egp` | Reference base price per unit (EGP) |

### `dim_customer.csv`
| Column | Description |
|--------|-------------|
| `customer_id` | Primary key |
| `customer_name` | Synthetic customer name |
| `customer_type` | Local Retailer, Garment Manufacturer, Wholesaler, Government/Military, or Export Buyer |
| `market` | Domestic or Export |
| `country` | Egypt (domestic) or export destination |
| `governorate` | Egyptian governorate (domestic customers only) |

### `dim_channel.csv`
| Column | Description |
|--------|-------------|
| `channel_id` | Primary key |
| `channel_name` | Direct Sales, Distributor, Export Agent, Government Tender, E-commerce, Trade Fair |
| `channel_type` | Domestic or International |

### `dim_production_line.csv`
| Column | Description |
|--------|-------------|
| `line_id` | Primary key |
| `line_name` | Factory line or hall name |
| `department` | Spinning, Weaving, Finishing, or Garment |
| `production_type` | Specific machinery type (e.g. Rapier Loom, Dyeing) |
| `capacity_kg_per_day` | Rated daily capacity (kg) |
| `operational_status` | Active or Partial |
| `location` | All lines located in El Mahalla El Kubra |

---

## Intended Relationships
- `fact_sales` → `dim_date`, `dim_product`, `dim_customer`, `dim_channel`
- `fact_production` → `dim_date`, `dim_production_line`

## Notes for Students
- `total_revenue_egp` must be converted to a numeric type before any SUM or AVERAGE measure will work.
- The `market` column (Domestic / Export) is useful for comparing revenue streams without a join.
- Unit prices in 2024 reflect the impact of EGP currency fluctuations — year-over-year price comparisons are meaningful.
- `fact_production` records are monthly snapshots per production line — connect to both `dim_date` and `dim_production_line` to analyse factory efficiency.
- Clean all data in Power Query before building any measures or visuals.

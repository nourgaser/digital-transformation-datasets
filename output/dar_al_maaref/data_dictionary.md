# Data Dictionary — Dar Al Maaref
## Digital Transformation Course · BINF 402 · GIU · Spring 2026

---

## Business Story
Dar Al Maaref is an Egyptian publishing and printing company selling educational books, academic titles, novels, and reference works.
This dataset covers **book sales orders** and **monthly inventory snapshots** for 2023–2024.
Customers include individual buyers, schools, libraries, and distributors.
Your goal as a manager is to track sales performance, profitability, inventory levels, and channel efficiency.

---

## Files

### `fact_sales.csv` (main fact table)
| Column | Description |
|--------|-------------|
| `sale_id` | Unique order identifier |
| `date_id` | Foreign key → `dim_date.date_id` |
| `book_id` | Foreign key → `dim_book.book_id` |
| `customer_id` | Foreign key → `dim_customer.customer_id` |
| `channel_id` | Foreign key → `dim_channel.channel_id` |
| `quantity` | Number of copies ordered |
| `unit_price_egp` | Actual selling price per copy (EGP) |
| `discount_pct` | Discount percentage applied |
| `discount_amount` | Total discount value (EGP) |
| `total_revenue` | Net revenue for the order (EGP) |
| `total_cost` | Total production/procurement cost (EGP) |
| `profit` | Revenue minus cost (EGP) |
| `order_status` | Delivered, Returned, or Pending |
| `processing_days` | Days from order to delivery |

### `fact_inventory.csv` (secondary fact table)
| Column | Description |
|--------|-------------|
| `inventory_id` | Unique snapshot identifier |
| `date_id` | Foreign key → `dim_date.date_id` (month start) |
| `book_id` | Foreign key → `dim_book.book_id` |
| `opening_stock` | Units at start of month |
| `units_received` | Units restocked during the month |
| `units_sold` | Units sold/dispatched during the month |
| `closing_stock` | Units remaining at end of month |
| `reorder_point` | Minimum stock threshold before reorder |
| `below_reorder` | True if closing stock < reorder point |

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

### `dim_book.csv`
| Column | Description |
|--------|-------------|
| `book_id` | Primary key |
| `title` | Book title |
| `category` | Educational, Academic, Novel, or Reference |
| `author` | Author name |
| `list_price_egp` | Standard retail price (EGP) |
| `unit_cost_egp` | Production cost per copy (EGP) |
| `published_year` | Year of publication |
| `is_bestseller` | Whether book is a top seller |
| `isbn` | Synthetic ISBN identifier |

### `dim_customer.csv`
| Column | Description |
|--------|-------------|
| `customer_id` | Primary key |
| `customer_name` | Customer or institution name |
| `customer_type` | Individual, School, Library, or Distributor |
| `governorate` | Egyptian governorate |
| `region` | Broader region (e.g., Upper Egypt, Delta) |

### `dim_channel.csv`
| Column | Description |
|--------|-------------|
| `channel_id` | Primary key |
| `channel_name` | Channel (Online Store, Retail Bookstore, etc.) |
| `channel_type` | Direct - B2C or B2B |

---

## Intended Relationships
- `fact_sales.date_id` → `dim_date.date_id`
- `fact_sales.book_id` → `dim_book.book_id`
- `fact_sales.customer_id` → `dim_customer.customer_id`
- `fact_sales.channel_id` → `dim_channel.channel_id`
- `fact_inventory.date_id` → `dim_date.date_id`
- `fact_inventory.book_id` → `dim_book.book_id`

## Notes for Students
- The dataset **requires cleaning** before analysis — look for type issues, missing values, and inconsistencies.
- Build a **star schema** in Power BI with both fact tables connected through shared dimensions.
- Mark `dim_date` as your Date Table for time intelligence.
- Back-to-school months (August–September) should show clear seasonal patterns in the data.

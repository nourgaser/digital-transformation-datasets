# Star Schema Relationships — MSW

## Tables
- **fact_sales** — main fact: product sales orders (~2,000+ rows)
- **fact_production** — secondary fact: monthly production line snapshots (~360 rows)
- **dim_date** — date dimension (shared by both fact tables)
- **dim_product** — product catalog (sales only)
- **dim_customer** — buyer dimension (sales only)
- **dim_channel** — sales channel (sales only)
- **dim_production_line** — factory lines (production only)

## Relationships

### fact_sales
| Fact Column | → | Dimension | PK | Cardinality | Filter |
|-------------|---|-----------|----|-------------|--------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single |
| `product_id` | → | `dim_product` | `product_id` | Many-to-One | Single |
| `customer_id` | → | `dim_customer` | `customer_id` | Many-to-One | Single |
| `channel_id` | → | `dim_channel` | `channel_id` | Many-to-One | Single |

### fact_production
| Fact Column | → | Dimension | PK | Cardinality | Filter |
|-------------|---|-----------|----|-------------|--------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single |
| `line_id` | → | `dim_production_line` | `line_id` | Many-to-One | Single |

## Notes
- Both fact tables share `dim_date` — Power BI handles this correctly with separate relationships.
- `dim_product`, `dim_customer`, `dim_channel` connect to `fact_sales` only.
- `dim_production_line` connects to `fact_production` only.
- Do NOT connect the two fact tables directly — use `dim_date` for cross-table time analysis.
- Mark `dim_date[date]` as a **Date Table** after converting from string to Date type in Power Query.
- `total_revenue_egp` must be converted to Decimal Number before any SUM measure will work.
- `market` exists in both `fact_sales` (denormalized convenience column) and `dim_customer` — use `dim_customer[market]` via the relationship for cleaner filtering.

# Star Schema Relationships — ENR T07

## Tables
- **fact_ticket_sales** — central fact table (~2,000+ rows after cleaning)
- **dim_date** — date dimension
- **dim_route** — route dimension
- **dim_train** — train dimension
- **dim_channel** — booking channel dimension

## Relationships

| Fact Column | → | Dimension Table | Dimension Column | Cardinality | Filter Direction |
|-------------|---|-----------------|-----------------|-------------|-----------------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single (dim → fact) |
| `route_id` | → | `dim_route` | `route_id` | Many-to-One | Single (dim → fact) |
| `train_id` | → | `dim_train` | `train_id` | Many-to-One | Single (dim → fact) |
| `channel_id` | → | `dim_channel` | `channel_id` | Many-to-One | Single (dim → fact) |

## Notes
- All relationships are standard **one-to-many** from dimension PK to fact FK.
- Filter direction should be **single** (dimension → fact) for correct measure context.
- No many-to-many relationships.
- `dim_date[date]` must be marked as a **Date Table** in Power BI for time intelligence DAX to work.
- After cleaning, `total_revenue` must be a **Decimal Number** type for SUM to work.

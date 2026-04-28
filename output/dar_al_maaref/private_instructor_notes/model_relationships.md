# Star Schema Relationships — Dar Al Maaref

## Tables
- **fact_sales** — central fact table (~2,000+ rows after cleaning)
- **fact_inventory** — secondary fact table (monthly stock snapshots per book)
- **dim_date** — date dimension (shared by both fact tables)
- **dim_book** — book dimension (shared by both fact tables)
- **dim_customer** — customer dimension
- **dim_channel** — sales channel dimension

## Relationships

### fact_sales relationships
| Fact Column | → | Dimension Table | Dimension Column | Cardinality | Filter Direction |
|-------------|---|-----------------|-----------------|-------------|-----------------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single (dim → fact) |
| `book_id` | → | `dim_book` | `book_id` | Many-to-One | Single (dim → fact) |
| `customer_id` | → | `dim_customer` | `customer_id` | Many-to-One | Single (dim → fact) |
| `channel_id` | → | `dim_channel` | `channel_id` | Many-to-One | Single (dim → fact) |

### fact_inventory relationships
| Fact Column | → | Dimension Table | Dimension Column | Cardinality | Filter Direction |
|-------------|---|-----------------|-----------------|-------------|-----------------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single (dim → fact) |
| `book_id` | → | `dim_book` | `book_id` | Many-to-One | Single (dim → fact) |

## Notes
- Both fact tables share `dim_date` and `dim_book` — Power BI handles this correctly with two separate relationships.
- Do **not** create a direct relationship between `fact_sales` and `fact_inventory` — route all filters through shared dimensions.
- Mark `dim_date[date]` as a **Date Table** for time intelligence DAX functions.
- After cleaning, `channel_id` whitespace must be removed (Trim in Power Query) or the FK relationship will silently produce blanks.
- Filter direction should be **single** (dimension → fact) for all relationships.

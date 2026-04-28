# Star Schema Relationships — SODIC

## Tables
- **fact_unit_sales** — main fact: property unit contracts (~2,000+ rows)
- **fact_project_progress** — secondary fact: monthly project status snapshots (~240 rows)
- **dim_date** — date dimension (shared)
- **dim_project** — project/compound dimension (shared)
- **dim_unit_type** — unit type dimension (sales only)
- **dim_customer** — buyer dimension (sales only)
- **dim_channel** — sales channel dimension (sales only)

## Relationships

### fact_unit_sales
| Fact Column | → | Dimension | PK | Cardinality | Filter |
|-------------|---|-----------|----|-------------|--------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single |
| `project_id` | → | `dim_project` | `project_id` | Many-to-One | Single |
| `unit_type_id` | → | `dim_unit_type` | `unit_type_id` | Many-to-One | Single |
| `customer_id` | → | `dim_customer` | `customer_id` | Many-to-One | Single |
| `channel_id` | → | `dim_channel` | `channel_id` | Many-to-One | Single |

### fact_project_progress
| Fact Column | → | Dimension | PK | Cardinality | Filter |
|-------------|---|-----------|----|-------------|--------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single |
| `project_id` | → | `dim_project` | `project_id` | Many-to-One | Single |

## Notes
- Both fact tables share `dim_date` and `dim_project` — Power BI handles this correctly with separate relationships.
- `dim_unit_type`, `dim_customer`, and `dim_channel` are only connected to `fact_unit_sales`.
- Do NOT connect the two fact tables to each other directly — use shared dimensions for cross-table analysis.
- Mark `dim_date[date]` as a **Date Table** after converting from string to Date type.
- `contract_value` must be a numeric type (Decimal Number) before any SUM measure will work.
- The `delivery_status` casing issue in `fact_project_progress` directly affects the "On Track %" calculation — clean before building visuals.

# Star Schema Relationships — Banque du Caire

## Tables
- **fact_transactions** — main fact table: banking transactions (~2,000+ rows)
- **fact_loans** — secondary fact table: loan applications and performance (~600 rows)
- **dim_date** — date dimension (shared)
- **dim_branch** — branch dimension (shared)
- **dim_customer** — customer dimension
- **dim_channel** — channel dimension (transactions only)
- **dim_product** — product dimension (loans only)

## Relationships

### fact_transactions
| Fact Column | → | Dimension | PK | Cardinality | Filter |
|-------------|---|-----------|----|-------------|--------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single |
| `branch_id` | → | `dim_branch` | `branch_id` | Many-to-One | Single |
| `customer_id` | → | `dim_customer` | `customer_id` | Many-to-One | Single |
| `channel_id` | → | `dim_channel` | `channel_id` | Many-to-One | Single |

### fact_loans
| Fact Column | → | Dimension | PK | Cardinality | Filter |
|-------------|---|-----------|----|-------------|--------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single |
| `branch_id` | → | `dim_branch` | `branch_id` | Many-to-One | Single |
| `customer_id` | → | `dim_customer` | `customer_id` | Many-to-One | Single |
| `product_id` | → | `dim_product` | `product_id` | Many-to-One | Single |

## Notes
- `branch_id` in `fact_transactions` is nullable — digital transactions have no branch. Students must handle this in visuals (e.g., use ISBLANK checks).
- Both fact tables share `dim_date`, `dim_branch`, and `dim_customer`. Power BI handles this correctly; do NOT create cross-fact relationships.
- Mark `dim_date[date]` as a **Date Table** after converting from string to Date type.
- `dim_channel` is only relevant to `fact_transactions`; `dim_product` only to `fact_loans`.

# Star Schema Relationships — TMG

## Tables
- **fact_unit_sales** — main fact: property unit contracts (~2,000+ rows)
- **fact_community_services** — secondary fact: TMG Life app activity (~800 rows)
- **dim_date** — date dimension (shared)
- **dim_project** — project/community dimension (shared)
- **dim_unit_type** — unit type dimension (sales only)
- **dim_customer** — customer dimension (shared)
- **dim_channel** — sales channel dimension (sales only)
- **dim_service_type** — service category dimension (services only)

## Relationships

### fact_unit_sales
| Fact Column | → | Dimension | PK | Cardinality | Filter |
|-------------|---|-----------|----|-------------|--------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single |
| `project_id` | → | `dim_project` | `project_id` | Many-to-One | Single |
| `unit_type_id` | → | `dim_unit_type` | `unit_type_id` | Many-to-One | Single |
| `customer_id` | → | `dim_customer` | `customer_id` | Many-to-One | Single |
| `channel_id` | → | `dim_channel` | `channel_id` | Many-to-One | Single |

### fact_community_services
| Fact Column | → | Dimension | PK | Cardinality | Filter |
|-------------|---|-----------|----|-------------|--------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single |
| `customer_id` | → | `dim_customer` | `customer_id` | Many-to-One | Single |
| `project_id` | → | `dim_project` | `project_id` | Many-to-One | Single |
| `service_type_id` | → | `dim_service_type` | `service_type_id` | Many-to-One | Single |

## Notes
- Both fact tables share `dim_date`, `dim_project`, and `dim_customer` — connect each separately, do NOT create cross-fact relationships.
- `dim_unit_type` and `dim_channel` connect only to `fact_unit_sales`.
- `dim_service_type` connects only to `fact_community_services`.
- Mark `dim_date[date]` as a **Date Table** after converting from string to Date type.
- `contract_value` must be a numeric type (Decimal Number) before any SUM measure will work.
- Filter direction should be **single** (dimension → fact) for all relationships.

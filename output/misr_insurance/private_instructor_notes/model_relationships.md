# Star Schema Relationships — Misr Insurance Company

## Tables
- **fact_policies** — main fact: insurance policies sold (~2,000+ rows)
- **fact_claims** — secondary fact: claims filed (~700 rows)
- **dim_date** — date dimension (shared)
- **dim_branch** — branch dimension (shared)
- **dim_customer** — customer dimension (shared)
- **dim_product** — insurance product dimension (shared)
- **dim_channel** — sales channel (policies only)

## Relationships

### fact_policies
| Fact Column | → | Dimension | PK | Cardinality | Filter |
|-------------|---|-----------|----|-------------|--------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single |
| `customer_id` | → | `dim_customer` | `customer_id` | Many-to-One | Single |
| `branch_id` | → | `dim_branch` | `branch_id` | Many-to-One | Single |
| `product_id` | → | `dim_product` | `product_id` | Many-to-One | Single |
| `channel_id` | → | `dim_channel` | `channel_id` | Many-to-One | Single |

### fact_claims
| Fact Column | → | Dimension | PK | Cardinality | Filter |
|-------------|---|-----------|----|-------------|--------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single |
| `customer_id` | → | `dim_customer` | `customer_id` | Many-to-One | Single |
| `branch_id` | → | `dim_branch` | `branch_id` | Many-to-One | Single |
| `product_id` | → | `dim_product` | `product_id` | Many-to-One | Single |

## Notes
- `fact_claims.policy_id` references `fact_policies.policy_id` — do NOT create a direct fact-to-fact relationship in Power BI. Route all analysis through shared dimensions.
- Both fact tables share `dim_date`, `dim_branch`, `dim_customer`, and `dim_product` — Power BI handles this correctly with separate relationships.
- `dim_channel` applies only to `fact_policies` (how the policy was sold); claims do not have a channel.
- Mark `dim_date[date]` as a **Date Table** after converting from string.
- Loss Ratio = [Total Claims Paid] / [Total Premium Revenue] — a key insurance KPI that spans both fact tables; students must be careful about filter context when calculating it.

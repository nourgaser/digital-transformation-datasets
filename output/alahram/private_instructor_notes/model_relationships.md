# Star Schema Relationships — Al-Ahram Newspapers Company

## Tables
- **fact_ad_revenue** — main fact: advertisement bookings (~2,000+ rows, 2019–2024)
- **fact_monthly_metrics** — secondary fact: monthly company-wide KPI snapshot (72 rows)
- **dim_date** — date dimension shared by both facts (2019–2024, 2,192 rows)
- **dim_advertiser** — advertiser dimension (100 rows)
- **dim_platform** — publication/platform dimension (6 rows)
- **dim_ad_format** — ad format dimension (12 rows)

## Relationships

### fact_ad_revenue
| Fact Column | → | Dimension | PK | Cardinality | Filter |
|-------------|---|-----------|----|-------------|--------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single |
| `advertiser_id` | → | `dim_advertiser` | `advertiser_id` | Many-to-One | Single |
| `platform_id` | → | `dim_platform` | `platform_id` | Many-to-One | Single |
| `format_id` | → | `dim_ad_format` | `format_id` | Many-to-One | Single |

### fact_monthly_metrics
| Fact Column | → | Dimension | PK | Cardinality | Filter |
|-------------|---|-----------|----|-------------|--------|
| `date_id` | → | `dim_date` | `date_id` | Many-to-One | Single |

## Notes
- Both fact tables share `dim_date` — Power BI handles this correctly.
- `fact_monthly_metrics` has no dimension other than `dim_date`; it is a company-level aggregate scorecard. Do not connect it to dim_platform or dim_advertiser.
- `impressions_k` in `fact_ad_revenue` is NULL for all print ad rows — this is intentional. Students should filter to `ad_medium = "Digital"` before using this column.
- Mark `dim_date[date]` as a **Date Table** after converting from string to Date type.
- `net_revenue_egp` must be converted to Decimal Number (fixing type and removing negatives) before any SUM will work.
- The `ad_medium` column is a convenience denormalisation from `dim_platform[medium]` — either works for filtering.

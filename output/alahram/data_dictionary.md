# Data Dictionary — Al-Ahram Newspapers Company
## Digital Transformation Course · BINF 402 · GIU · Spring 2026

---

## Business Story
Al-Ahram, founded in 1875, is Egypt's oldest and most prominent media company. It operates Egypt's flagship daily Arabic newspaper, an English weekly, an evening edition, the leading Arabic news portal (ahram.org.eg), a mobile news app, and one of the most-watched Egyptian YouTube channels.

This dataset covers **advertisement bookings** and **monthly company performance metrics** for 2019–2024 — a period of dramatic digital transformation, with EGP devaluation, COVID-19, and the global shift from print to digital media all shaping business outcomes. Your goal as a Media Executive is to track how ad revenue is shifting from print to digital, whether audience growth is compensating for print circulation decline, and how the cost structure is evolving.

---

## Files

### `fact_ad_revenue.csv` (main fact table)
| Column | Description |
|--------|-------------|
| `booking_id` | Unique advertisement booking identifier |
| `date_id` | Foreign key → `dim_date.date_id` (booking date) |
| `advertiser_id` | Foreign key → `dim_advertiser.advertiser_id` |
| `platform_id` | Foreign key → `dim_platform.platform_id` |
| `format_id` | Foreign key → `dim_ad_format.format_id` |
| `ad_medium` | Print or Digital (convenience column) |
| `duration_days` | Number of days the ad ran (1 for print insertions) |
| `gross_revenue_egp` | Revenue before discount (EGP) |
| `discount_pct` | Discount applied (decimal, e.g. 0.10 = 10%) |
| `net_revenue_egp` | Final billed revenue after discount (EGP) |
| `impressions_k` | Estimated digital impressions/views (thousands) — **NULL for print ads by design** |
| `booking_status` | Confirmed, Under Review, or Cancelled |

### `fact_monthly_metrics.csv` (secondary fact table — monthly KPI scorecard)
| Column | Description |
|--------|-------------|
| `metric_id` | Unique row identifier |
| `date_id` | Foreign key → `dim_date.date_id` (first day of the month) |
| `print_circulation_k` | Average daily print copies distributed (thousands) |
| `unique_visitors_k` | Monthly unique website visitors (thousands) |
| `page_views_k` | Monthly page views across digital platforms (thousands) |
| `bounce_rate_pct` | Website bounce rate (%) |
| `avg_session_min` | Average visitor session duration (minutes) |
| `traffic_trend` | Growing, Stable, or Declining (vs prior month) |
| `archive_licensing_egp` | Monthly revenue from digital archive licensing (EGP) |
| `commercial_printing_egp` | Monthly revenue from external commercial printing services (EGP) |
| `printing_cost_egp` | Monthly newspaper printing cost (EGP) |
| `distribution_cost_egp` | Monthly newspaper distribution cost (EGP) |
| `it_cost_egp` | Monthly IT & digital infrastructure cost (EGP) |
| `fb_followers_k` | Facebook page followers at month-end (thousands) |
| `tw_followers_k` | Twitter/X followers at month-end (thousands) |
| `post_engagement_pct` | Average engagement rate across social posts (%) |
| `staff_trained_cumulative` | Cumulative number of staff who completed digital upskilling programmes |

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

### `dim_advertiser.csv`
| Column | Description |
|--------|-------------|
| `advertiser_id` | Primary key |
| `advertiser_name` | Synthetic company name |
| `advertiser_category` | Government, Banking/Finance, Telecom, Real Estate, FMCG, Automotive, Healthcare, Education, or Retail |
| `platform_preference` | Print_Heavy, Mixed, or Digital_Heavy |
| `advertiser_tier` | Premium, Standard, or Budget |

### `dim_platform.csv`
| Column | Description |
|--------|-------------|
| `platform_id` | Primary key |
| `platform_name` | Al-Ahram Daily, Al-Ahram Weekly, Al-Masaa Evening, ahram.org.eg, Al-Ahram Mobile App, Al-Ahram YouTube |
| `medium` | Print or Digital |
| `description` | Brief platform description |

### `dim_ad_format.csv`
| Column | Description |
|--------|-------------|
| `format_id` | Primary key |
| `format_name` | Full Page, Half Page, Display Banner, Video Pre-roll 15s, etc. |
| `medium` | Print or Digital |
| `base_rate_egp` | Reference base rate (EGP, in 2019 terms) |
| `rate_basis` | per insertion (print) or per day / per placement (digital) |

---

## Intended Relationships
- `fact_ad_revenue` → `dim_date`, `dim_advertiser`, `dim_platform`, `dim_ad_format`
- `fact_monthly_metrics` → `dim_date`

## Notes for Students
- `net_revenue_egp` must be converted to a numeric type before any SUM measure will work.
- `impressions_k` is NULL for all print ad rows — this is **by design**, not a data error. Only use this column when filtering to Digital ads.
- The dataset spans 2019–2024: print ad revenue will show a clear decline while digital grows — this is the central insight to explore.
- Ad prices in 2023–2024 are significantly higher in EGP terms due to currency devaluation — compare prices across years carefully.
- `fact_monthly_metrics` contains one row per month (72 rows total). Connect it to `dim_date` to enable time-series analysis of traffic, costs, and social media.
- Clean all data in Power Query before building any measures or visuals.

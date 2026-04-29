# Dashboard Questions & Visual Suggestions — Al-Ahram Newspapers Company

## Analytical Questions (student-facing prompts)
1. How has total ad revenue split between Print and Digital changed from 2019 to 2024?
2. Which year showed the biggest acceleration in digital ad revenue — and can you link it to external events (COVID 2020, EGP devaluation 2023)?
3. Which advertiser category spends the most on digital ads? Which still prefers print?
4. How has website traffic (unique visitors) grown from 2019 to 2024, and what is the seasonal pattern?
5. How have bounce rate and average session duration changed over 6 years — is engagement improving?
6. How does archive licensing revenue trend compare to print circulation decline?
7. What is the operating cost structure — how do printing, distribution, and IT costs compare over time?
8. Which platform (Daily, Weekly, Evening, ahram.org.eg, Mobile App) generates the most ad revenue?
9. Which ad format has the highest average booking value?
10. How have Facebook and Twitter follower counts grown, and is engagement rate keeping pace?

## Suggested Visuals (instructor only)

| Visual | Type | Fields |
|--------|------|--------|
| Total Net Revenue KPI | Card | [Total Net Revenue] |
| Digital Revenue % KPI | Card | [Digital Revenue %] |
| Total Confirmed Bookings KPI | Card | [Total Confirmed Bookings] |
| Avg Unique Visitors KPI | Card | [Avg Unique Visitors K] |
| Print vs Digital Revenue Over Time | Area/Line | dim_date[year], Print vs Digital (stacked) |
| Revenue by Platform | Bar | dim_platform[platform_name], [Total Net Revenue] |
| Revenue by Ad Format | Bar | dim_ad_format[format_name], [Total Net Revenue] |
| Revenue by Advertiser Category | Bar | dim_advertiser[advertiser_category], [Total Net Revenue] |
| YoY Revenue Growth | Line | dim_date[year], [YoY Revenue Growth %] |
| Unique Visitors Trend | Line | dim_date[month_name], [Avg Unique Visitors K] |
| Bounce Rate & Session Duration | Dual-line | dim_date[year], bounce_rate + avg_session |
| Print Circulation Decline | Line | dim_date[year], print_circulation_k |
| Operating Cost Breakdown | Stacked bar | dim_date[year], printing + distribution + IT |
| Social Followers Growth | Line | dim_date[year], fb + twitter followers |
| Cancellation Rate | Card/Bar | [Cancellation Rate] |

## Suggested Slicers
- Year / Quarter / Month
- Ad Medium (Print / Digital)
- Platform
- Advertiser Category / Tier
- Booking Status
- Ad Format

## Dashboard Pages Suggestion
1. **Revenue Overview** — total revenue, print vs digital trend, top advertisers
2. **Digital Transformation** — digital revenue %, mobile share, e-commerce channel
3. **Audience & Engagement** — unique visitors, bounce rate, session duration, social media
4. **Operations & Costs** — printing, distribution, IT costs over time; circulation decline

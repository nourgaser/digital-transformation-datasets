# Dashboard Questions & Visual Suggestions — Misr Insurance Company

## Analytical Questions (student-facing prompts)
1. Which insurance product generates the highest premium revenue and net profit?
2. What is the overall Loss Ratio, and how does it vary by product category?
3. Which regions have the highest claim frequency and claim value?
4. How does premium revenue trend month-over-month and year-over-year?
5. What is the claim approval rate, and how long does processing typically take?
6. Which sales channel (Branch / Agent / Online) drives the most policies?
7. What share of customers are returning vs new, and how does this affect revenue?
8. Are there seasonal patterns in policy sales (e.g., Travel in summer, Motor in winter)?
9. Which branches perform best in terms of policy volume and premium collected?
10. How does the combined ratio compare to industry benchmarks?

## Suggested Visuals (instructor only)

| Visual | Type | Fields |
|--------|------|--------|
| Total Premium Revenue KPI | Card | [Total Premium Revenue] |
| Total Claims Paid KPI | Card | [Total Claims Paid] |
| Net Profit KPI | Card | [Net Profit] |
| Loss Ratio KPI | Card/Gauge | [Loss Ratio] |
| Claim Approval Rate KPI | Card | [Claim Approval Rate] |
| Premium Revenue over Time | Line | dim_date[month_name], [Total Premium Revenue] |
| Revenue by Product Category | Bar | dim_product[product_category], [Total Premium Revenue] |
| Claims by Product Category | Bar | dim_product[product_category], [Total Claims Paid] |
| Loss Ratio by Product | Bar | dim_product[product_name], [Loss Ratio] |
| Revenue by Region | Map / Bar | dim_branch[region], [Total Premium Revenue] |
| Claims by Cause | Treemap / Bar | fact_claims[claim_cause], count |
| Claim Status Breakdown | Donut | fact_claims[claim_status], count |
| Avg Processing Days by Product | Bar | dim_product[product_category], [Avg Claim Processing Days] |
| Channel Mix | Donut | dim_channel[channel_name], [Total Policies Issued] |
| Returning vs New Customers | Stacked bar | dim_date[year], [Returning Customers] + [New Customers] |
| YoY Revenue Comparison | Line (dual) | dim_date[month], [Total Premium Revenue] vs prev year |

## Suggested Slicers
- Year / Quarter / Month
- Product Category
- Region / Branch
- Customer Type (Individual / Corporate)
- Channel
- Claim Status

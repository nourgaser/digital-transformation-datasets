# Dashboard Questions & Visual Suggestions — TMG

## Analytical Questions (student-facing prompts)
1. Which TMG projects generate the highest total contract value (Madinaty, Al Rehab, Noor City, others)?
2. How does Off-Plan financing contribute to total revenue, and how does it compare to cash + standard installments?
3. Which unit types drive the most revenue and volume across the portfolio?
4. How does sales volume change month-over-month and year-over-year?
5. How does the channel mix differ between 2023 and 2024 — is the TMG Life app gaining share?
6. What is the average price per sqm by project, and how has it changed from 2023 to 2024 (EGP devaluation impact)?
7. What share of buyers are Egyptian Diaspora or foreign investors?
8. How active are residents on the TMG Life app? Which service categories are most used?
9. What is the average service resolution time, and which service categories take longest?
10. What is the average customer rating for completed services?
11. Which projects have the highest community service activity (a proxy for resident engagement)?
12. What is the cancellation rate by project and channel?

## Suggested Visuals (instructor only)

| Visual | Type | Fields |
|--------|------|--------|
| Total Contract Value KPI | Card | [Total Contract Value] |
| Total Units Sold KPI | Card | [Total Units Sold] |
| Off-Plan Sales % KPI | Card | [Off-Plan Sales %] |
| Avg Service Rating KPI | Card | [Avg Service Rating] |
| Sales by Project | Bar | dim_project[project_name], [Total Contract Value] |
| Sales by Unit Type | Bar/Donut | dim_unit_type[unit_type], [Total Units Sold] |
| Contract Value over Time | Line | dim_date[month_name], [Total Contract Value] |
| YoY Comparison | Line (dual) | dim_date[month], current vs prior year |
| Channel Mix 2023 vs 2024 | Clustered bar | dim_channel[channel_name], year slicer |
| Sales by Buyer Type | Donut | dim_customer[buyer_type], [Total Contract Value] |
| Off-Plan vs Cash | Stacked bar | fact[is_off_plan], [Total Contract Value] |
| Service Activity by Category | Bar | dim_service_type[service_category], count |
| Service Status Breakdown | Donut | fact_community_services[service_status] |
| Avg Resolution Hours by Category | Bar | dim_service_type[service_category], [Avg Resolution Hours] |
| Service Activity by Project | Bar | dim_project[project_name], [Total Service Activities] |
| Payment Plan Distribution | Pie | fact_unit_sales[payment_plan], count |
| Cancellation Rate by Project | Bar | dim_project[project_name], [Cancellation Rate] |

## Suggested Slicers
- Year / Quarter / Month
- Project Name / Project Type
- Unit Type
- Sales Channel / Channel Type
- Buyer Type
- Service Category
- Contract Status

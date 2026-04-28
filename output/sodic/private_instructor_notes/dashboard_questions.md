# Dashboard Questions & Visual Suggestions — SODIC

## Analytical Questions (student-facing prompts)
1. Which projects generate the highest total contract value?
2. How does revenue from Broker vs Direct vs Digital (Sakneen) compare, and how has the channel mix shifted from 2023 to 2024?
3. Which unit types (Villa, Apartment, Commercial) drive the most revenue and volume?
4. How does sales volume change by month — are there seasonal peaks (North Coast in summer, year-end Q4)?
5. What is the average contract value per project, and how does price per sqm compare across projects?
6. What is the project completion rate, and which projects are on track vs delayed?
7. What share of buyers are investors vs end-users, and which buyer types prefer which projects?
8. How does 2024 pricing compare to 2023 (EGP inflation impact on contract values)?
9. What is the cancellation rate by project and channel?
10. Which payment plan is most popular, and does it vary by unit type or buyer segment?

## Suggested Visuals (instructor only)

| Visual | Type | Fields |
|--------|------|--------|
| Total Contract Value KPI | Card | [Total Contract Value] |
| Total Units Sold KPI | Card | [Total Units Sold] |
| Avg Contract Value KPI | Card | [Average Contract Value] |
| Digital Sales % KPI | Card | [Digital Sales %] |
| Sales by Project | Bar | dim_project[project_name], [Total Contract Value] |
| Sales by Unit Type | Bar/Donut | dim_unit_type[unit_type], [Total Units Sold] |
| Contract Value over Time | Line | dim_date[month_name], [Total Contract Value] |
| YoY Comparison | Line (dual) | dim_date[month], current vs prior year |
| Channel Mix 2023 vs 2024 | Clustered bar | dim_channel[channel_name], year slicer |
| Project Completion | Gauge/Bar | dim_project[project_name], [Avg Completion %] |
| Budget vs Actual | Clustered bar | dim_project[project_name], budget_total vs budget_spent |
| Buyer Type Breakdown | Donut | dim_customer[buyer_type], [Total Buyers] |
| Sales by Location | Bar/Map | dim_project[location], [Total Contract Value] |
| Payment Plan Distribution | Pie | fact_unit_sales[payment_plan], count |
| Cancellation Rate by Project | Bar | dim_project[project_name], [Cancellation Rate] |

## Suggested Slicers
- Year / Quarter / Month
- Project Name / Location
- Unit Type
- Sales Channel
- Buyer Type
- Contract Status

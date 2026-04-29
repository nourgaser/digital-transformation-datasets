# Dashboard Questions & Visual Suggestions — MSW

## Analytical Questions (student-facing prompts)
1. Which product category (Yarn, Grey Fabric, Finished Fabric, Garment) generates the most revenue?
2. How has the Export vs Domestic revenue split changed from 2023 to 2024?
3. Which sales channel is growing fastest — and what is the share of E-commerce in 2024?
4. What is the seasonal pattern of sales revenue (are there peaks in Sep–Nov)?
5. Which customer type (Local Retailer, Garment Manufacturer, Export Buyer, etc.) drives the most total revenue?
6. How does average production efficiency compare across the four departments?
7. Which production line has the highest defect rate, and which has the most downtime hours?
8. What is the 2024 vs 2023 price inflation impact on average unit price?
9. What is the order cancellation and return rate — does it vary by product category or channel?
10. How has monthly production output changed from 2023 to 2024 (digitization impact on efficiency)?

## Suggested Visuals (instructor only)

| Visual | Type | Fields |
|--------|------|--------|
| Total Revenue KPI | Card | [Total Revenue] |
| Total Orders KPI | Card | [Total Orders] |
| Export Revenue % KPI | Card | [Export Revenue %] |
| Avg Production Efficiency KPI | Card | [Avg Production Efficiency %] |
| Revenue by Category | Bar | dim_product[category], [Total Revenue] |
| Revenue by Channel | Bar | dim_channel[channel_name], [Total Revenue] |
| Revenue Over Time | Line | dim_date[month_name], [Total Revenue] |
| YoY Revenue Comparison | Line (dual) | dim_date[month], current vs prior year |
| Export vs Domestic Split | Donut | fact_sales[market], [Total Revenue] |
| Channel Mix 2023 vs 2024 | Clustered bar | dim_channel[channel_name], year slicer |
| Defect Rate by Department | Bar | dim_production_line[department], [Avg Defect Rate %] |
| Efficiency by Production Line | Bar | dim_production_line[line_name], [Avg Production Efficiency %] |
| Production Output Trend | Line | dim_date[month_name], [Total Output KG] |
| Customer Type Revenue | Bar | dim_customer[customer_type], [Total Revenue] |
| Cancellation Rate by Product | Bar | dim_product[category], [Cancellation Rate] |

## Suggested Slicers
- Year / Quarter / Month
- Product Category / Fiber Type
- Customer Type / Market (Export vs Domestic)
- Sales Channel
- Department (for production views)
- Order Status

# Dashboard Questions & Visual Suggestions — Dar Al Maaref

## Analytical Questions (student-facing prompts)
1. Which book titles and categories generate the most revenue?
2. Which customer type (Individual / School / Library / Distributor) drives the most sales?
3. How does revenue change month-over-month and year-over-year?
4. What is the profit margin across different book categories?
5. Which sales channel (online vs. contract vs. distributor) performs best?
6. Which governorates/regions generate the most sales?
7. Which books are running low on stock and may need reprinting?
8. What is the average order processing time by customer type?
9. How does back-to-school season (Aug–Sep) affect sales and inventory?
10. What is the return rate, and which books have the highest return rates?

## Suggested Visuals (instructor only)

| Visual | Type | Fields |
|--------|------|--------|
| Total Revenue KPI | Card | [Total Revenue] |
| Total Orders KPI | Card | [Total Orders] |
| Profit Margin % KPI | Card | [Profit Margin %] |
| Customer Retention Rate KPI | Card | [Customer Retention Rate] |
| Revenue by Book Category | Bar/Donut | dim_book[category], [Total Revenue] |
| Top 10 Best-Selling Books | Bar | dim_book[title], [Total Units Sold] |
| Sales over Time | Line | dim_date[month_name], [Total Revenue] — year slicer |
| Revenue by Customer Type | Stacked bar | dim_customer[customer_type], [Total Revenue] |
| Revenue by Governorate | Map / Choropleth | dim_customer[governorate], [Total Revenue] |
| Channel Comparison | Clustered bar | dim_channel[channel_name], [Total Revenue] |
| Inventory Below Reorder | Table/Alert | dim_book[title], fact_inventory[closing_stock], [reorder_point] |
| Avg Processing Days | Bar | dim_customer[customer_type], [Avg Processing Days] |
| YoY Revenue | Line | dim_date[year+month], [Total Revenue] + [Revenue Previous Year] |

## Suggested Slicers
- Year
- Quarter / Month
- Book Category
- Customer Type
- Governorate / Region
- Sales Channel

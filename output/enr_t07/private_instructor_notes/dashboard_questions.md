# Dashboard Questions & Visual Suggestions — ENR T07

## Analytical Questions (student-facing prompts)
1. Which routes generate the most total revenue?
2. How does ticket revenue change month-over-month and year-over-year?
3. Which ticket class (First / Second / Third) contributes the most to revenue and volume?
4. How does online channel performance compare to offline?
5. Which booking channel (Website, App, Fawry, etc.) sells the most tickets?
6. What is the cancellation rate, and does it vary by route or class?
7. How does occupancy rate vary by train type and route?
8. What is the revenue split between express and standard services?

## Suggested Visuals (instructor only)

| Visual | Type | Fields |
|--------|------|--------|
| Total Revenue KPI card | Card | [Total Revenue] |
| Total Tickets Sold KPI card | Card | [Total Tickets Sold] |
| Revenue Growth % KPI card | Card | [Revenue MoM Growth %] |
| Occupancy Rate KPI card | Card | [Occupancy Rate] |
| Revenue by Route | Bar chart | dim_route[origin_city] + destination, [Total Revenue] |
| Tickets by Class | Pie/Donut | fact[ticket_class], [Total Tickets Sold] |
| Sales over Time | Line chart | dim_date[month], [Total Revenue] — with year slicer |
| Online vs Offline | Clustered bar | dim_channel[channel_category], [Total Revenue] |
| Channel breakdown | Stacked bar | dim_channel[channel_name], [Total Revenue] |
| Revenue by Train Type | Bar | dim_train[train_type], [Total Revenue] |
| YoY Revenue | Line | dim_date[year+month], [Total Revenue] + [Revenue Previous Year] |
| Cancellation Rate | Card / Gauge | [Cancellation Rate] |

## Suggested Slicers
- Year
- Month
- Route
- Ticket Class
- Channel Category (Online / Offline)
- Train Type

# Dashboard Questions & Visual Suggestions — Banque du Caire

## Analytical Questions (student-facing prompts)
1. What is the total transaction volume, and how has it grown year-over-year?
2. How is the loan portfolio distributed across product types and customer segments?
3. What is the Non-Performing Loan (NPL) ratio, and which segments drive it?
4. How does digital transaction adoption compare to in-branch over 2023 vs 2024?
5. Which branches generate the highest transaction volumes and fee revenue?
6. What is the loan approval vs rejection rate, and how does it vary by risk level?
7. Which customer segments (Retail, Premium, SME, Corporate) contribute most to volume?
8. How does transaction volume vary by month — are there seasonal peaks?
9. What share of customers are digitally enrolled, and how does that affect their behavior?
10. Which regions (Cairo, Delta, Upper Egypt) are most active in terms of transactions and loans?

## Suggested Visuals (instructor only)

| Visual | Type | Fields |
|--------|------|--------|
| Total Transaction Volume KPI | Card | [Total Transaction Volume] |
| NPL Ratio KPI | Card/Gauge | [NPL Ratio] |
| Loan Approval Rate KPI | Card | [Loan Approval Rate] |
| Digital Adoption Rate KPI | Card | [Digital Adoption Rate] |
| Transaction Volume over Time | Line | dim_date[month_name], [Total Transaction Volume] |
| Digital vs Physical Trend | Line (dual) | dim_date[month], [Digital Transactions] + [Physical Transactions] |
| Volume by Branch | Bar | dim_branch[branch_name], [Total Transaction Volume] |
| Volume by Region | Map / Bar | dim_branch[region], [Total Transaction Volume] |
| Loan Portfolio by Type | Donut | dim_product[product_name], [Total Loan Portfolio] |
| Loan Status Breakdown | Stacked bar | fact_loans[loan_status], count |
| NPL by Customer Segment | Bar | dim_customer[segment], [NPL Ratio] |
| Risk Level Distribution | Pie | fact_loans[risk_level], count |
| Transactions by Type | Treemap | fact_transactions[transaction_type], [Total Transaction Volume] |
| Digital Adoption YoY | Clustered bar | dim_date[year], [Digital Adoption Rate] |

## Suggested Slicers
- Year / Quarter
- Branch / Region
- Customer Segment
- Channel Type (Digital / Physical)
- Product Type
- Loan Status

# Suggested DAX Measures — Dar Al Maaref

## Revenue & Profit
```dax
Total Revenue =
    CALCULATE(
        SUM(fact_sales[total_revenue]),
        fact_sales[order_status] = "Delivered"
    )

Total Cost =
    CALCULATE(
        SUM(fact_sales[total_cost]),
        fact_sales[order_status] = "Delivered"
    )

Total Profit =
    [Total Revenue] - [Total Cost]

Profit Margin % =
    DIVIDE([Total Profit], [Total Revenue])

Total Orders =
    COUNTROWS(fact_sales)

Average Order Value =
    DIVIDE([Total Revenue], [Total Orders])
```

## Sales Performance
```dax
Total Units Sold =
    CALCULATE(
        SUM(fact_sales[quantity]),
        fact_sales[order_status] = "Delivered"
    )

Return Rate =
    DIVIDE(
        COUNTROWS(FILTER(fact_sales, fact_sales[order_status] = "Returned")),
        [Total Orders]
    )

Revenue by Category =
    CALCULATE([Total Revenue], ALLEXCEPT(dim_book, dim_book[category]))
```

## Growth & Time Intelligence
```dax
YTD Revenue =
    TOTALYTD([Total Revenue], dim_date[date])

Revenue MoM Growth % =
    VAR PrevMonth = CALCULATE([Total Revenue], DATEADD(dim_date[date], -1, MONTH))
    RETURN DIVIDE([Total Revenue] - PrevMonth, PrevMonth)

Revenue Previous Year =
    CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(dim_date[date]))

YoY Revenue Growth % =
    DIVIDE([Total Revenue] - [Revenue Previous Year], [Revenue Previous Year])
```

## Customer KPIs
```dax
Number of Customers =
    DISTINCTCOUNT(fact_sales[customer_id])

Repeat Customers =
    COUNTROWS(
        FILTER(
            VALUES(fact_sales[customer_id]),
            CALCULATE(COUNTROWS(fact_sales)) > 1
        )
    )

Customer Retention Rate =
    DIVIDE([Repeat Customers], [Number of Customers])

Avg Processing Days =
    AVERAGE(fact_sales[processing_days])
```

## Inventory KPIs
```dax
Total Closing Stock =
    SUM(fact_inventory[closing_stock])

Books Below Reorder Point =
    CALCULATE(
        COUNTROWS(fact_inventory),
        fact_inventory[below_reorder] = TRUE()
    )

Inventory Turnover =
    DIVIDE([Total Units Sold], [Total Closing Stock])
```

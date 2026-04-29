# Suggested DAX Measures — Misr Spinning and Weaving Company (MSW)

## Sales Revenue
```dax
Total Revenue =
    CALCULATE(
        SUM(fact_sales[total_revenue_egp]),
        fact_sales[order_status] = "Completed",
        fact_sales[total_revenue_egp] > 0
    )

Total Orders =
    CALCULATE(
        COUNTROWS(fact_sales),
        fact_sales[order_status] = "Completed"
    )

Average Order Value =
    DIVIDE([Total Revenue], [Total Orders])

Average Unit Price =
    DIVIDE(
        CALCULATE(SUM(fact_sales[total_revenue_egp]),
                  fact_sales[order_status] = "Completed"),
        CALCULATE(SUM(fact_sales[quantity]),
                  fact_sales[order_status] = "Completed")
    )

Total Quantity Sold =
    CALCULATE(
        SUM(fact_sales[quantity]),
        fact_sales[order_status] = "Completed"
    )

Cancellation Rate =
    DIVIDE(
        CALCULATE(COUNTROWS(fact_sales), fact_sales[order_status] = "Cancelled"),
        COUNTROWS(fact_sales)
    )
```

## Channel & Market Performance
```dax
Export Revenue =
    CALCULATE([Total Revenue], fact_sales[market] = "Export")

Domestic Revenue =
    CALCULATE([Total Revenue], fact_sales[market] = "Domestic")

Export Revenue % =
    DIVIDE([Export Revenue], [Total Revenue])

E-commerce Revenue =
    CALCULATE([Total Revenue],
        RELATED(dim_channel[channel_name]) = "E-commerce"
    )

E-commerce Revenue % =
    DIVIDE([E-commerce Revenue], [Total Revenue])
```

## Production KPIs
```dax
Avg Production Efficiency % =
    AVERAGE(fact_production[efficiency_pct])

Avg Defect Rate % =
    AVERAGE(fact_production[defect_rate_pct])

Total Output KG =
    SUM(fact_production[actual_output_kg])

Total Defect KG =
    SUM(fact_production[defect_qty_kg])

Lines Under Maintenance =
    CALCULATE(
        DISTINCTCOUNT(fact_production[line_id]),
        fact_production[production_status] = "Under Maintenance"
    )

Avg Downtime Hours =
    CALCULATE(
        AVERAGE(fact_production[downtime_hours]),
        NOT(ISBLANK(fact_production[downtime_hours]))
    )
```

## Growth & Time Intelligence
```dax
YTD Revenue =
    TOTALYTD([Total Revenue], dim_date[date])

MoM Revenue Growth % =
    VAR Prev = CALCULATE([Total Revenue], DATEADD(dim_date[date], -1, MONTH))
    RETURN DIVIDE([Total Revenue] - Prev, Prev)

YoY Revenue Growth % =
    DIVIDE(
        [Total Revenue] - CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(dim_date[date])),
        CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(dim_date[date]))
    )

YoY Efficiency Change % =
    DIVIDE(
        [Avg Production Efficiency %] -
        CALCULATE([Avg Production Efficiency %], SAMEPERIODLASTYEAR(dim_date[date])),
        CALCULATE([Avg Production Efficiency %], SAMEPERIODLASTYEAR(dim_date[date]))
    )
```

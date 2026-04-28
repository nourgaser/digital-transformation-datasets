# Suggested DAX Measures — SODIC

## Sales Revenue
```dax
Total Contract Value =
    CALCULATE(
        SUM(fact_unit_sales[contract_value]),
        fact_unit_sales[contract_status] = "Signed",
        fact_unit_sales[contract_value] > 0
    )

Total Units Sold =
    CALCULATE(
        COUNTROWS(fact_unit_sales),
        fact_unit_sales[contract_status] = "Signed"
    )

Average Contract Value =
    DIVIDE([Total Contract Value], [Total Units Sold])

Average Price per SQM =
    DIVIDE(
        CALCULATE(SUM(fact_unit_sales[contract_value]),
                  fact_unit_sales[contract_status] = "Signed"),
        CALCULATE(SUM(fact_unit_sales[area_sqm]),
                  fact_unit_sales[contract_status] = "Signed")
    )

Cancellation Rate =
    DIVIDE(
        CALCULATE(COUNTROWS(fact_unit_sales),
                  fact_unit_sales[contract_status] = "Cancelled"),
        COUNTROWS(fact_unit_sales)
    )

Total Down Payments Collected =
    CALCULATE(
        SUM(fact_unit_sales[down_payment]),
        fact_unit_sales[contract_status] = "Signed"
    )

Total Commission Paid =
    CALCULATE(
        SUM(fact_unit_sales[commission_amount]),
        fact_unit_sales[contract_status] = "Signed"
    )
```

## Channel Performance
```dax
Digital Sales Value =
    CALCULATE([Total Contract Value],
        RELATED(dim_channel[channel_type]) = "Online"
    )

Broker Sales Value =
    CALCULATE([Total Contract Value],
        dim_channel[channel_name] = "Broker"
    )

Digital Sales % =
    DIVIDE([Digital Sales Value], [Total Contract Value])
```

## Project Performance
```dax
Avg Completion % =
    AVERAGE(fact_project_progress[completion_pct])

Projects On Track =
    CALCULATE(
        DISTINCTCOUNT(fact_project_progress[project_id]),
        fact_project_progress[delivery_status] = "On Track"
    )

Avg Cost Overrun % =
    CALCULATE(
        AVERAGE(fact_project_progress[cost_overrun_pct]),
        fact_project_progress[cost_overrun_pct] >= 0
    )

Budget Utilization % =
    DIVIDE(
        SUM(fact_project_progress[budget_spent_mEGP]),
        SUM(fact_project_progress[budget_total_mEGP])
    )
```

## Growth & Time Intelligence
```dax
YTD Contract Value =
    TOTALYTD([Total Contract Value], dim_date[date])

MoM Sales Growth % =
    VAR Prev = CALCULATE([Total Contract Value], DATEADD(dim_date[date], -1, MONTH))
    RETURN DIVIDE([Total Contract Value] - Prev, Prev)

YoY Sales Growth % =
    DIVIDE(
        [Total Contract Value] - CALCULATE([Total Contract Value], SAMEPERIODLASTYEAR(dim_date[date])),
        CALCULATE([Total Contract Value], SAMEPERIODLASTYEAR(dim_date[date]))
    )
```

## Customer KPIs
```dax
Total Buyers =
    DISTINCTCOUNT(fact_unit_sales[customer_id])

Investor Buyers % =
    DIVIDE(
        CALCULATE([Total Units Sold], fact_unit_sales[is_investor_buyer] = TRUE()),
        [Total Units Sold]
    )

Diaspora Buyers % =
    DIVIDE(
        CALCULATE([Total Buyers],
            RELATED(dim_customer[buyer_type]) = "Egyptian Diaspora"),
        [Total Buyers]
    )
```

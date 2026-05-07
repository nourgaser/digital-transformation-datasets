# Suggested DAX Measures — TMG

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

Off-Plan Sales % =
    DIVIDE(
        CALCULATE([Total Contract Value], fact_unit_sales[is_off_plan] = TRUE()),
        [Total Contract Value]
    )

Total Down Payments Collected =
    CALCULATE(
        SUM(fact_unit_sales[down_payment]),
        fact_unit_sales[contract_status] = "Signed"
    )
```

## Channel Performance
```dax
Digital Channel Revenue =
    CALCULATE([Total Contract Value],
        RELATED(dim_channel[channel_type]) = "Digital"
    )

Direct Sales Revenue =
    CALCULATE([Total Contract Value],
        RELATED(dim_channel[channel_type]) = "Direct"
    )

Digital Sales % =
    DIVIDE([Digital Channel Revenue], [Total Contract Value])
```

## Community Services (TMG Life App)
```dax
Total Service Activities =
    COUNTROWS(fact_community_services)

Total Service Revenue =
    SUM(fact_community_services[amount_paid_egp])

Avg Service Rating =
    CALCULATE(
        AVERAGE(fact_community_services[rating]),
        fact_community_services[service_status] = "Completed"
    )

Avg Resolution Hours =
    CALCULATE(
        AVERAGE(fact_community_services[resolution_hours]),
        fact_community_services[resolution_hours] > 0
    )

Service Completion Rate =
    DIVIDE(
        CALCULATE(COUNTROWS(fact_community_services),
                  fact_community_services[service_status] = "Completed"),
        [Total Service Activities]
    )

Active App Users =
    DISTINCTCOUNT(fact_community_services[customer_id])
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

Diaspora Buyers % =
    DIVIDE(
        CALCULATE(DISTINCTCOUNT(fact_unit_sales[customer_id]),
            RELATED(dim_customer[buyer_type]) = "Egyptian Diaspora"),
        [Total Buyers]
    )

Foreign + Arab Investor % =
    DIVIDE(
        CALCULATE(DISTINCTCOUNT(fact_unit_sales[customer_id]),
            RELATED(dim_customer[buyer_type]) IN { "Arab Investor", "Foreign Investor" }),
        [Total Buyers]
    )
```

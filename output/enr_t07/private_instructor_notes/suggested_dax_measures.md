# Suggested DAX Measures — ENR T07

## Revenue & Sales
```dax
Total Revenue =
    CALCULATE(
        SUM(fact_ticket_sales[total_revenue]),
        fact_ticket_sales[booking_status] = "Completed"
    )

Total Tickets Sold =
    CALCULATE(
        SUM(fact_ticket_sales[tickets_sold]),
        fact_ticket_sales[booking_status] = "Completed"
    )

Average Ticket Price =
    DIVIDE([Total Revenue], [Total Tickets Sold])

Total Transactions =
    COUNTROWS(fact_ticket_sales)

Cancellation Rate =
    DIVIDE(
        COUNTROWS(FILTER(fact_ticket_sales, fact_ticket_sales[booking_status] = "Cancelled")),
        [Total Transactions]
    )
```

## Growth & Time Intelligence
```dax
Revenue MoM Growth % =
    VAR PrevMonth = CALCULATE([Total Revenue], DATEADD(dim_date[date], -1, MONTH))
    RETURN DIVIDE([Total Revenue] - PrevMonth, PrevMonth)

YTD Revenue =
    TOTALYTD([Total Revenue], dim_date[date])

Revenue Previous Year =
    CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(dim_date[date]))

YoY Revenue Growth % =
    DIVIDE([Total Revenue] - [Revenue Previous Year], [Revenue Previous Year])
```

## Occupancy
```dax
-- Occupancy Rate: tickets sold vs theoretical capacity per transaction
-- (requires knowing capacity per class per train — use dim_train)
Occupancy Rate =
    DIVIDE([Total Tickets Sold],
           SUMX(fact_ticket_sales,
               SWITCH(fact_ticket_sales[ticket_class],
                   "First",  RELATED(dim_train[first_class_capacity]),
                   "Second", RELATED(dim_train[second_class_capacity]),
                   "Third",  RELATED(dim_train[third_class_capacity])
               )
           )
    )
```

## Channel Analysis
```dax
Online Revenue =
    CALCULATE([Total Revenue],
        RELATED(dim_channel[channel_category]) = "Online"
    )

Offline Revenue =
    CALCULATE([Total Revenue],
        RELATED(dim_channel[channel_category]) = "Offline"
    )

Online Revenue % =
    DIVIDE([Online Revenue], [Total Revenue])
```

## Route Analysis
```dax
Revenue Per KM =
    DIVIDE([Total Revenue], SUM(dim_route[distance_km]))
```

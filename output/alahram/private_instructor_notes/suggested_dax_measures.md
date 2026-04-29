# Suggested DAX Measures — Al-Ahram Newspapers Company

## Ad Revenue
```dax
Total Net Revenue =
    CALCULATE(
        SUM(fact_ad_revenue[net_revenue_egp]),
        fact_ad_revenue[booking_status] = "Confirmed",
        fact_ad_revenue[net_revenue_egp] > 0
    )

Total Confirmed Bookings =
    CALCULATE(
        COUNTROWS(fact_ad_revenue),
        fact_ad_revenue[booking_status] = "Confirmed"
    )

Average Booking Value =
    DIVIDE([Total Net Revenue], [Total Confirmed Bookings])

Cancellation Rate =
    DIVIDE(
        CALCULATE(COUNTROWS(fact_ad_revenue),
                  fact_ad_revenue[booking_status] = "Cancelled"),
        COUNTROWS(fact_ad_revenue)
    )
```

## Print vs Digital Revenue
```dax
Print Revenue =
    CALCULATE([Total Net Revenue], fact_ad_revenue[ad_medium] = "Print")

Digital Revenue =
    CALCULATE([Total Net Revenue], fact_ad_revenue[ad_medium] = "Digital")

Digital Revenue % =
    DIVIDE([Digital Revenue], [Total Net Revenue])

Print Revenue % =
    DIVIDE([Print Revenue], [Total Net Revenue])
```

## Digital Engagement (from fact_monthly_metrics)
```dax
Avg Unique Visitors K =
    AVERAGE(fact_monthly_metrics[unique_visitors_k])

Avg Bounce Rate =
    AVERAGE(fact_monthly_metrics[bounce_rate_pct])

Avg Session Duration =
    CALCULATE(
        AVERAGE(fact_monthly_metrics[avg_session_min]),
        NOT(ISBLANK(fact_monthly_metrics[avg_session_min]))
    )

Total Archive Licensing Revenue =
    SUM(fact_monthly_metrics[archive_licensing_egp])
```

## Cost & Profitability
```dax
Total Printing Cost =
    SUM(fact_monthly_metrics[printing_cost_egp])

Total IT Cost =
    SUM(fact_monthly_metrics[it_cost_egp])

Total Distribution Cost =
    SUM(fact_monthly_metrics[distribution_cost_egp])

IT Cost Growth % =
    DIVIDE(
        [Total IT Cost] - CALCULATE([Total IT Cost], SAMEPERIODLASTYEAR(dim_date[date])),
        CALCULATE([Total IT Cost], SAMEPERIODLASTYEAR(dim_date[date]))
    )
```

## Growth & Time Intelligence
```dax
YTD Net Revenue =
    TOTALYTD([Total Net Revenue], dim_date[date])

MoM Revenue Growth % =
    VAR Prev = CALCULATE([Total Net Revenue], DATEADD(dim_date[date], -1, MONTH))
    RETURN DIVIDE([Total Net Revenue] - Prev, Prev)

YoY Revenue Growth % =
    DIVIDE(
        [Total Net Revenue] - CALCULATE([Total Net Revenue], SAMEPERIODLASTYEAR(dim_date[date])),
        CALCULATE([Total Net Revenue], SAMEPERIODLASTYEAR(dim_date[date]))
    )

YoY Digital Revenue Growth % =
    DIVIDE(
        [Digital Revenue] - CALCULATE([Digital Revenue], SAMEPERIODLASTYEAR(dim_date[date])),
        CALCULATE([Digital Revenue], SAMEPERIODLASTYEAR(dim_date[date]))
    )

YoY Print Circulation Change % =
    DIVIDE(
        AVERAGE(fact_monthly_metrics[print_circulation_k]) -
        CALCULATE(AVERAGE(fact_monthly_metrics[print_circulation_k]),
                  SAMEPERIODLASTYEAR(dim_date[date])),
        CALCULATE(AVERAGE(fact_monthly_metrics[print_circulation_k]),
                  SAMEPERIODLASTYEAR(dim_date[date]))
    )
```

## Social Media
```dax
Latest FB Followers K =
    LASTNONBLANK(fact_monthly_metrics[fb_followers_k],
                 AVERAGE(fact_monthly_metrics[fb_followers_k]))

Avg Post Engagement % =
    AVERAGE(fact_monthly_metrics[post_engagement_pct])
```

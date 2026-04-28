# Suggested DAX Measures — Misr Insurance Company

## Financial KPIs
```dax
Total Premium Revenue =
    CALCULATE(
        SUM(fact_policies[premium_egp]),
        fact_policies[premium_egp] > 0
    )

Total Claims Paid =
    CALCULATE(
        SUM(fact_claims[amount_paid_egp]),
        fact_claims[claim_status] = "Approved"
    )

Total Underwriting Cost =
    SUM(fact_policies[underwriting_cost])

Total Admin Cost =
    SUM(fact_policies[admin_cost])

Total Cost =
    [Total Underwriting Cost] + [Total Admin Cost]

Net Profit =
    [Total Premium Revenue] - [Total Claims Paid] - [Total Cost]

Loss Ratio =
    DIVIDE([Total Claims Paid], [Total Premium Revenue])

Combined Ratio =
    DIVIDE([Total Claims Paid] + [Total Cost], [Total Premium Revenue])

Profit Margin % =
    DIVIDE([Net Profit], [Total Premium Revenue])
```

## Sales & Product KPIs
```dax
Total Policies Issued =
    COUNTROWS(fact_policies)

Active Policies =
    CALCULATE(COUNTROWS(fact_policies), fact_policies[policy_status] = "Active")

Cancellation Rate =
    DIVIDE(
        CALCULATE(COUNTROWS(fact_policies), fact_policies[policy_status] = "Cancelled"),
        [Total Policies Issued]
    )

Avg Premium per Policy =
    DIVIDE([Total Premium Revenue], [Total Policies Issued])

Revenue by Product =
    CALCULATE([Total Premium Revenue],
        ALLEXCEPT(dim_product, dim_product[product_id])
    )
```

## Claims & Operational KPIs
```dax
Total Claims Filed =
    COUNTROWS(fact_claims)

Claim Approval Rate =
    DIVIDE(
        CALCULATE(COUNTROWS(fact_claims), fact_claims[claim_status] = "Approved"),
        [Total Claims Filed]
    )

Claim Rejection Rate =
    DIVIDE(
        CALCULATE(COUNTROWS(fact_claims), fact_claims[claim_status] = "Rejected"),
        [Total Claims Filed]
    )

Avg Claim Processing Days =
    CALCULATE(
        AVERAGE(fact_claims[processing_days]),
        fact_claims[processing_days] > 0
    )

Claims per Month =
    DIVIDE([Total Claims Filed], DISTINCTCOUNT(dim_date[month]))
```

## Customer KPIs
```dax
Total Customers =
    DISTINCTCOUNT(fact_policies[customer_id])

Returning Customers =
    CALCULATE(
        DISTINCTCOUNT(fact_policies[customer_id]),
        fact_policies[is_returning_customer] = TRUE()
    )

Customer Retention Rate =
    DIVIDE([Returning Customers], [Total Customers])

New Customers =
    [Total Customers] - [Returning Customers]
```

## Growth & Time Intelligence
```dax
YTD Premium Revenue =
    TOTALYTD([Total Premium Revenue], dim_date[date])

MoM Premium Growth % =
    VAR Prev = CALCULATE([Total Premium Revenue], DATEADD(dim_date[date], -1, MONTH))
    RETURN DIVIDE([Total Premium Revenue] - Prev, Prev)

YoY Premium Growth % =
    DIVIDE(
        [Total Premium Revenue] - CALCULATE([Total Premium Revenue], SAMEPERIODLASTYEAR(dim_date[date])),
        CALCULATE([Total Premium Revenue], SAMEPERIODLASTYEAR(dim_date[date]))
    )
```

# Suggested DAX Measures — Banque du Caire

## Financial Performance
```dax
Total Transaction Volume =
    CALCULATE(
        SUM(fact_transactions[amount_egp]),
        fact_transactions[amount_egp] > 0
    )

Total Fee Revenue =
    SUM(fact_transactions[fee_egp])

Total Loan Portfolio =
    CALCULATE(
        SUM(fact_loans[principal_egp]),
        fact_loans[loan_status] = "Approved"
    )

Total NPL Value =
    CALCULATE(
        SUM(fact_loans[principal_egp]),
        fact_loans[is_npl] = TRUE()
    )

NPL Ratio =
    DIVIDE([Total NPL Value], [Total Loan Portfolio])
```

## Loan & Credit Performance
```dax
Total Loans =
    COUNTROWS(fact_loans)

Loan Approval Rate =
    DIVIDE(
        CALCULATE(COUNTROWS(fact_loans), fact_loans[loan_status] = "Approved"),
        [Total Loans]
    )

Loan Rejection Rate =
    DIVIDE(
        CALCULATE(COUNTROWS(fact_loans), fact_loans[loan_status] = "Rejected"),
        [Total Loans]
    )

Avg Interest Rate =
    AVERAGE(fact_loans[interest_rate])

Avg Loan Size =
    CALCULATE(
        AVERAGE(fact_loans[principal_egp]),
        fact_loans[loan_status] = "Approved"
    )
```

## Customer & Digital KPIs
```dax
Total Customers =
    DISTINCTCOUNT(fact_transactions[customer_id])

Digital Transactions =
    CALCULATE(COUNTROWS(fact_transactions), fact_transactions[is_digital] = TRUE())

Physical Transactions =
    CALCULATE(COUNTROWS(fact_transactions), fact_transactions[is_digital] = FALSE())

Digital Adoption Rate =
    DIVIDE([Digital Transactions], COUNTROWS(fact_transactions))

Avg Transactions per Customer =
    DIVIDE(COUNTROWS(fact_transactions), [Total Customers])
```

## Branch Performance
```dax
Revenue per Branch =
    DIVIDE([Total Fee Revenue], DISTINCTCOUNT(fact_transactions[branch_id]))

Transaction Volume by Branch =
    CALCULATE([Total Transaction Volume],
        ALLEXCEPT(dim_branch, dim_branch[branch_id])
    )
```

## Growth & Time Intelligence
```dax
YTD Transaction Volume =
    TOTALYTD([Total Transaction Volume], dim_date[date])

MoM Volume Growth % =
    VAR Prev = CALCULATE([Total Transaction Volume], DATEADD(dim_date[date], -1, MONTH))
    RETURN DIVIDE([Total Transaction Volume] - Prev, Prev)

YoY Volume Growth % =
    DIVIDE(
        [Total Transaction Volume] - CALCULATE([Total Transaction Volume], SAMEPERIODLASTYEAR(dim_date[date])),
        CALCULATE([Total Transaction Volume], SAMEPERIODLASTYEAR(dim_date[date]))
    )
```

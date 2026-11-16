# 09 · Cleaning and data quality

**Goal:** turn messy input into trustworthy data and report what was wrong.
**Exercise:** [`exercises/m09_data_quality.py`](../exercises/m09_data_quality.py)

`payments_raw` contains the problems you meet in real feeds:

| Problem | Example | Fix |
|---|---|---|
| Exact duplicate rows | `P2`, `P8` delivered twice | `dropDuplicates()` |
| Inconsistent values | `CARD`, `" wallet "` | `F.lower(F.trim(...))` |
| Everything is a string | `amount`, `paid_at` | `cast("double")`, `F.to_timestamp(col, fmt)` |
| Missing values | empty `amount`, empty `paid_at` | flag, do not guess |
| Orphan keys | `order_id = 9999` | `left_anti` join to the parent table |

## Clean, then check

1. **Standardise** types and formats in one step, so every later step sees the same data.
2. **Check** with explicit rules, each producing rows of `(record_id, issue)`.
3. **Split**: valid rows continue; failing rows go to a quarantine table with the reason.

```python
issues = (missing_amount
          .unionByName(missing_paid_at)
          .unionByName(unknown_order))
valid = payments.join(issues.select("payment_id").distinct(), "payment_id", "left_anti")
```

Keeping issues as data, rather than printing them, lets you count them per run, alert on thresholds
and show stakeholders exactly which records failed and why.

## Dedupe with care

`dropDuplicates()` with no arguments removes only rows that are identical in **every** column.
`dropDuplicates(["payment_id"])` keeps an arbitrary row per id. When versions differ, pick the winner
explicitly with `row_number()` ordered by a timestamp (module 05).

## Casting

With ANSI mode off (the Spark 3.x default), a value that cannot be cast becomes NULL silently. Count
NULLs before and after casting, or enable `spark.sql.ansi.enabled=true` to fail loudly instead.

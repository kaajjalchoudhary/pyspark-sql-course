# 04 · Window functions in SQL

**Goal:** calculate across related rows without collapsing them.
**Exercise:** [`exercises/m04_sql_window_functions.py`](../exercises/m04_sql_window_functions.py)

## Anatomy

```sql
function(...) OVER (
    PARTITION BY ...      -- which rows belong together
    ORDER BY ...          -- order inside the partition
    ROWS BETWEEN ...      -- the frame: which rows the function sees
)
```

`GROUP BY` returns one row per group. A window function returns one value **per input row**.

## Ranking

| Function | Ties | Example values |
|---|---|---|
| `ROW_NUMBER()` | always unique | 1, 2, 3, 4 |
| `RANK()` | shared, then a gap | 1, 2, 2, 4 |
| `DENSE_RANK()` | shared, no gap | 1, 2, 2, 3 |

"Top 3 products" → `ROW_NUMBER() <= 3`. "Products with the top 3 revenue values" → `DENSE_RANK() <= 3`.

## Offsets

```sql
LAG(order_date)  OVER (PARTITION BY customer_id ORDER BY order_date)  -- previous row
LEAD(order_date) OVER (PARTITION BY customer_id ORDER BY order_date)  -- next row
```

The first row of each partition has no previous row, so `LAG` returns NULL.

## Running totals and frames

```sql
SUM(daily_revenue) OVER (
    ORDER BY order_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
```

Write the frame explicitly. With `ORDER BY` and no frame, the default is `RANGE … CURRENT ROW`, which
treats rows with the same sort value as one: duplicate dates would jump together.

## Performance

A window with `PARTITION BY` shuffles rows so each partition sits together. A window with no
`PARTITION BY` moves **all** rows to a single task; fine for small results, a bottleneck on big ones.

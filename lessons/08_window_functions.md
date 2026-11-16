# 08 · Window functions in PySpark

**Goal:** use `Window` specifications for ranking, running totals and per-group context.
**Exercise:** [`exercises/m08_window_functions.py`](../exercises/m08_window_functions.py)

## Building a window

```python
from pyspark.sql import Window

w = Window.partitionBy("customer_id").orderBy("order_date")

orders.withColumn("order_number", F.row_number().over(w))
      .withColumn("prev_order",   F.lag("order_date").over(w))
```

## Frames matter for first and last

With `orderBy`, the default frame ends at the **current row**. So `F.last("order_date").over(w)` returns
the current row's date, not the customer's last order. Widen the frame:

```python
w_full = w.rowsBetween(Window.unboundedPreceding, Window.unboundedFollowing)
F.last("order_date").over(w_full)
```

## Share of total

```python
whole = Window.partitionBy()
revenue.withColumn("pct", F.round(100 * F.col("revenue") / F.sum("revenue").over(whole), 1))
```

An empty `partitionBy()` puts every row in one partition: correct, but it does not scale. On large data
compute the total with a separate aggregation and join (or `crossJoin`) it back.

## Window or groupBy?

- Need one row per group → `groupBy().agg()`.
- Need every row plus group context (rank, previous value, share) → a window.

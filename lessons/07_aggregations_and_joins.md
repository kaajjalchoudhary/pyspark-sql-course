# 07 · Aggregations, joins and pivots in PySpark

**Goal:** group, join and reshape data with the DataFrame API.
**Exercise:** [`exercises/m07_aggregations_and_joins.py`](../exercises/m07_aggregations_and_joins.py)

## groupBy and agg

```python
(orders.groupBy("country")
       .agg(F.count("*").alias("orders"),
            F.round(F.avg("order_value"), 2).alias("avg_order_value")))
```

Always alias aggregates; otherwise you get column names like `avg(order_value)`.

## Joins

```python
customers.join(orders, on="customer_id", how="left")
```

| `how` | Meaning |
|---|---|
| `"inner"` (default) | matching rows only |
| `"left"` | all left rows |
| `"left_semi"` | left rows with a match, left columns only |
| `"left_anti"` | left rows without a match |

Joining on a column **name** (`on="customer_id"`) keeps a single key column. Joining on an expression
(`customers.customer_id == orders.customer_id`) keeps both, and later references become ambiguous.

## Counting after a left join

`F.count("*")` counts the NULL row produced for an unmatched customer as 1.
`F.count("order_id")` ignores NULLs and correctly returns 0.

## Pivot

```python
(lines.groupBy("month")
      .pivot("category", ["Electronics", "Furniture", "Kitchen"])
      .agg(F.sum("revenue"))
      .fillna(0))
```

Pass the pivot values explicitly. Without them Spark runs an extra job to find the distinct values,
and the column set changes whenever the data does.

## Broadcast joins

When one side is small (a dimension table), `F.broadcast(small_df)` sends a copy to every executor so
the large side is not shuffled. Module 10 covers when this helps and when it hurts.

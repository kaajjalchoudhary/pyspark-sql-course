# 06 · DataFrame API basics

**Goal:** express the same logic in Python with the PySpark DataFrame API.
**Exercise:** [`exercises/m06_dataframe_basics.py`](../exercises/m06_dataframe_basics.py)

## SQL to DataFrame cheat sheet

| SQL | PySpark |
|---|---|
| `FROM orders` | `spark.table("orders")` |
| `SELECT a, b AS c` | `.select("a", F.col("b").alias("c"))` |
| `WHERE x = 1` | `.filter(F.col("x") == 1)` |
| new column | `.withColumn("total", F.col("q") * F.col("p"))` |
| `ORDER BY a DESC` | `.orderBy(F.col("a").desc())` |
| `CAST(x AS INT)` | `F.col("x").cast("int")` |
| `CASE WHEN … THEN … ELSE … END` | `F.when(cond, v).otherwise(other)` |

Import functions as `from pyspark.sql import functions as F`. Do not `from pyspark.sql.functions import *`:
it shadows Python built-ins such as `sum`, `min`, `max` and `round`.

## Combining conditions

```python
orders.filter((F.col("status") == "delivered") & (F.col("order_date") >= "2024-03-01"))
```

Use `&`, `|` and `~`, and wrap every condition in parentheses. Python's `and` / `or` raise an error.

## Lazy evaluation

Transformations (`select`, `filter`, `join`, `withColumn`) only build a plan. Nothing runs until an
**action**: `show()`, `count()`, `collect()`, `write`. This lets Spark optimise the whole plan, and it is
why an error in a transformation may only appear at the action.

## Schemas

Read files with an explicit schema (see `course.py`) instead of `inferSchema=True`. Inference needs an
extra pass over the data and can guess types differently from one file to the next.

## Avoid

- `collect()` on large data: it pulls every row into the driver's memory.
- Python UDFs when a built-in function exists: built-ins run inside the JVM and are much faster.
- Long chains of `withColumn` in a loop; use a single `select` with all the new columns.

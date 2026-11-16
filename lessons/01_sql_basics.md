# 01 · SQL basics: SELECT, WHERE, ORDER BY

**Goal:** read rows from a table, keep the ones you need and return them in a predictable order.
**Exercise:** [`exercises/m01_sql_basics.py`](../exercises/m01_sql_basics.py)

## How a query is evaluated

You write `SELECT … FROM … WHERE … ORDER BY`, but the engine evaluates it in a different order:

```
FROM  →  WHERE  →  GROUP BY  →  HAVING  →  SELECT  →  ORDER BY  →  LIMIT
```

This explains two common errors: you cannot use a `SELECT` alias inside `WHERE` (it does not exist yet),
but you can use it in `ORDER BY` (it does by then).

## Running SQL in Spark

```python
from course import get_spark, register_tables

spark = get_spark()
register_tables(spark)          # customers, products, orders, order_items, payments_raw
spark.sql("SELECT * FROM customers").show()
```

`spark.sql` returns a DataFrame, so SQL and the DataFrame API mix freely.

## Filtering

```sql
SELECT name, city
FROM customers
WHERE country = 'DE'            -- string literals use single quotes
  AND signup_date >= DATE '2024-03-01';
```

| Operator | Example | Note |
|---|---|---|
| `=`, `<>`, `<`, `>=` | `status <> 'cancelled'` | |
| `IN` | `country IN ('DE', 'AE')` | |
| `BETWEEN` | `unit_price BETWEEN 100 AND 300` | **inclusive** at both ends |
| `LIKE` | `name LIKE 'A%'` | `%` any characters, `_` one character |
| `IS NULL` | `amount IS NULL` | `= NULL` is never true |

## Dates: prefer half-open ranges

```sql
WHERE order_date >= DATE '2024-03-01'
  AND order_date <  DATE '2024-04-01'
```

This works whether the column is a `DATE` or a `TIMESTAMP`. `BETWEEN '2024-03-01' AND '2024-03-31'` silently
drops everything after midnight on the 31st when the column is a timestamp.

## Ordering

`ORDER BY` is the only guarantee of order. Without it Spark may return rows in any order, and the order
can change between runs. Add a tie-breaker when the sort key is not unique.

## Common mistakes

- Comparing with `NULL` using `=`.
- Relying on the order rows happen to come back in.
- Using `BETWEEN` on timestamps.

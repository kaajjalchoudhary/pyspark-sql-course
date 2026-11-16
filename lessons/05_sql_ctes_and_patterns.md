# 05 · CTEs and everyday patterns

**Goal:** write multi-step queries that are easy to read, test and review.
**Exercise:** [`exercises/m05_sql_ctes_and_patterns.py`](../exercises/m05_sql_ctes_and_patterns.py)

## Common table expressions

```sql
WITH monthly AS (
    SELECT DATE_FORMAT(order_date, 'yyyy-MM') AS month, SUM(...) AS revenue
    FROM ...
    GROUP BY 1
),
with_prev AS (
    SELECT month, revenue, LAG(revenue) OVER (ORDER BY month) AS prev_revenue
    FROM monthly
)
SELECT month, revenue, prev_revenue,
       ROUND(100 * (revenue - prev_revenue) / prev_revenue, 1) AS growth_pct
FROM with_prev;
```

Each CTE is one named step. You can debug by selecting from any step on its own.

## Pattern: latest record per key

```sql
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC, order_id DESC) AS rn
    FROM orders
)
SELECT * FROM ranked WHERE rn = 1;
```

Used everywhere: CDC feeds, re-delivered files, "current" state from a history table. The second
`ORDER BY` key makes the result deterministic when two rows share a date. Databricks SQL (and DuckDB,
Snowflake, BigQuery) can shorten this with `QUALIFY ROW_NUMBER() OVER (...) = 1`.

## Pattern: period over period

`LAG` over the period, then compute the change. Guard against division by zero with
`NULLIF(prev_revenue, 0)` when the previous value can be zero.

## Pattern: filter on an aggregate

Use `HAVING` (or a CTE plus `WHERE`) for questions like "customers with at least two delivered orders".

## More patterns

The companion repository [sql-patterns-for-data-engineers](https://github.com/kaajjalchoudhary/sql-patterns-for-data-engineers)
has 36 further patterns (gaps and islands, sessionization, SCD Type 2, snapshot diff and more), each
with data and a tested expected result.

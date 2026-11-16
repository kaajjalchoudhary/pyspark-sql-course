# 02 · Aggregation: GROUP BY and HAVING

**Goal:** turn many rows into one row per group.
**Exercise:** [`exercises/m02_sql_aggregation.py`](../exercises/m02_sql_aggregation.py)

## The rule of GROUP BY

Every column in `SELECT` must either be in `GROUP BY` or be inside an aggregate function.

```sql
SELECT country, COUNT(*) AS customers
FROM customers
GROUP BY country;
```

## Aggregate functions

| Function | Counts NULLs? |
|---|---|
| `COUNT(*)` | yes, counts rows |
| `COUNT(col)` | no, counts non-NULL values |
| `COUNT(DISTINCT col)` | no |
| `SUM`, `AVG`, `MIN`, `MAX` | ignore NULLs |

`AVG(col)` divides by the number of **non-NULL** values. If NULL should mean zero, use `AVG(COALESCE(col, 0))`.

## WHERE vs HAVING

- `WHERE` filters **rows** before grouping.
- `HAVING` filters **groups** after aggregation.

```sql
SELECT p.category, SUM(i.quantity) AS units
FROM orders o
JOIN order_items i ON i.order_id = o.order_id
JOIN products p    ON p.product_id = i.product_id
WHERE o.status = 'delivered'          -- row filter
GROUP BY p.category
HAVING SUM(i.quantity) >= 3           -- group filter
ORDER BY units DESC;
```

Filtering in `WHERE` whenever possible is also faster: fewer rows reach the shuffle that grouping needs.

## Grain

Before aggregating, ask: *what does one row represent?* In `order_items` one row is one product in one
order. Revenue per order means summing `quantity * unit_price` up to the order grain.

## Common mistakes

- `COUNT(*)` after a `LEFT JOIN` counts the unmatched row as 1. Use `COUNT(right_table.key)`.
- Mixing grains: joining orders to items and then summing an order-level column multiplies it.

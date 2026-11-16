# 03 · Joins

**Goal:** combine tables correctly, including rows that have no match.
**Exercise:** [`exercises/m03_sql_joins.py`](../exercises/m03_sql_joins.py)

## Join types

| Join | Keeps |
|---|---|
| `INNER JOIN` | only rows that match on both sides |
| `LEFT JOIN` | every left row; right columns are NULL when there is no match |
| `FULL OUTER JOIN` | every row from both sides |
| `LEFT SEMI JOIN` (Spark) | left rows that **have** a match, left columns only |
| `LEFT ANTI JOIN` (Spark) | left rows that have **no** match |

Semi and anti joins answer "exists / does not exist" questions without duplicating rows.

```sql
-- customers who never ordered
SELECT c.customer_id, c.name
FROM customers c
LEFT ANTI JOIN orders o ON o.customer_id = c.customer_id;
```

In standard SQL the same is written with `NOT EXISTS`. Avoid `NOT IN (subquery)`: if the subquery
returns a single NULL, it returns no rows at all.

## The ON vs WHERE trap

```sql
-- keeps customers with no delivered orders
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id AND o.status = 'delivered'

-- silently becomes an inner join: unmatched rows have status NULL and are filtered out
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.status = 'delivered'
```

Conditions on the right-hand table of a `LEFT JOIN` belong in `ON`.

## Fan-out

Joining a one-to-many relationship repeats the "one" side. Always check row counts before and after
a join; an unexpected increase usually means a duplicated key.

## Type mismatches

`payments_raw.order_id` is a string. Cast explicitly (`CAST(p.order_id AS INT)`) so the join compares
like with like and the intent is visible.

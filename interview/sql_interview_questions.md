# SQL interview questions for data engineers

Questions that come up repeatedly in data engineering interviews, with worked answers. Every query
runs against the course tables (`spark.sql(...)` after `register_tables(spark)`). Try each one before
opening the answer.

---

### 1. Find the second-highest product price.

<details><summary>Answer</summary>

```sql
SELECT product_name, unit_price
FROM (
    SELECT product_name, unit_price,
           DENSE_RANK() OVER (ORDER BY unit_price DESC) AS rnk
    FROM products
)
WHERE rnk = 2;
```

`DENSE_RANK` returns every product at the second-highest **price**, including ties. Interviewers often
follow up with "what if two products share the top price?": `ROW_NUMBER` would wrongly return one of
them, `RANK` could skip 2 entirely.
</details>

### 2. What is the difference between `WHERE` and `HAVING`?

<details><summary>Answer</summary>

`WHERE` filters rows before grouping and cannot reference aggregates. `HAVING` filters groups after
aggregation. Put every condition that does not need an aggregate in `WHERE`: fewer rows are grouped.
</details>

### 3. Find customers who have never placed an order. Give two ways.

<details><summary>Answer</summary>

```sql
-- 1. NOT EXISTS (portable)
SELECT c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);

-- 2. LEFT JOIN ... IS NULL
SELECT c.name FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL;
```

Avoid `NOT IN (SELECT customer_id FROM orders)`: one NULL in the subquery makes it return nothing.
In Spark, `LEFT ANTI JOIN` expresses the same intent directly.
</details>

### 4. Remove duplicates, keeping the latest row per key.

<details><summary>Answer</summary>

```sql
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC, order_id DESC) AS rn
    FROM orders
)
SELECT * FROM ranked WHERE rn = 1;
```

Mention the tie-breaker: without `order_id DESC`, two orders on the same day give a random winner.
</details>

### 5. Running total of revenue by day.

<details><summary>Answer</summary>

```sql
SELECT order_date, daily_revenue,
       SUM(daily_revenue) OVER (ORDER BY order_date
                                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_revenue
FROM daily_revenue;
```

State the frame explicitly; the default `RANGE` frame groups equal dates together.
</details>

### 6. `RANK` vs `DENSE_RANK` vs `ROW_NUMBER`?

<details><summary>Answer</summary>

For scores 100, 90, 90, 80: `ROW_NUMBER` 1,2,3,4 · `RANK` 1,2,2,4 · `DENSE_RANK` 1,2,2,3.
</details>

### 7. Month-over-month growth.

<details><summary>Answer</summary>

```sql
SELECT month, revenue,
       ROUND(100 * (revenue - LAG(revenue) OVER (ORDER BY month))
             / NULLIF(LAG(revenue) OVER (ORDER BY month), 0), 1) AS growth_pct
FROM monthly_revenue;
```

`NULLIF(..., 0)` prevents division by zero; the first month is NULL because it has no previous month.
</details>

### 8. Why might `COUNT(*)` and `COUNT(column)` differ?

<details><summary>Answer</summary>

`COUNT(*)` counts rows; `COUNT(column)` counts non-NULL values. After a `LEFT JOIN`, use
`COUNT(right.key)` so unmatched rows count as 0, not 1.
</details>

### 9. A `LEFT JOIN` returns fewer rows than the left table. How?

<details><summary>Answer</summary>

It cannot on its own, so a later filter is the cause: usually a `WHERE` condition on a right-table
column, which removes the NULL rows and turns the query into an inner join. Move the condition into
`ON`. (More rows than the left table means duplicate keys on the right: a fan-out.)
</details>

### 10. Products bought together: count order pairs.

<details><summary>Answer</summary>

```sql
SELECT a.product_id AS product_a, b.product_id AS product_b, COUNT(*) AS orders_together
FROM order_items a
JOIN order_items b ON a.order_id = b.order_id AND a.product_id < b.product_id
GROUP BY a.product_id, b.product_id
ORDER BY orders_together DESC;
```

`a.product_id < b.product_id` keeps each pair once and drops self-pairs.
</details>

### 11. How would you prove a load into the warehouse is complete?

<details><summary>Answer</summary>

Reconcile source and target per business date: row counts, sums of key measures and distinct key
counts, compared with a `FULL OUTER JOIN` of the two aggregates so days missing on either side show up.
Store the result as a table and alert on any mismatch.
</details>

### 12. Gaps and islands: find streaks of consecutive days.

<details><summary>Answer</summary>

Subtract a `ROW_NUMBER()` (in days) from the date. Consecutive dates share the same result, which
becomes the group key:

```sql
SELECT user_id, MIN(d) AS streak_start, MAX(d) AS streak_end, COUNT(*) AS days
FROM (
    SELECT user_id, d,
           DATE_SUB(d, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY d)) AS grp
    FROM (SELECT DISTINCT user_id, login_date AS d FROM logins)
)
GROUP BY user_id, grp;
```
</details>

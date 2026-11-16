# PySpark interview questions for data engineers

Conceptual and hands-on questions with worked answers. Code runs against the course tables.

---

### 1. What is lazy evaluation, and why does Spark use it?

<details><summary>Answer</summary>

Transformations (`select`, `filter`, `join`) only build a logical plan; nothing executes until an action
(`count`, `collect`, `show`, `write`). Seeing the whole plan lets the Catalyst optimiser push filters
down, prune columns, reorder operations and pick join strategies before any data moves.
</details>

### 2. Narrow vs wide transformations?

<details><summary>Answer</summary>

Narrow (`filter`, `select`, `withColumn`): each output partition depends on one input partition, no
data movement. Wide (`groupBy`, `join`, `distinct`, `orderBy`): rows must be redistributed by key, which
causes a **shuffle**: disk and network I/O and a new stage. Most tuning is about reducing shuffles.
</details>

### 3. `repartition` vs `coalesce`?

<details><summary>Answer</summary>

`repartition(n)` does a full shuffle and can increase or decrease partitions, optionally by column.
`coalesce(n)` only merges existing partitions without a shuffle, so it can only decrease them and may
leave them uneven. Use `coalesce` before writing to avoid many small files.
</details>

### 4. When should you use a broadcast join?

<details><summary>Answer</summary>

When one side is small enough to fit in each executor's memory (a dimension table). The small side is
copied to every executor and the large side is not shuffled.

```python
order_items.join(F.broadcast(products), "product_id")
```

Spark broadcasts automatically below `spark.sql.autoBroadcastJoinThreshold` (10 MB default). Broadcasting
something large causes out-of-memory errors.
</details>

### 5. What is data skew and how do you handle it?

<details><summary>Answer</summary>

A few keys hold most of the rows, so a few tasks do most of the work. Detect it in the Spark UI
(one task much slower, much larger shuffle read). Fixes: enable AQE skew-join handling, filter or
separately handle NULL / hot keys, broadcast the other side, or salt the key (append a random suffix,
aggregate in two steps).
</details>

### 6. Count orders per customer, including customers with none.

<details><summary>Answer</summary>

```python
(customers.join(orders, "customer_id", "left")
          .groupBy("customer_id", "name")
          .agg(F.count("order_id").alias("order_count")))
```

`F.count("order_id")` skips the NULL produced for unmatched customers; `F.count("*")` would return 1.
</details>

### 7. Keep the latest record per key in PySpark.

<details><summary>Answer</summary>

```python
w = Window.partitionBy("customer_id").orderBy(F.col("order_date").desc(), F.col("order_id").desc())
latest = orders.withColumn("rn", F.row_number().over(w)).filter("rn = 1").drop("rn")
```

`dropDuplicates(["customer_id"])` is not equivalent: it keeps an arbitrary row.
</details>

### 8. Why avoid Python UDFs?

<details><summary>Answer</summary>

Each row is serialised from the JVM to a Python worker and back, and the optimiser cannot see inside
the function. Built-in functions in `pyspark.sql.functions` run in the JVM and are optimised. If a UDF
is unavoidable, a vectorised `pandas_udf` (Arrow) is much faster than a row-at-a-time UDF.
</details>

### 9. `cache()` vs `persist()`?

<details><summary>Answer</summary>

`cache()` is `persist()` with the default storage level (memory and disk for DataFrames). `persist()`
lets you choose the level. Both are lazy: the data is stored at the first action. Cache only data reused
by several actions, and `unpersist()` afterwards.
</details>

### 10. How do you make a pipeline idempotent?

<details><summary>Answer</summary>

Re-running it for the same input must give the same result without duplicates. Common techniques:
overwrite a specific partition (`partitionOverwriteMode=dynamic`) instead of appending, `MERGE` on a
business key (Delta Lake, Iceberg), deterministic dedupe before writing, and checkpoints for streaming.
</details>

### 11. What does Adaptive Query Execution do?

<details><summary>Answer</summary>

AQE (on by default since Spark 3.2) re-optimises the plan at runtime using real shuffle statistics: it
coalesces small shuffle partitions, switches a sort-merge join to a broadcast join when one side turns
out small, and splits skewed partitions in joins.
</details>

### 12. A job became slow after the data doubled. Where do you look first?

<details><summary>Answer</summary>

1. The Spark UI: which stage is slow, and is the time spread evenly across tasks (volume) or
   concentrated in a few (skew)?
2. `explain()`: unexpected `SortMergeJoin` where a broadcast was expected, filters not pushed down,
   repeated scans of the same source.
3. Shuffle partition count and size, spill to disk, and small-file problems on the input.
</details>

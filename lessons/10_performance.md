# 10 · Performance basics

**Goal:** read a query plan and recognise the few things that make most Spark jobs slow.
**Exercise:** [`exercises/m10_performance.py`](../exercises/m10_performance.py)

## Reading a plan

```python
df.explain()            # physical plan
df.explain("formatted") # easier to read
```

Look for `Exchange` (a shuffle), the join strategy (`BroadcastHashJoin`, `SortMergeJoin`) and whether
filters are pushed down into the file scan (`PushedFilters`).

## Shuffles

Wide operations (`groupBy`, `join`, `distinct`, `orderBy`, windows with `partitionBy`) move data
between executors over the network. They are usually the most expensive part of a job.

- Filter and select early, so less data is shuffled.
- `spark.sql.shuffle.partitions` (default 200) sets the partitions after a shuffle; with Adaptive Query
  Execution (on by default in Spark 3.2+) Spark coalesces small partitions for you.

## Broadcast joins

```python
order_items.join(F.broadcast(products), "product_id")
```

The small table is copied to every executor; the large table is not shuffled. Spark does this
automatically below `spark.sql.autoBroadcastJoinThreshold` (10 MB by default). Broadcasting a table
that is too large causes driver or executor out-of-memory errors.

## Skew

If one key holds most of the rows (one huge customer, `NULL` keys), one task does most of the work.
Signs: one task far slower than the rest in the Spark UI. Remedies: AQE skew join handling, filtering
NULL keys before the join, or salting the key.

## Partitions and files

- `repartition(n, col)` shuffles into `n` partitions by hash of `col`.
- `coalesce(n)` reduces partitions **without** a shuffle; use it to avoid writing many small files.
- Write large tables partitioned by a low-cardinality column used in filters (for example a date).

## Caching

`df.cache()` helps only when the same DataFrame is used by several actions. Cache after expensive
steps, and `unpersist()` when done.

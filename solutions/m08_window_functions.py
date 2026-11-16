"""Module 08 · Window functions with the DataFrame API. Lesson: lessons/08_window_functions.md"""

from pyspark.sql import DataFrame, SparkSession, Window
from pyspark.sql import functions as F


def q1_revenue_share(spark: SparkSession) -> DataFrame:
    """Each customer's share of total delivered revenue (customers with revenue only).

    Columns: name, revenue, pct_of_total (1 dp). Ordered by revenue descending.
    An empty Window.partitionBy() spans the whole DataFrame: fine for small results,
    but it moves every row to one partition, so avoid it on big data.
    """
    revenue = (
        spark.table("orders").filter(F.col("status") == "delivered")
        .join(spark.table("order_items"), "order_id")
        .join(spark.table("products"), "product_id")
        .join(spark.table("customers"), "customer_id")
        .groupBy("customer_id", "name")
        .agg(F.sum(F.col("quantity") * F.col("unit_price")).alias("revenue"))
    )
    whole = Window.partitionBy()
    return (
        revenue.withColumn("pct_of_total", F.round(100 * F.col("revenue") / F.sum("revenue").over(whole), 1))
        .select("name", "revenue", "pct_of_total")
        .orderBy(F.col("revenue").desc())
    )


def q2_customer_order_history(spark: SparkSession) -> DataFrame:
    """One row per customer who ordered: customer_id, first_order, last_order, order_count.

    Built with window functions (first, last over a full frame, count) and then deduplicated,
    to practise frames: with ORDER BY, the default frame stops at the current row, so
    last() would return the current row. The frame is widened explicitly.
    """
    w = (
        Window.partitionBy("customer_id").orderBy("order_date")
        .rowsBetween(Window.unboundedPreceding, Window.unboundedFollowing)
    )
    return (
        spark.table("orders")
        .select(
            "customer_id",
            F.first("order_date").over(w).alias("first_order"),
            F.last("order_date").over(w).alias("last_order"),
            F.count("*").over(w).alias("order_count"),
        )
        .dropDuplicates(["customer_id"])
        .orderBy("customer_id")
    )

"""Module 10 · Performance basics: partitions, shuffles and broadcast joins. Lesson: lessons/10_performance.md"""

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F


def q1_broadcast_join(spark: SparkSession) -> DataFrame:
    """Join order_items to products so Spark uses a broadcast hash join (no shuffle of order_items).

    Columns: order_id, product_name, quantity.
    """
    return (
        spark.table("order_items")
        .join(F.broadcast(spark.table("products")), "product_id")
        .select("order_id", "product_name", "quantity")
    )


def q2_repartition_by_customer(spark: SparkSession) -> DataFrame:
    """Return orders hash-partitioned by customer_id into exactly 4 partitions."""
    return spark.table("orders").repartition(4, "customer_id")

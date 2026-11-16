"""Module 06 · DataFrame API basics. Lesson: lessons/06_dataframe_basics.md

From here on, use the DataFrame API (spark.table, select, withColumn, filter), not spark.sql.
"""

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F


def q1_order_calendar(spark: SparkSession) -> DataFrame:
    """Columns: order_id, order_year, order_month, is_delivered (boolean). Ordered by order_id."""
    return (
        spark.table("orders")
        .select(
            "order_id",
            F.year("order_date").alias("order_year"),
            F.month("order_date").alias("order_month"),
            (F.col("status") == "delivered").alias("is_delivered"),
        )
        .orderBy("order_id")
    )


def q2_line_totals(spark: SparkSession) -> DataFrame:
    """One row per order line. Columns: order_id, product_name, line_total (quantity * unit_price, 2 dp)."""
    items = spark.table("order_items")
    products = spark.table("products")
    return (
        items.join(products, on="product_id", how="inner")
        .withColumn("line_total", F.round(F.col("quantity") * F.col("unit_price"), 2))
        .select("order_id", "product_name", "line_total")
        .orderBy("order_id", "product_name")
    )

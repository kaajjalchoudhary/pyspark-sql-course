"""Module 07 · Aggregations, joins and pivots with the DataFrame API. Lesson: lessons/07_aggregations_and_joins.md"""

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F


def _order_values(spark: SparkSession) -> DataFrame:
    """Value of every order: order_id, customer_id, order_date, status, order_value."""
    items = spark.table("order_items").join(spark.table("products"), "product_id")
    values = items.groupBy("order_id").agg(F.sum(F.col("quantity") * F.col("unit_price")).alias("order_value"))
    return spark.table("orders").join(values, "order_id")


def q1_avg_order_value_by_country(spark: SparkSession) -> DataFrame:
    """Delivered orders per country. Columns: country, orders, avg_order_value (2 dp). Ordered by country."""
    delivered = _order_values(spark).filter(F.col("status") == "delivered")
    return (
        delivered.join(spark.table("customers").select("customer_id", "country"), "customer_id")
        .groupBy("country")
        .agg(
            F.count("*").alias("orders"),
            F.round(F.avg("order_value"), 2).alias("avg_order_value"),
        )
        .orderBy("country")
    )


def q2_monthly_revenue_by_category(spark: SparkSession) -> DataFrame:
    """Delivered revenue pivoted by category, one row per month ('yyyy-MM'), missing values as 0.

    Columns: month, Electronics, Furniture, Kitchen. Passing the pivot values explicitly
    saves Spark an extra job to discover them and fixes the column order.
    """
    lines = (
        spark.table("orders").filter(F.col("status") == "delivered")
        .join(spark.table("order_items"), "order_id")
        .join(spark.table("products"), "product_id")
        .withColumn("month", F.date_format("order_date", "yyyy-MM"))
        .withColumn("revenue", F.col("quantity") * F.col("unit_price"))
    )
    return (
        lines.groupBy("month")
        .pivot("category", ["Electronics", "Furniture", "Kitchen"])
        .agg(F.sum("revenue"))
        .fillna(0)
        .orderBy("month")
    )


def q3_order_count_per_customer(spark: SparkSession) -> DataFrame:
    """Every customer with their number of orders (0 if none). Columns: name, order_count.

    Ordered by customer_id. count("order_id") ignores the NULLs a left join produces,
    so customers without orders correctly get 0 (count("*") would give 1).
    """
    customers = spark.table("customers")
    return (
        customers.join(spark.table("orders"), "customer_id", "left")
        .groupBy("customer_id", "name")
        .agg(F.count("order_id").alias("order_count"))
        .orderBy("customer_id")
        .select("name", "order_count")
    )

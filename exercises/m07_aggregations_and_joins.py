"""Module 07 · Aggregations, joins and pivots with the DataFrame API. Lesson: lessons/07_aggregations_and_joins.md

Your turn: replace each NotImplementedError with your answer, then run
    COURSE_TARGET=exercises pytest -k m07_aggregations_and_joins
Stuck? Compare with solutions/m07_aggregations_and_joins.py only after a real attempt.
"""

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F


def q1_avg_order_value_by_country(spark: SparkSession) -> DataFrame:
    """Delivered orders per country. Columns: country, orders, avg_order_value (2 dp). Ordered by country."""
    raise NotImplementedError("Write your answer here")


def q2_monthly_revenue_by_category(spark: SparkSession) -> DataFrame:
    """Delivered revenue pivoted by category, one row per month ('yyyy-MM'), missing values as 0.

    Columns: month, Electronics, Furniture, Kitchen. Passing the pivot values explicitly
    saves Spark an extra job to discover them and fixes the column order.
    """
    raise NotImplementedError("Write your answer here")


def q3_order_count_per_customer(spark: SparkSession) -> DataFrame:
    """Every customer with their number of orders (0 if none). Columns: name, order_count.

    Ordered by customer_id. count("order_id") ignores the NULLs a left join produces,
    so customers without orders correctly get 0 (count("*") would give 1).
    """
    raise NotImplementedError("Write your answer here")

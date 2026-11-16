"""Module 05 · CTEs and everyday patterns (Spark SQL). Lesson: lessons/05_sql_ctes_and_patterns.md

Your turn: replace each NotImplementedError with your answer, then run
    COURSE_TARGET=exercises pytest -k m05_sql_ctes_and_patterns
Stuck? Compare with solutions/m05_sql_ctes_and_patterns.py only after a real attempt.
"""

from pyspark.sql import DataFrame, SparkSession


def q1_latest_order_per_customer(spark: SparkSession) -> DataFrame:
    """Each customer's most recent order. Columns: customer_id, order_id, order_date."""
    raise NotImplementedError("Write your answer here")


def q2_month_over_month(spark: SparkSession) -> DataFrame:
    """Delivered revenue per month with growth versus the previous month.

    Columns: month ('yyyy-MM'), revenue, prev_revenue, growth_pct (rounded to 1 decimal).
    """
    raise NotImplementedError("Write your answer here")


def q3_repeat_buyers(spark: SparkSession) -> DataFrame:
    """Customers with at least 2 delivered orders. Columns: name, delivered_orders."""
    raise NotImplementedError("Write your answer here")

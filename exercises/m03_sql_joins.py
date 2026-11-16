"""Module 03 · Joins: inner, left, anti (Spark SQL). Lesson: lessons/03_sql_joins.md

Your turn: replace each NotImplementedError with your answer, then run
    COURSE_TARGET=exercises pytest -k m03_sql_joins
Stuck? Compare with solutions/m03_sql_joins.py only after a real attempt.
"""

from pyspark.sql import DataFrame, SparkSession


def q1_customers_without_orders(spark: SparkSession) -> DataFrame:
    """customer_id and name of customers who never placed an order."""
    raise NotImplementedError("Write your answer here")


def q2_revenue_per_customer(spark: SparkSession) -> DataFrame:
    """Delivered revenue per customer, keeping customers with no delivered orders at 0.

    Columns: name, revenue. The status filter sits in the ON clause: in WHERE it would
    turn the LEFT JOIN back into an inner join and drop the zero-revenue customers.
    """
    raise NotImplementedError("Write your answer here")


def q3_orders_without_payment(spark: SparkSession) -> DataFrame:
    """order_id and status of orders with no row in payments_raw (its order_id is a string)."""
    raise NotImplementedError("Write your answer here")

"""Module 04 · Window functions (Spark SQL). Lesson: lessons/04_sql_window_functions.md

Your turn: replace each NotImplementedError with your answer, then run
    COURSE_TARGET=exercises pytest -k m04_sql_window_functions
Stuck? Compare with solutions/m04_sql_window_functions.py only after a real attempt.
"""

from pyspark.sql import DataFrame, SparkSession


def q1_product_rank_in_category(spark: SparkSession) -> DataFrame:
    """Rank products by revenue inside their category, ignoring cancelled orders.

    Columns: category, product_name, revenue, rank_in_category (dense_rank, 1 = best).
    """
    raise NotImplementedError("Write your answer here")


def q2_running_revenue(spark: SparkSession) -> DataFrame:
    """Daily delivered revenue and its running total. Columns: order_date, daily_revenue, running_revenue."""
    raise NotImplementedError("Write your answer here")


def q3_days_since_previous_order(spark: SparkSession) -> DataFrame:
    """For every order, days since the same customer's previous order (NULL for the first).

    Columns: customer_id, order_id, order_date, days_since_prev.
    """
    raise NotImplementedError("Write your answer here")

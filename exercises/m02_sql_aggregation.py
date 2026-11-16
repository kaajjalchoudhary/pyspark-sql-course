"""Module 02 · Aggregation: GROUP BY, HAVING (Spark SQL). Lesson: lessons/02_sql_aggregation.md

Your turn: replace each NotImplementedError with your answer, then run
    COURSE_TARGET=exercises pytest -k m02_sql_aggregation
Stuck? Compare with solutions/m02_sql_aggregation.py only after a real attempt.
"""

from pyspark.sql import DataFrame, SparkSession


def q1_customers_per_country(spark: SparkSession) -> DataFrame:
    """country and number of customers (column: customers), ordered by country."""
    raise NotImplementedError("Write your answer here")


def q2_order_revenue(spark: SparkSession) -> DataFrame:
    """Revenue of every order (sum of quantity * unit_price). Columns: order_id, revenue."""
    raise NotImplementedError("Write your answer here")


def q3_popular_categories(spark: SparkSession) -> DataFrame:
    """Categories with at least 3 units sold in delivered orders. Columns: category, units.

    WHERE filters rows before grouping; HAVING filters groups after aggregation.
    """
    raise NotImplementedError("Write your answer here")

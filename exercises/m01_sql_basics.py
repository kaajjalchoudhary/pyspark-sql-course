"""Module 01 · SQL basics: SELECT, WHERE, ORDER BY (Spark SQL). Lesson: lessons/01_sql_basics.md

Your turn: replace each NotImplementedError with your answer, then run
    COURSE_TARGET=exercises pytest -k m01_sql_basics
Stuck? Compare with solutions/m01_sql_basics.py only after a real attempt.
"""

from pyspark.sql import DataFrame, SparkSession


def q1_german_customers(spark: SparkSession) -> DataFrame:
    """Name and city of every customer in Germany (country = 'DE'), ordered by name."""
    raise NotImplementedError("Write your answer here")


def q2_delivered_in_march(spark: SparkSession) -> DataFrame:
    """order_id and order_date of delivered orders placed in March 2024, ordered by order_id."""
    raise NotImplementedError("Write your answer here")


def q3_mid_priced_products(spark: SparkSession) -> DataFrame:
    """product_name and unit_price of products priced 100 to 300 (inclusive), most expensive first."""
    raise NotImplementedError("Write your answer here")

"""Module 06 · DataFrame API basics. Lesson: lessons/06_dataframe_basics.md

From here on, use the DataFrame API (spark.table, select, withColumn, filter), not spark.sql.

Your turn: replace each NotImplementedError with your answer, then run
    COURSE_TARGET=exercises pytest -k m06_dataframe_basics
Stuck? Compare with solutions/m06_dataframe_basics.py only after a real attempt.
"""

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F


def q1_order_calendar(spark: SparkSession) -> DataFrame:
    """Columns: order_id, order_year, order_month, is_delivered (boolean). Ordered by order_id."""
    raise NotImplementedError("Write your answer here")


def q2_line_totals(spark: SparkSession) -> DataFrame:
    """One row per order line. Columns: order_id, product_name, line_total (quantity * unit_price, 2 dp)."""
    raise NotImplementedError("Write your answer here")

"""Module 10 · Performance basics: partitions, shuffles and broadcast joins. Lesson: lessons/10_performance.md

Your turn: replace each NotImplementedError with your answer, then run
    COURSE_TARGET=exercises pytest -k m10_performance
Stuck? Compare with solutions/m10_performance.py only after a real attempt.
"""

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F


def q1_broadcast_join(spark: SparkSession) -> DataFrame:
    """Join order_items to products so Spark uses a broadcast hash join (no shuffle of order_items).

    Columns: order_id, product_name, quantity.
    """
    raise NotImplementedError("Write your answer here")


def q2_repartition_by_customer(spark: SparkSession) -> DataFrame:
    """Return orders hash-partitioned by customer_id into exactly 4 partitions."""
    raise NotImplementedError("Write your answer here")

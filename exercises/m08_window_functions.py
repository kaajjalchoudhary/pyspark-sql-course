"""Module 08 · Window functions with the DataFrame API. Lesson: lessons/08_window_functions.md

Your turn: replace each NotImplementedError with your answer, then run
    COURSE_TARGET=exercises pytest -k m08_window_functions
Stuck? Compare with solutions/m08_window_functions.py only after a real attempt.
"""

from pyspark.sql import DataFrame, SparkSession, Window
from pyspark.sql import functions as F


def q1_revenue_share(spark: SparkSession) -> DataFrame:
    """Each customer's share of total delivered revenue (customers with revenue only).

    Columns: name, revenue, pct_of_total (1 dp). Ordered by revenue descending.
    An empty Window.partitionBy() spans the whole DataFrame: fine for small results,
    but it moves every row to one partition, so avoid it on big data.
    """
    raise NotImplementedError("Write your answer here")


def q2_customer_order_history(spark: SparkSession) -> DataFrame:
    """One row per customer who ordered: customer_id, first_order, last_order, order_count.

    Built with window functions (first, last over a full frame, count) and then deduplicated,
    to practise frames: with ORDER BY, the default frame stops at the current row, so
    last() would return the current row. The frame is widened explicitly.
    """
    raise NotImplementedError("Write your answer here")

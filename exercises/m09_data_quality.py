"""Module 09 · Cleaning and data quality on messy input. Lesson: lessons/09_data_quality.md

payments_raw is deliberately messy: exact duplicate rows, inconsistent casing and spaces in
method, a missing amount, a missing timestamp and a payment for an order that does not exist.

Your turn: replace each NotImplementedError with your answer, then run
    COURSE_TARGET=exercises pytest -k m09_data_quality
Stuck? Compare with solutions/m09_data_quality.py only after a real attempt.
"""

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F


def q1_clean_payments(spark: SparkSession) -> DataFrame:
    """Drop exact duplicates, normalise method (trim + lower), cast amount to double,
    paid_at to timestamp and order_id to int. Keep all columns."""
    raise NotImplementedError("Write your answer here")


def q2_quality_issues(spark: SparkSession) -> DataFrame:
    """One row per problem found in the cleaned payments. Columns: payment_id, issue.

    issue is one of: missing_amount, missing_paid_at, unknown_order.
    """
    raise NotImplementedError("Write your answer here")


def q3_valid_payment_summary(spark: SparkSession) -> DataFrame:
    """Only payments with no issues. One row: valid_payments, total_amount."""
    raise NotImplementedError("Write your answer here")

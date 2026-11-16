"""Module 09 · Cleaning and data quality on messy input. Lesson: lessons/09_data_quality.md

payments_raw is deliberately messy: exact duplicate rows, inconsistent casing and spaces in
method, a missing amount, a missing timestamp and a payment for an order that does not exist.
"""

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F


def q1_clean_payments(spark: SparkSession) -> DataFrame:
    """Drop exact duplicates, normalise method (trim + lower), cast amount to double,
    paid_at to timestamp and order_id to int. Keep all columns."""
    return (
        spark.table("payments_raw")
        .dropDuplicates()
        .withColumn("method", F.lower(F.trim("method")))
        .withColumn("order_id", F.col("order_id").cast("int"))
        .withColumn("amount", F.col("amount").cast("double"))
        .withColumn("paid_at", F.to_timestamp("paid_at", "yyyy-MM-dd HH:mm:ss"))
    )


def q2_quality_issues(spark: SparkSession) -> DataFrame:
    """One row per problem found in the cleaned payments. Columns: payment_id, issue.

    issue is one of: missing_amount, missing_paid_at, unknown_order.
    """
    payments = q1_clean_payments(spark)
    orders = spark.table("orders").select("order_id")
    missing_amount = payments.filter(F.col("amount").isNull()).select("payment_id", F.lit("missing_amount").alias("issue"))
    missing_paid_at = payments.filter(F.col("paid_at").isNull()).select("payment_id", F.lit("missing_paid_at").alias("issue"))
    unknown_order = payments.join(orders, "order_id", "left_anti").select("payment_id", F.lit("unknown_order").alias("issue"))
    return missing_amount.unionByName(missing_paid_at).unionByName(unknown_order).orderBy("payment_id", "issue")


def q3_valid_payment_summary(spark: SparkSession) -> DataFrame:
    """Only payments with no issues. One row: valid_payments, total_amount."""
    payments = q1_clean_payments(spark)
    bad = q2_quality_issues(spark).select("payment_id").distinct()
    valid = payments.join(bad, "payment_id", "left_anti")
    return valid.agg(
        F.count("*").alias("valid_payments"),
        F.round(F.sum("amount"), 2).alias("total_amount"),
    )

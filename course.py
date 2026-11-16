"""Shared helpers for the course: a local SparkSession and the sample tables.

Every exercise receives a SparkSession whose catalog already has these views:
customers, products, orders, order_items, payments_raw
"""

from __future__ import annotations

from pathlib import Path

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import (
    DateType,
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

DATA = Path(__file__).resolve().parent / "data"

SCHEMAS = {
    "customers": StructType([
        StructField("customer_id", IntegerType()),
        StructField("name", StringType()),
        StructField("city", StringType()),
        StructField("country", StringType()),
        StructField("signup_date", DateType()),
    ]),
    "products": StructType([
        StructField("product_id", IntegerType()),
        StructField("product_name", StringType()),
        StructField("category", StringType()),
        StructField("unit_price", DoubleType()),
    ]),
    "orders": StructType([
        StructField("order_id", IntegerType()),
        StructField("customer_id", IntegerType()),
        StructField("order_date", DateType()),
        StructField("status", StringType()),
    ]),
    "order_items": StructType([
        StructField("order_id", IntegerType()),
        StructField("product_id", IntegerType()),
        StructField("quantity", IntegerType()),
    ]),
    # Deliberately messy: kept as strings so the data-quality module can clean it.
    "payments_raw": StructType([
        StructField("payment_id", StringType()),
        StructField("order_id", StringType()),
        StructField("method", StringType()),
        StructField("amount", StringType()),
        StructField("paid_at", StringType()),
    ]),
}


def get_spark(app_name: str = "pyspark-sql-course") -> SparkSession:
    """A small local session: 1 core keeps results deterministic and fast on a laptop."""
    return (
        SparkSession.builder.master("local[1]")
        .appName(app_name)
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )


def load_table(spark: SparkSession, name: str) -> DataFrame:
    return spark.read.csv(
        str(DATA / f"{name}.csv"),
        header=True,
        schema=SCHEMAS[name],
        ignoreLeadingWhiteSpace=False,
        ignoreTrailingWhiteSpace=False,
    )


def register_tables(spark: SparkSession) -> None:
    """Register every sample table as a temp view so Spark SQL can query it."""
    for name in SCHEMAS:
        load_table(spark, name).createOrReplaceTempView(name)

"""Module 01 · SQL basics: SELECT, WHERE, ORDER BY (Spark SQL). Lesson: lessons/01_sql_basics.md"""

from pyspark.sql import DataFrame, SparkSession


def q1_german_customers(spark: SparkSession) -> DataFrame:
    """Name and city of every customer in Germany (country = 'DE'), ordered by name."""
    return spark.sql("""
        SELECT name, city
        FROM customers
        WHERE country = 'DE'
        ORDER BY name
    """)


def q2_delivered_in_march(spark: SparkSession) -> DataFrame:
    """order_id and order_date of delivered orders placed in March 2024, ordered by order_id."""
    return spark.sql("""
        SELECT order_id, order_date
        FROM orders
        WHERE status = 'delivered'
          AND order_date >= DATE '2024-03-01'
          AND order_date <  DATE '2024-04-01'   -- half-open range: safe for dates and timestamps
        ORDER BY order_id
    """)


def q3_mid_priced_products(spark: SparkSession) -> DataFrame:
    """product_name and unit_price of products priced 100 to 300 (inclusive), most expensive first."""
    return spark.sql("""
        SELECT product_name, unit_price
        FROM products
        WHERE unit_price BETWEEN 100 AND 300
        ORDER BY unit_price DESC
    """)

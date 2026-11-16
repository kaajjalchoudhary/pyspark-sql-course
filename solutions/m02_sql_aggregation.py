"""Module 02 · Aggregation: GROUP BY, HAVING (Spark SQL). Lesson: lessons/02_sql_aggregation.md"""

from pyspark.sql import DataFrame, SparkSession


def q1_customers_per_country(spark: SparkSession) -> DataFrame:
    """country and number of customers (column: customers), ordered by country."""
    return spark.sql("""
        SELECT country, COUNT(*) AS customers
        FROM customers
        GROUP BY country
        ORDER BY country
    """)


def q2_order_revenue(spark: SparkSession) -> DataFrame:
    """Revenue of every order (sum of quantity * unit_price). Columns: order_id, revenue."""
    return spark.sql("""
        SELECT i.order_id, ROUND(SUM(i.quantity * p.unit_price), 2) AS revenue
        FROM order_items AS i
        JOIN products AS p ON p.product_id = i.product_id
        GROUP BY i.order_id
        ORDER BY i.order_id
    """)


def q3_popular_categories(spark: SparkSession) -> DataFrame:
    """Categories with at least 3 units sold in delivered orders. Columns: category, units.

    WHERE filters rows before grouping; HAVING filters groups after aggregation.
    """
    return spark.sql("""
        SELECT p.category, SUM(i.quantity) AS units
        FROM orders AS o
        JOIN order_items AS i ON i.order_id = o.order_id
        JOIN products AS p ON p.product_id = i.product_id
        WHERE o.status = 'delivered'
        GROUP BY p.category
        HAVING SUM(i.quantity) >= 3
        ORDER BY units DESC, p.category
    """)

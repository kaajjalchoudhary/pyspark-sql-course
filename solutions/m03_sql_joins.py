"""Module 03 · Joins: inner, left, anti (Spark SQL). Lesson: lessons/03_sql_joins.md"""

from pyspark.sql import DataFrame, SparkSession


def q1_customers_without_orders(spark: SparkSession) -> DataFrame:
    """customer_id and name of customers who never placed an order."""
    return spark.sql("""
        SELECT c.customer_id, c.name
        FROM customers AS c
        LEFT ANTI JOIN orders AS o ON o.customer_id = c.customer_id
        ORDER BY c.customer_id
    """)


def q2_revenue_per_customer(spark: SparkSession) -> DataFrame:
    """Delivered revenue per customer, keeping customers with no delivered orders at 0.

    Columns: name, revenue. The status filter sits in the ON clause: in WHERE it would
    turn the LEFT JOIN back into an inner join and drop the zero-revenue customers.
    """
    return spark.sql("""
        SELECT c.name,
               ROUND(COALESCE(SUM(i.quantity * p.unit_price), 0), 2) AS revenue
        FROM customers AS c
        LEFT JOIN orders AS o
               ON o.customer_id = c.customer_id AND o.status = 'delivered'
        LEFT JOIN order_items AS i ON i.order_id = o.order_id
        LEFT JOIN products AS p ON p.product_id = i.product_id
        GROUP BY c.customer_id, c.name
        ORDER BY revenue DESC, c.name
    """)


def q3_orders_without_payment(spark: SparkSession) -> DataFrame:
    """order_id and status of orders with no row in payments_raw (its order_id is a string)."""
    return spark.sql("""
        SELECT o.order_id, o.status
        FROM orders AS o
        LEFT ANTI JOIN payments_raw AS p
               ON CAST(p.order_id AS INT) = o.order_id
        ORDER BY o.order_id
    """)

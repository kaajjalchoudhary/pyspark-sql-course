"""Module 05 · CTEs and everyday patterns (Spark SQL). Lesson: lessons/05_sql_ctes_and_patterns.md"""

from pyspark.sql import DataFrame, SparkSession


def q1_latest_order_per_customer(spark: SparkSession) -> DataFrame:
    """Each customer's most recent order. Columns: customer_id, order_id, order_date."""
    return spark.sql("""
        WITH ranked AS (
            SELECT customer_id, order_id, order_date,
                   ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC, order_id DESC) AS rn
            FROM orders
        )
        SELECT customer_id, order_id, order_date
        FROM ranked
        WHERE rn = 1
        ORDER BY customer_id
    """)


def q2_month_over_month(spark: SparkSession) -> DataFrame:
    """Delivered revenue per month with growth versus the previous month.

    Columns: month ('yyyy-MM'), revenue, prev_revenue, growth_pct (rounded to 1 decimal).
    """
    return spark.sql("""
        WITH monthly AS (
            SELECT DATE_FORMAT(o.order_date, 'yyyy-MM') AS month,
                   SUM(i.quantity * p.unit_price) AS revenue
            FROM orders AS o
            JOIN order_items AS i ON i.order_id = o.order_id
            JOIN products AS p ON p.product_id = i.product_id
            WHERE o.status = 'delivered'
            GROUP BY DATE_FORMAT(o.order_date, 'yyyy-MM')
        ),
        with_prev AS (
            SELECT month, revenue, LAG(revenue) OVER (ORDER BY month) AS prev_revenue
            FROM monthly
        )
        SELECT month, revenue, prev_revenue,
               ROUND(100 * (revenue - prev_revenue) / prev_revenue, 1) AS growth_pct
        FROM with_prev
        ORDER BY month
    """)


def q3_repeat_buyers(spark: SparkSession) -> DataFrame:
    """Customers with at least 2 delivered orders. Columns: name, delivered_orders."""
    return spark.sql("""
        SELECT c.name, COUNT(*) AS delivered_orders
        FROM customers AS c
        JOIN orders AS o ON o.customer_id = c.customer_id
        WHERE o.status = 'delivered'
        GROUP BY c.customer_id, c.name
        HAVING COUNT(*) >= 2
        ORDER BY delivered_orders DESC, c.name
    """)

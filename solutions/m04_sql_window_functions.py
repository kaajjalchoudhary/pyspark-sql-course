"""Module 04 · Window functions (Spark SQL). Lesson: lessons/04_sql_window_functions.md"""

from pyspark.sql import DataFrame, SparkSession


def q1_product_rank_in_category(spark: SparkSession) -> DataFrame:
    """Rank products by revenue inside their category, ignoring cancelled orders.

    Columns: category, product_name, revenue, rank_in_category (dense_rank, 1 = best).
    """
    return spark.sql("""
        WITH product_revenue AS (
            SELECT p.category, p.product_name, SUM(i.quantity * p.unit_price) AS revenue
            FROM orders AS o
            JOIN order_items AS i ON i.order_id = o.order_id
            JOIN products AS p ON p.product_id = i.product_id
            WHERE o.status <> 'cancelled'
            GROUP BY p.category, p.product_name
        )
        SELECT category, product_name, revenue,
               DENSE_RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS rank_in_category
        FROM product_revenue
        ORDER BY category, rank_in_category
    """)


def q2_running_revenue(spark: SparkSession) -> DataFrame:
    """Daily delivered revenue and its running total. Columns: order_date, daily_revenue, running_revenue."""
    return spark.sql("""
        WITH daily AS (
            SELECT o.order_date, SUM(i.quantity * p.unit_price) AS daily_revenue
            FROM orders AS o
            JOIN order_items AS i ON i.order_id = o.order_id
            JOIN products AS p ON p.product_id = i.product_id
            WHERE o.status = 'delivered'
            GROUP BY o.order_date
        )
        SELECT order_date, daily_revenue,
               SUM(daily_revenue) OVER (
                   ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
               ) AS running_revenue
        FROM daily
        ORDER BY order_date
    """)


def q3_days_since_previous_order(spark: SparkSession) -> DataFrame:
    """For every order, days since the same customer's previous order (NULL for the first).

    Columns: customer_id, order_id, order_date, days_since_prev.
    """
    return spark.sql("""
        SELECT customer_id, order_id, order_date,
               DATEDIFF(order_date,
                        LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date)
               ) AS days_since_prev
        FROM orders
        ORDER BY customer_id, order_date
    """)

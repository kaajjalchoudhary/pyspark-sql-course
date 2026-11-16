"""Checks every module's answers against known results.

    pytest                                   # checks solutions/ (what CI runs)
    COURSE_TARGET=exercises pytest           # checks your answers in exercises/
    COURSE_TARGET=exercises pytest -k m03    # one module at a time
"""

import datetime as dt
import importlib
import os

import pytest

TARGET = os.environ.get("COURSE_TARGET", "solutions")
D = dt.date.fromisoformat

# (module, function) -> (expected columns, expected rows in order)
EXPECTED = {
    ("m01_sql_basics", "q1_german_customers"): (
        ["name", "city"],
        [("Jonas Weber", "Duisburg"), ("Lena Fischer", "Berlin"), ("Tom Becker", "Berlin")],
    ),
    ("m01_sql_basics", "q2_delivered_in_march"): (
        ["order_id", "order_date"],
        [(1005, D("2024-03-05")), (1006, D("2024-03-09"))],
    ),
    ("m01_sql_basics", "q3_mid_priced_products"): (
        ["product_name", "unit_price"],
        [("Desk Chair", 300.0), ("Monitor", 250.0), ("Bookshelf", 180.0), ("Headphones", 150.0)],
    ),
    ("m02_sql_aggregation", "q1_customers_per_country"): (
        ["country", "customers"],
        [("AE", 3), ("DE", 3), ("IN", 2)],
    ),
    ("m02_sql_aggregation", "q2_order_revenue"): (
        ["order_id", "revenue"],
        [(1001, 1225.0), (1002, 150.0), (1003, 500.0), (1004, 300.0), (1005, 1500.0), (1006, 50.0),
         (1007, 180.0), (1008, 162.5), (1009, 600.0), (1010, 287.5), (1011, 1200.0), (1012, 360.0)],
    ),
    ("m02_sql_aggregation", "q3_popular_categories"): (
        ["category", "units"],
        [("Kitchen", 10), ("Electronics", 9), ("Furniture", 4)],
    ),
    ("m03_sql_joins", "q1_customers_without_orders"): (
        ["customer_id", "name"],
        [(7, "Sara Ali"), (8, "Tom Becker")],
    ),
    ("m03_sql_joins", "q2_revenue_per_customer"): (
        ["name", "revenue"],
        [("Aisha Khan", 1887.5), ("Omar Haddad", 1500.0), ("Jonas Weber", 600.0), ("Ravi Mehta", 560.0),
         ("Lena Fischer", 287.5), ("Priya Nair", 0.0), ("Sara Ali", 0.0), ("Tom Becker", 0.0)],
    ),
    ("m03_sql_joins", "q3_orders_without_payment"): (
        ["order_id", "status"],
        [(1004, "cancelled"), (1007, "returned"), (1011, "shipped")],
    ),
    ("m04_sql_window_functions", "q1_product_rank_in_category"): (
        ["category", "product_name", "revenue", "rank_in_category"],
        [("Electronics", "Laptop", 3600.0, 1), ("Electronics", "Monitor", 750.0, 2),
         ("Electronics", "Headphones", 600.0, 3), ("Furniture", "Desk Chair", 600.0, 1),
         ("Furniture", "Bookshelf", 540.0, 2), ("Kitchen", "Coffee Mug", 125.0, 1)],
    ),
    ("m04_sql_window_functions", "q2_running_revenue"): (
        ["order_date", "daily_revenue", "running_revenue"],
        [(D("2024-02-01"), 1225.0, 1225.0), (D("2024-02-03"), 150.0, 1375.0), (D("2024-02-15"), 500.0, 1875.0),
         (D("2024-03-05"), 1500.0, 3375.0), (D("2024-03-09"), 50.0, 3425.0), (D("2024-04-02"), 162.5, 3587.5),
         (D("2024-04-10"), 600.0, 4187.5), (D("2024-04-12"), 287.5, 4475.0), (D("2024-05-02"), 360.0, 4835.0)],
    ),
    ("m04_sql_window_functions", "q3_days_since_previous_order"): (
        ["customer_id", "order_id", "order_date", "days_since_prev"],
        [(1, 1001, D("2024-02-01"), None), (1, 1003, D("2024-02-15"), 14), (1, 1008, D("2024-04-02"), 47),
         (2, 1002, D("2024-02-03"), None), (2, 1006, D("2024-03-09"), 35), (2, 1012, D("2024-05-02"), 54),
         (3, 1004, D("2024-02-20"), None), (3, 1010, D("2024-04-12"), 52),
         (4, 1005, D("2024-03-05"), None), (4, 1011, D("2024-04-25"), 51),
         (5, 1007, D("2024-03-21"), None), (6, 1009, D("2024-04-10"), None)],
    ),
    ("m05_sql_ctes_and_patterns", "q1_latest_order_per_customer"): (
        ["customer_id", "order_id", "order_date"],
        [(1, 1008, D("2024-04-02")), (2, 1012, D("2024-05-02")), (3, 1010, D("2024-04-12")),
         (4, 1011, D("2024-04-25")), (5, 1007, D("2024-03-21")), (6, 1009, D("2024-04-10"))],
    ),
    ("m05_sql_ctes_and_patterns", "q2_month_over_month"): (
        ["month", "revenue", "prev_revenue", "growth_pct"],
        [("2024-02", 1875.0, None, None), ("2024-03", 1550.0, 1875.0, -17.3),
         ("2024-04", 1050.0, 1550.0, -32.3), ("2024-05", 360.0, 1050.0, -65.7)],
    ),
    ("m05_sql_ctes_and_patterns", "q3_repeat_buyers"): (
        ["name", "delivered_orders"],
        [("Aisha Khan", 3), ("Ravi Mehta", 3)],
    ),
    ("m06_dataframe_basics", "q1_order_calendar"): (
        ["order_id", "order_year", "order_month", "is_delivered"],
        [(1001, 2024, 2, True), (1002, 2024, 2, True), (1003, 2024, 2, True), (1004, 2024, 2, False),
         (1005, 2024, 3, True), (1006, 2024, 3, True), (1007, 2024, 3, False), (1008, 2024, 4, True),
         (1009, 2024, 4, True), (1010, 2024, 4, True), (1011, 2024, 4, False), (1012, 2024, 5, True)],
    ),
    ("m06_dataframe_basics", "q2_line_totals"): (
        ["order_id", "product_name", "line_total"],
        [(1001, "Coffee Mug", 25.0), (1001, "Laptop", 1200.0), (1002, "Headphones", 150.0),
         (1003, "Monitor", 500.0), (1004, "Desk Chair", 300.0), (1005, "Headphones", 300.0),
         (1005, "Laptop", 1200.0), (1006, "Coffee Mug", 50.0), (1007, "Bookshelf", 180.0),
         (1008, "Coffee Mug", 12.5), (1008, "Headphones", 150.0), (1009, "Desk Chair", 600.0),
         (1010, "Coffee Mug", 37.5), (1010, "Monitor", 250.0), (1011, "Laptop", 1200.0),
         (1012, "Bookshelf", 360.0)],
    ),
    ("m07_aggregations_and_joins", "q1_avg_order_value_by_country"): (
        ["country", "orders", "avg_order_value"],
        [("AE", 4, 846.88), ("DE", 2, 443.75), ("IN", 3, 186.67)],
    ),
    ("m07_aggregations_and_joins", "q2_monthly_revenue_by_category"): (
        ["month", "Electronics", "Furniture", "Kitchen"],
        [("2024-02", 1850.0, 0.0, 25.0), ("2024-03", 1500.0, 0.0, 50.0),
         ("2024-04", 400.0, 600.0, 50.0), ("2024-05", 0.0, 360.0, 0.0)],
    ),
    ("m07_aggregations_and_joins", "q3_order_count_per_customer"): (
        ["name", "order_count"],
        [("Aisha Khan", 3), ("Ravi Mehta", 3), ("Lena Fischer", 2), ("Omar Haddad", 2),
         ("Priya Nair", 1), ("Jonas Weber", 1), ("Sara Ali", 0), ("Tom Becker", 0)],
    ),
    ("m08_window_functions", "q1_revenue_share"): (
        ["name", "revenue", "pct_of_total"],
        [("Aisha Khan", 1887.5, 39.0), ("Omar Haddad", 1500.0, 31.0), ("Jonas Weber", 600.0, 12.4),
         ("Ravi Mehta", 560.0, 11.6), ("Lena Fischer", 287.5, 5.9)],
    ),
    ("m08_window_functions", "q2_customer_order_history"): (
        ["customer_id", "first_order", "last_order", "order_count"],
        [(1, D("2024-02-01"), D("2024-04-02"), 3), (2, D("2024-02-03"), D("2024-05-02"), 3),
         (3, D("2024-02-20"), D("2024-04-12"), 2), (4, D("2024-03-05"), D("2024-04-25"), 2),
         (5, D("2024-03-21"), D("2024-03-21"), 1), (6, D("2024-04-10"), D("2024-04-10"), 1)],
    ),
    ("m09_data_quality", "q2_quality_issues"): (
        ["payment_id", "issue"],
        [("P10", "unknown_order"), ("P5", "missing_amount"), ("P9", "missing_paid_at")],
    ),
    ("m09_data_quality", "q3_valid_payment_summary"): (
        ["valid_payments", "total_amount"],
        [(7, 4425.0)],
    ),
}


def _same(a, b) -> bool:
    if a is None or b is None:
        return a is None and b is None
    if isinstance(a, bool) or isinstance(b, bool):
        return a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(float(a) - float(b)) < 1e-6
    return a == b


def _load(module: str):
    return importlib.import_module(f"{TARGET}.{module}")


@pytest.mark.parametrize("module,func", sorted(EXPECTED), ids=lambda v: v)
def test_result(spark, module, func):
    columns, rows = EXPECTED[(module, func)]
    try:
        df = getattr(_load(module), func)(spark)
    except NotImplementedError:
        pytest.skip(f"{module}.{func} not attempted yet")
    assert df.columns == columns, f"expected columns {columns}, got {df.columns}"
    got = [tuple(r) for r in df.collect()]
    assert len(got) == len(rows), f"expected {len(rows)} rows, got {len(got)}: {got}"
    for g, want in zip(got, rows):
        assert all(_same(a, b) for a, b in zip(g, want)), f"row mismatch: got {g}, want {want}"


def test_m09_q1_clean_payments(spark):
    try:
        df = _load("m09_data_quality").q1_clean_payments(spark)
    except NotImplementedError:
        pytest.skip("m09_data_quality.q1_clean_payments not attempted yet")
    types = dict(df.dtypes)
    assert df.count() == 10, "exact duplicate rows should be removed"
    assert {r.method for r in df.select("method").distinct().collect()} == {"card", "wallet", "cash"}
    assert types["amount"] == "double"
    assert types["paid_at"] == "timestamp"
    assert types["order_id"] == "int"


def test_m10_q1_broadcast_join(spark):
    try:
        df = _load("m10_performance").q1_broadcast_join(spark)
    except NotImplementedError:
        pytest.skip("m10_performance.q1_broadcast_join not attempted yet")
    plan = df._jdf.queryExecution().executedPlan().toString()
    assert "BroadcastHashJoin" in plan, plan
    assert df.columns == ["order_id", "product_name", "quantity"]
    assert df.count() == 16


def test_m10_q2_repartition_by_customer(spark):
    try:
        df = _load("m10_performance").q2_repartition_by_customer(spark)
    except NotImplementedError:
        pytest.skip("m10_performance.q2_repartition_by_customer not attempted yet")
    assert df.rdd.getNumPartitions() == 4
    assert df.count() == 12

# PySpark & SQL for Data Engineers

[![CI](https://github.com/kaajjalchoudhary/pyspark-sql-course/actions/workflows/ci.yml/badge.svg)](https://github.com/kaajjalchoudhary/pyspark-sql-course/actions/workflows/ci.yml)

A hands-on course that takes you from your first `SELECT` to reading Spark query plans. Every module
has a short lesson, exercises you solve in code, reference solutions, and automated tests that tell you
immediately whether your answer is right.

Created and taught by **Kajal Choudhary**, AI & Data Engineer with 9+ years of data work in banking,
retail and e-commerce, building production pipelines on Databricks, PySpark and dbt.

## Who it is for

- Analysts moving into data engineering
- Engineers who know Python and want to work confidently with Spark
- Anyone preparing for data engineering interviews

You need basic Python. No prior Spark experience is required.

## Curriculum

| # | Module | You will learn | Lesson | Exercise |
|---|---|---|---|---|
| 01 | SQL basics | `SELECT`, `WHERE`, `ORDER BY`, safe date filtering | [lesson](lessons/01_sql_basics.md) | [exercise](exercises/m01_sql_basics.py) |
| 02 | Aggregation | `GROUP BY`, `HAVING`, `COUNT(*)` vs `COUNT(col)`, grain | [lesson](lessons/02_sql_aggregation.md) | [exercise](exercises/m02_sql_aggregation.py) |
| 03 | Joins | inner, left, semi and anti joins; the `ON` vs `WHERE` trap; fan-out | [lesson](lessons/03_sql_joins.md) | [exercise](exercises/m03_sql_joins.py) |
| 04 | Window functions (SQL) | ranking, `LAG`/`LEAD`, running totals, frames | [lesson](lessons/04_sql_window_functions.md) | [exercise](exercises/m04_sql_window_functions.py) |
| 05 | CTEs and patterns | latest record per key, period over period, readable multi-step SQL | [lesson](lessons/05_sql_ctes_and_patterns.md) | [exercise](exercises/m05_sql_ctes_and_patterns.py) |
| 06 | DataFrame API basics | SQL-to-PySpark mapping, lazy evaluation, schemas | [lesson](lessons/06_dataframe_basics.md) | [exercise](exercises/m06_dataframe_basics.py) |
| 07 | Aggregations, joins, pivots | `groupBy().agg()`, join types, pivot, counting after left joins | [lesson](lessons/07_aggregations_and_joins.md) | [exercise](exercises/m07_aggregations_and_joins.py) |
| 08 | Window functions (PySpark) | `Window` specs, frames for `first`/`last`, share of total | [lesson](lessons/08_window_functions.md) | [exercise](exercises/m08_window_functions.py) |
| 09 | Data quality | cleaning messy input, issue reports, quarantining bad rows | [lesson](lessons/09_data_quality.md) | [exercise](exercises/m09_data_quality.py) |
| 10 | Performance | query plans, shuffles, broadcast joins, skew, partitions, caching | [lesson](lessons/10_performance.md) | [exercise](exercises/m10_performance.py) |

**Interview preparation:** [SQL questions](interview/sql_interview_questions.md) ·
[PySpark questions](interview/pyspark_interview_questions.md), each with a worked answer.

## The dataset

A small retail business in `data/`, small enough to check results by hand:

| Table | Rows | Columns |
|---|---|---|
| `customers` | 8 | customer_id, name, city, country, signup_date |
| `products` | 6 | product_id, product_name, category, unit_price |
| `orders` | 12 | order_id, customer_id, order_date, status |
| `order_items` | 16 | order_id, product_id, quantity |
| `payments_raw` | 12 | deliberately messy: duplicates, bad casing, missing values, an orphan key |

## Getting started

Requires Python 3.9+ and Java 17 (Spark runs on the JVM).

```bash
git clone https://github.com/kaajjalchoudhary/pyspark-sql-course.git
cd pyspark-sql-course
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Explore the data interactively:

```python
from course import get_spark, register_tables

spark = get_spark()
register_tables(spark)
spark.sql("SELECT * FROM orders").show()
```

## How to work through a module

1. Read the lesson in `lessons/`.
2. Open the matching file in `exercises/` and replace each `NotImplementedError` with your answer.
3. Check your work:

   ```bash
   COURSE_TARGET=exercises pytest -k m03      # one module
   COURSE_TARGET=exercises pytest             # everything you have attempted
   ```

   Questions you have not attempted yet are skipped, not failed.
4. Compare with `solutions/` after a genuine attempt. There is usually more than one correct answer;
   the tests check the result, not the code.

CI runs every reference solution on each push, so the expected results are always verified.

## Learn with me

I offer 1:1 and small-group sessions in **PySpark and SQL**, working through this course at your pace,
reviewing your code and preparing you for data engineering interviews.
Get in touch on [LinkedIn](https://www.linkedin.com/in/kaajal-choudhary).

## License

MIT

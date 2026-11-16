import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from course import get_spark, register_tables  # noqa: E402


@pytest.fixture(scope="session")
def spark():
    session = get_spark("pyspark-sql-course-tests")
    register_tables(session)
    yield session
    session.stop()

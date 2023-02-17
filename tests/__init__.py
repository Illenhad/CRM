from pathlib import Path

from settings import Settings


class TestSettings:
    PROJECT_PATH: str = Settings.PROJECT_PATH
    TEST_DB_FILE_NAME: str = "test_db.json"
    TEST_DB_DIR: str = 'tests'
    TEST_DB_PATH: Path = Path(PROJECT_PATH / TEST_DB_DIR / TEST_DB_FILE_NAME)
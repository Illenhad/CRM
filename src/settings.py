from pathlib import Path


class Settings:
    PROJECT_PATH: Path = Path(__file__).resolve().parent.parent
    PROJECT_DIR: str = PROJECT_PATH.name

    SRC_DIR: str = 'src'
    SRC_PATH: Path = Path(PROJECT_PATH / SRC_DIR)

    DB_FILE_NAME: str = "db.json"
    DB_DIR: str = 'db'
    DB_PATH: Path = Path(SRC_PATH / DB_DIR / DB_FILE_NAME)

    USER_DB_FILE_NAME: str = "user_db.json"
    USER_DB_DIR: str = 'db'
    USER_DB_PATH: Path = Path(SRC_PATH / USER_DB_DIR / USER_DB_FILE_NAME)

    LOG_FILE_NAME: str = 'user.log'
    LOG_DIR: str = 'logs'
    LOG_PATH: Path = Path(PROJECT_PATH / LOG_DIR / LOG_FILE_NAME)

from pathlib import Path


class Settings:
    PROJECT_PATH: Path = Path(__file__).resolve().parent
    PROJECT_DIR: str = PROJECT_PATH.name

    DB_FILE_NAME: str = "db.json"
    DB_PATH: Path = Path(PROJECT_PATH / DB_FILE_NAME)

    LOG_FILE_NAME: str = 'user.log'
    LOG_PATH: Path = Path(PROJECT_PATH / LOG_FILE_NAME)

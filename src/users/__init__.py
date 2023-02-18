import logging
from pathlib import Path

from src.db.database import UserDatabase
from src.settings import Settings


class Core:
    logging.basicConfig(filename=Settings.LOG_PATH,
                        level=logging.INFO,
                        format='%(asctime)s::%(levelname)s::%(message)s',
                        datefmt='%Y-%m-%d::%H:%M:%S')

    def __init__(self, db_path: Path = Settings.USER_DB_PATH):
        self._database = UserDatabase(db_path)

    @property
    def db(self):
        return self._database.db

    @property
    def logger(self):
        return logging


class NameValueError(ValueError):

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class PhoneValueError(ValueError):

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

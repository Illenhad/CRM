import logging
from pathlib import Path

from src.db.database import UserDatabase
from src.settings import Settings


class Core:
    logging.basicConfig(filename=Settings.LOG_PATH,
                        level=logging.INFO,
                        format='%(asctime)s::%(levelname)s::%(message)s',
                        datefmt='%Y-%m-%d::%H:%M:%S')

    def __init__(self):
        self._database = UserDatabase()

    @property
    def db(self):
        print(id(self._database.db))
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

from abc import ABC
from pathlib import Path

from tinydb import TinyDB

from src import singleton
from src.settings import Settings


class Database(ABC):

    def __init__(self, db_path: Path):
        self._db_path = db_path
        self._db = TinyDB(self._db_path, indent=2)

    @property
    def db(self):
        return self._db


@singleton
class UserDatabase(Database):

    def __init__(self):
        super().__init__(db_path=Settings.USER_DB_PATH)

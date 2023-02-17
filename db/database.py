from pathlib import Path

from tinydb import TinyDB

from db import db_instance
from settings import Settings


@db_instance
class Database:

    def __init__(self, db_path: Path = Settings.DB_PATH):
        self._db_path = db_path
        self._db = TinyDB(self._db_path, indent=2)

    @property
    def db(self):
        return self._db

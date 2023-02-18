from abc import ABC
from pathlib import Path

from src import singleton
from src.db import Database
from src.settings import Settings


@singleton
class UserDatabase(Database):

    def __init__(self, db_path: Path = Settings.USER_DB_PATH):
        super().__init__(db_path=db_path)

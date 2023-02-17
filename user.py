"""Module to generate random users"""
from collections.abc import Mapping
from pathlib import Path

import faker
import re
import string

from tinydb import table, where

from core import Core, PhoneValueError, NameValueError
from settings import Settings


class User(Core):

    def __init__(self, first_name: str, last_name: str, phone_number: str = "", address: str = "", db_path: Path = Settings.DB_PATH) -> None:
        super().__init__(db_path=db_path)

        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address

        self.logger.info(self.__repr__())

    def __repr__(self) -> str:
        return f"User(first_name={self.first_name}, last_name={self.last_name}, phone_number={self.phone_number}, " \
               f"address={self.address.replace('n', '')})"

    def __str__(self) -> str:
        return f"{self.get_full_name}\n{self.phone_number}\n{self.address}"

    @property
    def _mapping(self) -> Mapping:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "address": self.address.replace('n', '')
        }

    @property
    def get_full_name(self):
        """
        The function takes in a person object, and returns a string of the person's first name and last
        name in upper case
        :return: The first name and last name of the user.
        """
        return f"{self.first_name} {self.last_name.upper()}"

    @property
    def db_instance(self) -> table.Document:
        # self.db.get_
        return self.db.get((where('first_name') == self.first_name) and (where('last_name') == self.last_name))

    def _check_user(self):
        self._check_names()
        self._check_phone_number()

    def _check_phone_number(self):
        """
        It checks that the phone number is valid
        """
        phone_digit = re.sub(r"[+()\s]*", "", self.phone_number)
        if len(phone_digit) < 10 or not phone_digit.isdigit():
            msg = f"Invalid phone number : {self.phone_number}"
            self.logger.error(f"{msg} - {self.__repr__()}")
            raise PhoneValueError(message=msg)

    def _check_names(self):
        """
        If the first name or last name is empty, or if the first name or last name contains a digit or
        punctuation character, then raise a ValueError
        """
        if not (self.first_name and self.last_name):
            raise NameValueError(f"Invalid value : {self.first_name} {self.last_name}")

        special_chars = string.digits + string.punctuation
        for c in self.first_name + self.last_name:
            if c in special_chars:
                raise ValueError(f"Name invalid : {self.get_full_name}")

    def save(self, validate_data: bool = False) -> int:
        """
        If the user exists, return -1, otherwise insert the user into the database

        :param validate_data: If True, the user will be checked for validity before being saved,
        defaults to False
        :type validate_data: bool (optional)
        :return: The id of the user.
        """
        if validate_data:
            self._check_user()

        return -1 if self.exists() else self.db.insert(self._mapping)

    def exists(self) -> bool:
        """
        It checks if the database instance exists.
        :return: A boolean value.
        """
        return bool(self.db_instance)

    def delete(self) -> list[int]:
        """
        It deletes the user from the database if the user exists
        :return: The user id.
        """
        if self.exists():
            return self.db.remove(doc_ids=[self.db_instance.doc_id])
        return []


def get_all_users() -> list[User]:
    """
    "Return a list of User objects, where each User object is created from the data in the database."
    :return: A list of User objects
    """
    return [User(**user) for user in Core().db.all()]


def generate_fake_users(number: int = 1, save_user: bool = False) -> list[User]:
    """
    It generates fake users
    
    :param number: The number of users to generate, defaults to 1
    :type number: int (optional)
    :param save_user: if True, the user will be saved in the database, defaults to False
    :type save_user: bool (optional)
    :return: A list of User objects
    """
    fake = faker.Faker(locale="fr_FR")
    users = []
    for _ in range(number):
        user = User(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            phone_number=fake.phone_number(),
            address=fake.address().replace("\n", " "))
        if save_user:
            user.save(validate_data=True)

        users.append(user)

    return users


def main():
    for user in generate_fake_users(number=10, save_user=True):
        print("-" * 10)
        print(user)


if __name__ == "__main__":
    main()

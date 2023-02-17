import json
import string

from tinydb import table
from unittest import TestCase

from core import Core
from tests import TestSettings
from user import User


class TestException(Exception):

    def __init__(self, message: str = "Test failed."):
        self.message = message
        super().__init__(self.message)


class TestUser(TestCase):

    def _init_user(self):
        # Delete all data
        core = Core(db_path=TestSettings.TEST_DB_PATH)
        core.db.drop_tables()
        core.db.close()

        self.user = User(
            first_name="Pierre",
            last_name="Legrand",
            phone_number="0123456789",
            address="Fake address",
            db_path=TestSettings.TEST_DB_PATH
        )

    def test_init_a_user(self):
        self._init_user()

        self.assertEqual(self.user.first_name, "Pierre")
        self.assertEqual(self.user.last_name, "Legrand")
        self.assertEqual(self.user.phone_number, "0123456789")
        self.assertEqual(self.user.address, "Fake address")

    def test_get_full_name(self):
        self._init_user()

        self.assertEqual(self.user.get_full_name, "Pierre LEGRAND")

    def test_db_instance(self):
        self._init_user()

        self.assertEqual(self.user.db_instance, None)
        self.user.save()
        self.assertIsInstance(self.user.db_instance, table.Document)

    def test__check_user(self):
        self._init_user()

        raised = False
        try:
            self.user._check_names()
        except TestException:
            raised = True
        self.assertFalse(raised, TestException("Valid user's test failed."))

    def test__check_a_valid_phone_number(self):
        self._init_user()

        raised = False
        try:
            self.user._check_phone_number()
        except TestException:
            raised = True
        self.assertFalse(raised, TestException("Valid phone test failed."))

    def test__check_a_string_phone_number(self):
        self._init_user()

        with self.assertRaises(ValueError):
            self.user.phone_number = "Pierre"
            self.user._check_phone_number()

    def test__check_a_phone_number_with_special_characters(self):
        self._init_user()

        with self.assertRaises(ValueError):
            self.user.phone_number = string.punctuation
            self.user._check_phone_number()

    def test__check_a_phone_number_less_than_ten_digits(self):
        self._init_user()

        with self.assertRaises(ValueError):
            self.user.phone_number = "012"
            self.user._check_phone_number()

    def test__check_names_with_empty_first_name(self):
        self._init_user()

        self.user.first_name = ""
        with self.assertRaises(ValueError):
            self.user._check_names()

    def test__check_names_with_empty_last_name(self):
        self._init_user()

        self.user.last_name = ""
        with self.assertRaises(ValueError):
            self.user._check_names()

    def test__check_names_with_digit(self):
        self._init_user()

        self.user.first_name = "Pi3rr3"
        with self.assertRaises(ValueError):
            self.user._check_names()

    def test__check_names_with_special_charts(self):
        self._init_user()

        self.user.last_name = "Legr@nd!"
        with self.assertRaises(ValueError):
            self.user._check_names()

    def test__check_names_with_valid_names(self):
        self._init_user()

        raised = False
        try:
            self.user._check_names()
        except TestException:
            raised = True
        self.assertFalse(raised, TestException("Valid name's test failed."))

    def test_save(self):
        self._init_user()

        with open(TestSettings.TEST_DB_PATH, "r") as f:
            self.assertEqual(f.readlines(), ['{}'])

        self.user.save()

        with open(TestSettings.TEST_DB_PATH, "r") as f:
            file = json.load(f)
            self.assertIsInstance(file, dict)
            self.assertIsInstance(file.get("_default"), dict)
            self.assertDictEqual({
                "first_name": "Pierre",
                "last_name": "Legrand",
                "phone_number": "0123456789",
                "address": "Fake address"
            }, file.get("_default").get("1"))

        self.user.db.close()

    def test_exists(self):
        self._init_user()
        self.user.save()

        with open(TestSettings.TEST_DB_PATH, "r") as f:
            file = json.load(f)
            self.assertIsInstance(file, dict)
            self.assertIsInstance(file.get("_default"), dict)
            self.assertDictEqual({
                "first_name": "Pierre",
                "last_name": "Legrand",
                "phone_number": "0123456789",
                "address": "Fake address"
            }, file.get("_default").get("1"))

    def test_delete(self):
        self._init_user()
        self.user.save()

        self.assertEqual(self.user.delete(), [1])

        with open(TestSettings.TEST_DB_PATH, "r") as f:
            file = json.load(f)
            self.assertIsInstance(file, dict)
            self.assertIsInstance(file.get("_default"), dict)
            self.assertNotEqual({
                "first_name": "Pierre",
                "last_name": "Legrand",
                "phone_number": "0123456789",
                "address": "Fake address"
            }, file.get("_default").get(1))

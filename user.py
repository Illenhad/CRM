"""Module to generate random users"""
import faker
import logging

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
formatter = logging.basicConfig(
    filename=BASE_DIR / 'user.log', 
    level=logging.INFO, 
    format='%(asctime)s::%(levelname)s::%(message)s', 
    datefmt='%Y-%m-%d::%H:%M:%S')

fake = faker.Faker()

def get_user() -> str:
    """
    Generate a single user
    :return: A string of a first name and a last name.
    """
    logging.info("Generating user.")
    return f"{fake.first_name()} {fake.last_name()}"

def get_users(numbers:int=1) -> list:
    """
    Generate a list of users
    
    :param numbers: The number of users to generate, defaults to 1
    :type numbers: int (optional)
    :return: A list of users.
    """
    logging.info(f"Generating a list of {numbers} users.")
    return [get_user() for _ in range(numbers)]

if __name__ == "__main__":
    user = get_users(numbers=5)
    print(user)
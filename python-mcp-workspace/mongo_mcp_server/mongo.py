from pymongo import MongoClient

from .config import DEFAULT_DATABASE_NAME, MONGO_URI
from .validators import validate_database_name


client = MongoClient(MONGO_URI)


def list_database_names() -> list[str]:
    return client.list_database_names()


def get_database(database: str = DEFAULT_DATABASE_NAME):
    validate_database_name(database)
    return client[database]

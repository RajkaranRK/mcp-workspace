from ..config import DEFAULT_DATABASE_NAME
from ..mongo import get_database
from ..serializers import to_jsonable
from ..validators import (
    validate_collection_name,
    validate_index_keys,
    validate_index_name,
    validate_index_options,
)


def get_indexes(
    collection: str,
    database: str = DEFAULT_DATABASE_NAME,
) -> list:
    validate_collection_name(collection)

    indexes = list(get_database(database)[collection].list_indexes())

    return to_jsonable(indexes)


def create_index(
    collection: str,
    keys: dict,
    database: str = DEFAULT_DATABASE_NAME,
    options: dict | None = None,
) -> dict:
    options = options or {}

    validate_collection_name(collection)
    validate_index_keys(keys)
    validate_index_options(options)

    index_name = get_database(database)[collection].create_index(
        list(keys.items()),
        **options,
    )

    return {
        "indexName": index_name,
        "database": database,
        "collection": collection,
        "keys": keys,
        "options": options,
    }


def update_index(
    collection: str,
    indexName: str,
    keys: dict,
    database: str = DEFAULT_DATABASE_NAME,
    options: dict | None = None,
) -> dict:
    options = options or {}

    validate_collection_name(collection)
    validate_index_name(indexName)
    validate_index_keys(keys)
    validate_index_options(options)

    collection_instance = get_database(database)[collection]
    collection_instance.drop_index(indexName)
    new_index_name = collection_instance.create_index(list(keys.items()), **options)

    return {
        "droppedIndexName": indexName,
        "newIndexName": new_index_name,
        "database": database,
        "collection": collection,
        "keys": keys,
        "options": options,
    }


def delete_index(
    collection: str,
    indexName: str,
    database: str = DEFAULT_DATABASE_NAME,
) -> dict:
    validate_collection_name(collection)
    validate_index_name(indexName)

    get_database(database)[collection].drop_index(indexName)

    return {
        "deletedIndexName": indexName,
        "database": database,
        "collection": collection,
        "result": True,
    }

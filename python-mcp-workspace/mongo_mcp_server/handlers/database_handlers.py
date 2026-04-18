from ..config import DEFAULT_DATABASE_NAME
from ..mongo import get_database, list_database_names
from ..serializers import to_jsonable
from ..validators import (
    validate_collection_name,
    validate_confirmed,
    validate_create_collection_options,
    validate_database_name,
)


def list_databases(include_collections: bool = True) -> dict:
    databases = list_database_names()

    if not include_collections:
        return {
            "databases": databases,
        }

    return {
        "databases": [
            {
                "database": database,
                "collections": get_database(database).list_collection_names(),
            }
            for database in databases
        ],
    }


def list_collections(database: str = DEFAULT_DATABASE_NAME) -> dict:
    collections = get_database(database).list_collection_names()

    return {
        "database": database,
        "collections": collections,
    }


def create_database(database: str, collection: str = "_mcp_init") -> dict:
    validate_database_name(database)
    validate_collection_name(collection)

    database_instance = get_database(database)
    existing_collections = database_instance.list_collection_names(
        filter={"name": collection}
    )

    if not existing_collections:
        database_instance.create_collection(collection)

    return {
        "database": database,
        "collection": collection,
        "created": not bool(existing_collections),
    }


def create_collection(
    collection: str,
    database: str = DEFAULT_DATABASE_NAME,
    options: dict | None = None,
) -> dict:
    options = options or {}

    validate_collection_name(collection)
    validate_create_collection_options(options)

    get_database(database).create_collection(collection, **options)

    return {
        "database": database,
        "collection": collection,
        "created": True,
    }


def drop_database(database: str, confirm: bool) -> dict:
    validate_database_name(database)
    validate_confirmed(confirm)

    get_database(database).client.drop_database(database)

    return {
        "database": database,
        "dropped": True,
    }


def drop_collection(
    collection: str,
    confirm: bool,
    database: str = DEFAULT_DATABASE_NAME,
) -> dict:
    validate_collection_name(collection)
    validate_confirmed(confirm)

    result = get_database(database).drop_collection(collection)

    return to_jsonable(
        {
            "database": database,
            "collection": collection,
            "dropped": True,
            "result": result,
        }
    )

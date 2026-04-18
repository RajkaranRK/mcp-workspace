from typing import Any

from ..config import DEFAULT_DATABASE_NAME
from ..mongo import get_database
from ..serializers import to_jsonable
from ..validators import (
    validate_aggregation_pipeline,
    validate_collection_name,
    validate_confirmed,
    validate_documents,
    validate_non_empty_plain_object,
    validate_optional_boolean,
    validate_optional_number,
    validate_plain_object,
)


def find_documents(
    collection: str,
    database: str = DEFAULT_DATABASE_NAME,
    query: dict | None = None,
    projection: dict | None = None,
    sort: dict | None = None,
    limit: int = 10,
    skip: int = 0,
) -> list:
    query = query or {}

    validate_collection_name(collection)
    validate_plain_object(query, "query")
    validate_optional_number(limit, "limit")
    validate_optional_number(skip, "skip")

    if projection is not None:
        validate_plain_object(projection, "projection")

    if sort is not None:
        validate_plain_object(sort, "sort")

    cursor = get_database(database)[collection].find(query, projection)

    if sort is not None:
        cursor = cursor.sort(list(sort.items()))

    documents = list(
        cursor
        .skip(max(0, int(skip)))
        .limit(max(0, int(limit)))
    )

    return to_jsonable(documents)


def insert_document(
    collection: str,
    document: dict,
    database: str = DEFAULT_DATABASE_NAME,
) -> dict:
    validate_collection_name(collection)
    validate_plain_object(document, "document")

    result = get_database(database)[collection].insert_one(document)

    return to_jsonable(
        {
            "database": database,
            "collection": collection,
            "insertedId": result.inserted_id,
        }
    )


def bulk_insert(
    collection: str,
    documents: list[dict],
    database: str = DEFAULT_DATABASE_NAME,
    ordered: bool = True,
) -> dict:
    validate_collection_name(collection)
    validate_documents(documents)
    validate_optional_boolean(ordered, "ordered")

    result = get_database(database)[collection].insert_many(
        documents,
        ordered=ordered,
    )

    return to_jsonable(
        {
            "database": database,
            "collection": collection,
            "insertedCount": len(result.inserted_ids),
            "insertedIds": result.inserted_ids,
        }
    )


def update_documents(
    collection: str,
    filter: dict,
    database: str = DEFAULT_DATABASE_NAME,
    update: dict | None = None,
    set: dict | None = None,
    updateMany: bool = False,
    upsert: bool = False,
    confirm: bool | None = None,
) -> dict:
    validate_collection_name(collection)
    validate_plain_object(filter, "filter")
    validate_optional_boolean(updateMany, "updateMany")
    validate_optional_boolean(upsert, "upsert")

    if update is not None:
        validate_non_empty_plain_object(update, "update")
        update_document = update
    elif set is not None:
        validate_non_empty_plain_object(set, "set")
        update_document = {"$set": set}
    else:
        raise ValueError("Either update or set is required")

    if updateMany and len(filter) == 0:
        validate_confirmed(confirm)

    collection_instance = get_database(database)[collection]
    result = (
        collection_instance.update_many(filter, update_document, upsert=upsert)
        if updateMany
        else collection_instance.update_one(filter, update_document, upsert=upsert)
    )

    return to_jsonable(
        {
            "database": database,
            "collection": collection,
            "matchedCount": result.matched_count,
            "modifiedCount": result.modified_count,
            "upsertedId": result.upserted_id,
        }
    )


def delete_documents(
    collection: str,
    filter: dict,
    confirm: bool,
    database: str = DEFAULT_DATABASE_NAME,
    deleteMany: bool = False,
) -> dict:
    validate_collection_name(collection)
    validate_plain_object(filter, "filter")
    validate_optional_boolean(deleteMany, "deleteMany")
    validate_confirmed(confirm)

    collection_instance = get_database(database)[collection]
    result = (
        collection_instance.delete_many(filter)
        if deleteMany
        else collection_instance.delete_one(filter)
    )

    return {
        "database": database,
        "collection": collection,
        "deletedCount": result.deleted_count,
    }


def aggregate_documents(
    collection: str,
    pipeline: list[dict],
    database: str = DEFAULT_DATABASE_NAME,
    limit: int | None = None,
) -> dict:
    validate_collection_name(collection)
    validate_aggregation_pipeline(pipeline)
    validate_optional_number(limit, "limit")

    pipeline_to_run: list[dict[str, Any]] = [*pipeline]

    if limit is not None and limit > 0:
        pipeline_to_run.append({"$limit": limit})

    documents = list(get_database(database)[collection].aggregate(pipeline_to_run))

    return to_jsonable(
        {
            "database": database,
            "collection": collection,
            "pipeline": pipeline_to_run,
            "documents": documents,
        }
    )

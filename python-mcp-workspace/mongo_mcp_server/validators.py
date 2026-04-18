from typing import Any


def validate_database_name(database: str) -> None:
    if not isinstance(database, str) or not database.strip():
        raise ValueError("database must be a non-empty string")


def validate_collection_name(collection: str) -> None:
    if not isinstance(collection, str) or not collection.strip():
        raise ValueError("collection must be a non-empty string")


def validate_plain_object(value: Any, field_name: str) -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{field_name} must be an object")


def validate_non_empty_plain_object(value: Any, field_name: str) -> None:
    validate_plain_object(value, field_name)

    if len(value) == 0:
        raise ValueError(f"{field_name} must not be empty")


def validate_optional_boolean(value: Any, field_name: str) -> None:
    if value is not None and not isinstance(value, bool):
        raise ValueError(f"{field_name} must be a boolean")


def validate_optional_number(value: Any, field_name: str) -> None:
    if value is not None and not isinstance(value, (int, float)):
        raise ValueError(f"{field_name} must be a number")


def validate_documents(documents: Any) -> None:
    if not isinstance(documents, list) or len(documents) == 0:
        raise ValueError("documents must be a non-empty array")

    for index, document in enumerate(documents):
        validate_plain_object(document, f"documents[{index}]")


def validate_aggregation_pipeline(pipeline: Any) -> None:
    if not isinstance(pipeline, list):
        raise ValueError("pipeline must be an array")

    for index, stage in enumerate(pipeline):
        validate_non_empty_plain_object(stage, f"pipeline[{index}]")


def validate_create_collection_options(options: Any) -> None:
    if options is not None:
        validate_plain_object(options, "options")


def validate_confirmed(confirm: bool) -> None:
    if confirm is not True:
        raise ValueError("confirm must be true for this destructive operation")


def validate_index_keys(keys: Any) -> None:
    if not isinstance(keys, dict) or len(keys) == 0:
        raise ValueError("keys must be a non-empty object")


def validate_index_options(options: Any) -> None:
    if options is not None:
        validate_plain_object(options, "options")


def validate_index_name(index_name: str) -> None:
    if not isinstance(index_name, str) or not index_name.strip():
        raise ValueError("indexName must be a non-empty string")

    if index_name == "_id_":
        raise ValueError("The default _id_ index cannot be modified or deleted")

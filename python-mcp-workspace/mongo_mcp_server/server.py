from typing import Any

from mcp.server.fastmcp import FastMCP

from .handlers import database_handlers, document_handlers, index_handlers, user_handlers

mcp = FastMCP("mongo-mcp")


@mcp.tool()
def list_collections(database: str = "users") -> dict:
    """List all MongoDB collections."""
    return database_handlers.list_collections(database)


@mcp.tool()
def create_database(database: str, collection: str = "_mcp_init") -> dict:
    """Create a MongoDB database by creating an initial collection inside it."""
    return database_handlers.create_database(database, collection)


@mcp.tool()
def create_collection(
    collection: str,
    database: str = "users",
    options: dict[str, Any] | None = None,
) -> dict:
    """Create a collection in a MongoDB database."""
    return database_handlers.create_collection(collection, database, options)


@mcp.tool()
def drop_database(database: str, confirm: bool) -> dict:
    """Drop a MongoDB database. Requires confirm: true."""
    return database_handlers.drop_database(database, confirm)


@mcp.tool()
def drop_collection(
    collection: str,
    confirm: bool,
    database: str = "users",
) -> dict:
    """Drop a collection from a MongoDB database. Requires confirm: true."""
    return database_handlers.drop_collection(collection, confirm, database)


@mcp.tool()
def find_documents(
    collection: str,
    database: str = "users",
    query: dict[str, Any] | None = None,
    projection: dict[str, Any] | None = None,
    sort: dict[str, Any] | None = None,
    limit: int = 10,
    skip: int = 0,
) -> list:
    """Find documents in a collection."""
    return document_handlers.find_documents(
        collection,
        database,
        query,
        projection,
        sort,
        limit,
        skip,
    )


@mcp.tool()
def insert_document(
    collection: str,
    document: dict[str, Any],
    database: str = "users",
) -> dict:
    """Insert one document into any collection in any database."""
    return document_handlers.insert_document(collection, document, database)


@mcp.tool()
def bulk_insert(
    collection: str,
    documents: list[dict[str, Any]],
    database: str = "users",
    ordered: bool = True,
) -> dict:
    """Insert multiple documents into a collection."""
    return document_handlers.bulk_insert(collection, documents, database, ordered)


@mcp.tool()
def update_documents(
    collection: str,
    filter: dict[str, Any],
    database: str = "users",
    update: dict[str, Any] | None = None,
    set: dict[str, Any] | None = None,
    updateMany: bool = False,
    upsert: bool = False,
    confirm: bool | None = None,
) -> dict:
    """Update one or many documents in any collection in any database."""
    return document_handlers.update_documents(
        collection,
        filter,
        database,
        update,
        set,
        updateMany,
        upsert,
        confirm,
    )


@mcp.tool()
def delete_documents(
    collection: str,
    filter: dict[str, Any],
    confirm: bool,
    database: str = "users",
    deleteMany: bool = False,
) -> dict:
    """Delete one or many documents from any collection in any database."""
    return document_handlers.delete_documents(
        collection,
        filter,
        confirm,
        database,
        deleteMany,
    )


@mcp.tool()
def aggregate_documents(
    collection: str,
    pipeline: list[dict[str, Any]],
    database: str = "users",
    limit: int | None = None,
) -> dict:
    """Run an aggregation pipeline on any collection in any database."""
    return document_handlers.aggregate_documents(collection, pipeline, database, limit)


@mcp.tool()
def get_indexes(collection: str, database: str = "users") -> list:
    """Get indexes of a collection."""
    return index_handlers.get_indexes(collection, database)


@mcp.tool()
def create_index(
    collection: str,
    keys: dict[str, Any],
    database: str = "users",
    options: dict[str, Any] | None = None,
) -> dict:
    """Create an index on a collection."""
    return index_handlers.create_index(collection, keys, database, options)


@mcp.tool()
def update_index(
    collection: str,
    indexName: str,
    keys: dict[str, Any],
    database: str = "users",
    options: dict[str, Any] | None = None,
) -> dict:
    """Replace an existing index by dropping it and creating a new one."""
    return index_handlers.update_index(collection, indexName, keys, database, options)


@mcp.tool()
def delete_index(
    collection: str,
    indexName: str,
    database: str = "users",
) -> dict:
    """Delete an index from a collection by index name."""
    return index_handlers.delete_index(collection, indexName, database)


@mcp.tool()
def add_user(firstName: str, lastName: str, email: str) -> dict:
    """Add user data to the user collection."""
    return user_handlers.add_user(firstName, lastName, email)


@mcp.tool()
def update_user(
    id: str,
    firstName: str | None = None,
    lastName: str | None = None,
    email: str | None = None,
) -> dict:
    """Update user details in the user collection by id."""
    return user_handlers.update_user(id, firstName, lastName, email)


@mcp.tool()
def delete_user(id: str) -> dict:
    """Delete a user from the user collection by id."""
    return user_handlers.delete_user(id)


if __name__ == "__main__":
    mcp.run(transport="stdio")

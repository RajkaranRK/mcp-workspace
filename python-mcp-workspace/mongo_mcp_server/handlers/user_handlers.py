from bson import ObjectId

from ..config import DEFAULT_DATABASE_NAME
from ..mongo import get_database
from ..serializers import to_jsonable


def user_collection():
    return get_database(DEFAULT_DATABASE_NAME)["user"]


def add_user(firstName: str, lastName: str, email: str) -> dict:
    if not all(isinstance(value, str) for value in [firstName, lastName, email]):
        raise ValueError("firstName, lastName, and email must be strings")

    result = user_collection().insert_one(
        {
            "firstName": firstName,
            "lastName": lastName,
            "email": email,
        }
    )

    return to_jsonable(
        {
            "insertedId": result.inserted_id,
            "firstName": firstName,
            "lastName": lastName,
            "email": email,
        }
    )


def update_user(
    id: str,
    firstName: str | None = None,
    lastName: str | None = None,
    email: str | None = None,
) -> dict:
    if not isinstance(id, str) or not ObjectId.is_valid(id):
        raise ValueError("id must be a valid MongoDB ObjectId string")

    update = {}

    if firstName is not None:
        if not isinstance(firstName, str):
            raise ValueError("firstName must be a string")
        update["firstName"] = firstName

    if lastName is not None:
        if not isinstance(lastName, str):
            raise ValueError("lastName must be a string")
        update["lastName"] = lastName

    if email is not None:
        if not isinstance(email, str):
            raise ValueError("email must be a string")
        update["email"] = email

    if len(update) == 0:
        raise ValueError("At least one of firstName, lastName, or email is required")

    result = user_collection().update_one(
        {"_id": ObjectId(id)},
        {"$set": update},
    )

    return {
        "matchedCount": result.matched_count,
        "modifiedCount": result.modified_count,
        "updatedFields": update,
    }


def delete_user(id: str) -> dict:
    if not isinstance(id, str) or not ObjectId.is_valid(id):
        raise ValueError("id must be a valid MongoDB ObjectId string")

    result = user_collection().delete_one({"_id": ObjectId(id)})

    return {
        "deletedCount": result.deleted_count,
    }

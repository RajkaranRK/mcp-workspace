import { ObjectId } from "mongodb";
import { defaultDatabaseName } from "../config.js";
import { getDatabase } from "../mongo.js";
import { textContent } from "../response.js";

const userCollection = () => getDatabase(defaultDatabaseName).collection("user");

export const userHandlers = {
  add_user: async ({ firstName, lastName, email }) => {
    if (
      typeof firstName !== "string" ||
      typeof lastName !== "string" ||
      typeof email !== "string"
    ) {
      throw new Error("firstName, lastName, and email must be strings");
    }

    const result = await userCollection().insertOne({
      firstName,
      lastName,
      email
    });

    return textContent({
      insertedId: result.insertedId,
      firstName,
      lastName,
      email
    });
  },

  update_user: async ({ id, firstName, lastName, email }) => {
    if (typeof id !== "string" || !ObjectId.isValid(id)) {
      throw new Error("id must be a valid MongoDB ObjectId string");
    }

    const update = {};

    if (firstName !== undefined) {
      if (typeof firstName !== "string") {
        throw new Error("firstName must be a string");
      }
      update.firstName = firstName;
    }

    if (lastName !== undefined) {
      if (typeof lastName !== "string") {
        throw new Error("lastName must be a string");
      }
      update.lastName = lastName;
    }

    if (email !== undefined) {
      if (typeof email !== "string") {
        throw new Error("email must be a string");
      }
      update.email = email;
    }

    if (Object.keys(update).length === 0) {
      throw new Error("At least one of firstName, lastName, or email is required");
    }

    const result = await userCollection().updateOne(
      { _id: new ObjectId(id) },
      { $set: update }
    );

    return textContent({
      matchedCount: result.matchedCount,
      modifiedCount: result.modifiedCount,
      updatedFields: update
    });
  },

  delete_user: async ({ id }) => {
    if (typeof id !== "string" || !ObjectId.isValid(id)) {
      throw new Error("id must be a valid MongoDB ObjectId string");
    }

    const result = await userCollection().deleteOne({
      _id: new ObjectId(id)
    });

    return textContent({
      deletedCount: result.deletedCount
    });
  }
};

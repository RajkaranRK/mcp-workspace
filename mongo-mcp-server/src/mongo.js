import { MongoClient } from "mongodb";
import { defaultDatabaseName, mongoUri } from "./config.js";

export const client = new MongoClient(mongoUri);

export const connectMongo = async () => {
  await client.connect();
};

export const getDatabase = (database = defaultDatabaseName) => {
  validateDatabaseName(database);
  return client.db(database);
};

export const validateDatabaseName = (database) => {
  if (typeof database !== "string" || database.trim() === "") {
    throw new Error("database must be a non-empty string");
  }
};

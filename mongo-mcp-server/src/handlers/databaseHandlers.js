import { defaultDatabaseName } from "../config.js";
import { getDatabase, validateDatabaseName } from "../mongo.js";
import { textContent } from "../response.js";
import {
  validateCollectionName,
  validateConfirmed,
  validateCreateCollectionOptions
} from "../validators.js";

export const databaseHandlers = {
  list_collections: async ({ database = defaultDatabaseName }) => {
    const cols = await getDatabase(database).listCollections().toArray();

    return textContent({
      database,
      collections: cols.map((collection) => collection.name)
    });
  },

  create_database: async ({ database, collection = "_mcp_init" }) => {
    validateDatabaseName(database);
    validateCollectionName(collection);

    const databaseInstance = getDatabase(database);
    const existingCollections = await databaseInstance
      .listCollections({ name: collection })
      .toArray();

    if (existingCollections.length === 0) {
      await databaseInstance.createCollection(collection);
    }

    return textContent({
      database,
      collection,
      created: existingCollections.length === 0
    });
  },

  create_collection: async ({
    database = defaultDatabaseName,
    collection,
    options = {}
  }) => {
    validateCollectionName(collection);
    validateCreateCollectionOptions(options);

    await getDatabase(database).createCollection(collection, options);

    return textContent({
      database,
      collection,
      created: true
    });
  },

  drop_database: async ({ database, confirm }) => {
    validateDatabaseName(database);
    validateConfirmed(confirm);

    const result = await getDatabase(database).dropDatabase();

    return textContent({
      database,
      dropped: result
    });
  },

  drop_collection: async ({
    database = defaultDatabaseName,
    collection,
    confirm
  }) => {
    validateCollectionName(collection);
    validateConfirmed(confirm);

    const result = await getDatabase(database).dropCollection(collection);

    return textContent({
      database,
      collection,
      dropped: result
    });
  }
};

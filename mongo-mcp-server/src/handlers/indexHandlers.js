import { defaultDatabaseName } from "../config.js";
import { getDatabase } from "../mongo.js";
import { textContent } from "../response.js";
import {
  validateCollectionName,
  validateIndexKeys,
  validateIndexName,
  validateIndexOptions
} from "../validators.js";

export const indexHandlers = {
  get_indexes: async ({ database = defaultDatabaseName, collection }) => {
    validateCollectionName(collection);

    const indexes = await getDatabase(database)
      .collection(collection)
      .indexes();

    return textContent(indexes);
  },

  create_index: async ({
    database = defaultDatabaseName,
    collection,
    keys,
    options = {}
  }) => {
    validateCollectionName(collection);
    validateIndexKeys(keys);
    validateIndexOptions(options);

    const indexName = await getDatabase(database)
      .collection(collection)
      .createIndex(keys, options);

    return textContent({
      indexName,
      database,
      collection,
      keys,
      options
    });
  },

  update_index: async ({
    database = defaultDatabaseName,
    collection,
    indexName,
    keys,
    options = {}
  }) => {
    validateCollectionName(collection);
    validateIndexName(indexName);
    validateIndexKeys(keys);
    validateIndexOptions(options);

    const mongoCollection = getDatabase(database).collection(collection);

    await mongoCollection.dropIndex(indexName);
    const newIndexName = await mongoCollection.createIndex(keys, options);

    return textContent({
      droppedIndexName: indexName,
      newIndexName,
      database,
      collection,
      keys,
      options
    });
  },

  delete_index: async ({
    database = defaultDatabaseName,
    collection,
    indexName
  }) => {
    validateCollectionName(collection);
    validateIndexName(indexName);

    const result = await getDatabase(database)
      .collection(collection)
      .dropIndex(indexName);

    return textContent({
      deletedIndexName: indexName,
      database,
      collection,
      result
    });
  }
};

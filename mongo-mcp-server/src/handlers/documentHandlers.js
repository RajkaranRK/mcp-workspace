import { defaultDatabaseName } from "../config.js";
import { getDatabase } from "../mongo.js";
import { textContent } from "../response.js";
import {
  validateAggregationPipeline,
  validateCollectionName,
  validateConfirmed,
  validateDocuments,
  validateNonEmptyPlainObject,
  validateOptionalBoolean,
  validateOptionalNumber,
  validatePlainObject
} from "../validators.js";

export const documentHandlers = {
  find_documents: async ({
    database = defaultDatabaseName,
    collection,
    query = {},
    projection,
    sort,
    limit = 10,
    skip = 0
  }) => {
    validateCollectionName(collection);
    validatePlainObject(query, "query");
    validateOptionalNumber(limit, "limit");
    validateOptionalNumber(skip, "skip");

    if (projection !== undefined) {
      validatePlainObject(projection, "projection");
    }

    if (sort !== undefined) {
      validatePlainObject(sort, "sort");
    }

    let cursor = getDatabase(database)
      .collection(collection)
      .find(query);

    if (projection !== undefined) {
      cursor = cursor.project(projection);
    }

    if (sort !== undefined) {
      cursor = cursor.sort(sort);
    }

    const docs = await cursor
      .skip(Math.max(0, skip))
      .limit(Math.max(0, limit))
      .toArray();

    return textContent(docs);
  },

  insert_document: async ({
    database = defaultDatabaseName,
    collection,
    document
  }) => {
    validateCollectionName(collection);
    validatePlainObject(document, "document");

    const result = await getDatabase(database)
      .collection(collection)
      .insertOne(document);

    return textContent({
      database,
      collection,
      insertedId: result.insertedId
    });
  },

  bulk_insert: async ({
    database = defaultDatabaseName,
    collection,
    documents,
    ordered = true
  }) => {
    validateCollectionName(collection);
    validateDocuments(documents);
    validateOptionalBoolean(ordered, "ordered");

    const result = await getDatabase(database)
      .collection(collection)
      .insertMany(documents, { ordered });

    return textContent({
      database,
      collection,
      insertedCount: result.insertedCount,
      insertedIds: result.insertedIds
    });
  },

  update_documents: async ({
    database = defaultDatabaseName,
    collection,
    filter,
    update,
    set,
    updateMany = false,
    upsert = false,
    confirm
  }) => {
    validateCollectionName(collection);
    validatePlainObject(filter, "filter");
    validateOptionalBoolean(updateMany, "updateMany");
    validateOptionalBoolean(upsert, "upsert");

    let updateDocument;

    if (update !== undefined) {
      validateNonEmptyPlainObject(update, "update");
      updateDocument = update;
    } else if (set !== undefined) {
      validateNonEmptyPlainObject(set, "set");
      updateDocument = { $set: set };
    } else {
      throw new Error("Either update or set is required");
    }

    if (updateMany === true && Object.keys(filter).length === 0) {
      validateConfirmed(confirm);
    }

    const mongoCollection = getDatabase(database).collection(collection);
    const result = updateMany
      ? await mongoCollection.updateMany(filter, updateDocument, { upsert })
      : await mongoCollection.updateOne(filter, updateDocument, { upsert });

    return textContent({
      database,
      collection,
      matchedCount: result.matchedCount,
      modifiedCount: result.modifiedCount,
      upsertedCount: result.upsertedCount,
      upsertedId: result.upsertedId
    });
  },

  delete_documents: async ({
    database = defaultDatabaseName,
    collection,
    filter,
    deleteMany = false,
    confirm
  }) => {
    validateCollectionName(collection);
    validatePlainObject(filter, "filter");
    validateOptionalBoolean(deleteMany, "deleteMany");
    validateConfirmed(confirm);

    const mongoCollection = getDatabase(database).collection(collection);
    const result = deleteMany
      ? await mongoCollection.deleteMany(filter)
      : await mongoCollection.deleteOne(filter);

    return textContent({
      database,
      collection,
      deletedCount: result.deletedCount
    });
  },

  aggregate_documents: async ({
    database = defaultDatabaseName,
    collection,
    pipeline,
    limit
  }) => {
    validateCollectionName(collection);
    validateAggregationPipeline(pipeline);
    validateOptionalNumber(limit, "limit");

    const pipelineToRun = [...pipeline];

    if (limit !== undefined && limit > 0) {
      pipelineToRun.push({ $limit: limit });
    }

    const docs = await getDatabase(database)
      .collection(collection)
      .aggregate(pipelineToRun)
      .toArray();

    return textContent({
      database,
      collection,
      pipeline: pipelineToRun,
      documents: docs
    });
  }
};

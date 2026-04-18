const databaseProperty = {
  type: "string",
  description: "Optional database name. Defaults to users."
};

export const tools = [
  {
    name: "list_collections",
    description: "List all MongoDB collections",
    inputSchema: {
      type: "object",
      properties: {
        database: databaseProperty
      }
    }
  },
  {
    name: "create_database",
    description: "Create a MongoDB database by creating an initial collection inside it",
    inputSchema: {
      type: "object",
      properties: {
        database: { type: "string" },
        collection: {
          type: "string",
          description: "Optional initial collection name. Defaults to _mcp_init."
        }
      },
      required: ["database"]
    }
  },
  {
    name: "create_collection",
    description: "Create a collection in a MongoDB database",
    inputSchema: {
      type: "object",
      properties: {
        database: databaseProperty,
        collection: { type: "string" },
        options: {
          type: "object",
          description: "Optional MongoDB createCollection options"
        }
      },
      required: ["collection"]
    }
  },
  {
    name: "drop_database",
    description: "Drop a MongoDB database. Requires confirm: true.",
    inputSchema: {
      type: "object",
      properties: {
        database: { type: "string" },
        confirm: {
          type: "boolean",
          description: "Must be true to confirm dropping the database."
        }
      },
      required: ["database", "confirm"]
    }
  },
  {
    name: "drop_collection",
    description: "Drop a collection from a MongoDB database. Requires confirm: true.",
    inputSchema: {
      type: "object",
      properties: {
        database: databaseProperty,
        collection: { type: "string" },
        confirm: {
          type: "boolean",
          description: "Must be true to confirm dropping the collection."
        }
      },
      required: ["collection", "confirm"]
    }
  },
  {
    name: "find_documents",
    description: "Find documents in a collection",
    inputSchema: {
      type: "object",
      properties: {
        database: databaseProperty,
        collection: { type: "string" },
        query: { type: "object" },
        projection: {
          type: "object",
          description: "Optional MongoDB projection object"
        },
        sort: {
          type: "object",
          description: "Optional MongoDB sort object"
        },
        limit: {
          type: "number",
          description: "Optional maximum number of documents. Defaults to 10."
        },
        skip: {
          type: "number",
          description: "Optional number of documents to skip. Defaults to 0."
        }
      },
      required: ["collection"]
    }
  },
  {
    name: "insert_document",
    description: "Insert one document into any collection in any database",
    inputSchema: {
      type: "object",
      properties: {
        database: databaseProperty,
        collection: { type: "string" },
        document: { type: "object" }
      },
      required: ["collection", "document"]
    }
  },
  {
    name: "bulk_insert",
    description: "Insert multiple documents into a collection",
    inputSchema: {
      type: "object",
      properties: {
        database: databaseProperty,
        collection: { type: "string" },
        documents: {
          type: "array",
          items: {
            type: "object"
          }
        },
        ordered: {
          type: "boolean",
          description: "Optional insert order behavior. Defaults to true."
        }
      },
      required: ["collection", "documents"]
    }
  },
  {
    name: "update_documents",
    description: "Update one or many documents in any collection in any database",
    inputSchema: {
      type: "object",
      properties: {
        database: databaseProperty,
        collection: { type: "string" },
        filter: {
          type: "object",
          description: "MongoDB filter for selecting documents"
        },
        update: {
          type: "object",
          description: "MongoDB update document, for example { \"$set\": { \"status\": \"active\" } }"
        },
        set: {
          type: "object",
          description: "Convenience fields to set. Used only when update is not provided."
        },
        updateMany: {
          type: "boolean",
          description: "When true, update all matching documents. Defaults to false."
        },
        upsert: {
          type: "boolean",
          description: "When true, insert a document if no document matches. Defaults to false."
        },
        confirm: {
          type: "boolean",
          description: "Required as true when updateMany is true and filter is empty."
        }
      },
      required: ["collection", "filter"]
    }
  },
  {
    name: "delete_documents",
    description: "Delete one or many documents from any collection in any database. Requires confirm: true.",
    inputSchema: {
      type: "object",
      properties: {
        database: databaseProperty,
        collection: { type: "string" },
        filter: {
          type: "object",
          description: "MongoDB filter for selecting documents to delete"
        },
        deleteMany: {
          type: "boolean",
          description: "When true, delete all matching documents. Defaults to false."
        },
        confirm: {
          type: "boolean",
          description: "Must be true to confirm deleting documents."
        }
      },
      required: ["collection", "filter", "confirm"]
    }
  },
  {
    name: "aggregate_documents",
    description: "Run an aggregation pipeline on any collection in any database",
    inputSchema: {
      type: "object",
      properties: {
        database: databaseProperty,
        collection: { type: "string" },
        pipeline: {
          type: "array",
          items: {
            type: "object"
          }
        },
        limit: {
          type: "number",
          description: "Optional safety limit appended to the pipeline when greater than 0."
        }
      },
      required: ["collection", "pipeline"]
    }
  },
  {
    name: "get_indexes",
    description: "Get indexes of a collection",
    inputSchema: {
      type: "object",
      properties: {
        database: databaseProperty,
        collection: { type: "string" }
      },
      required: ["collection"]
    }
  },
  {
    name: "create_index",
    description: "Create an index on a collection",
    inputSchema: {
      type: "object",
      properties: {
        database: databaseProperty,
        collection: { type: "string" },
        keys: {
          type: "object",
          description: "Index keys, for example { \"email\": 1 } or { \"firstName\": 1, \"lastName\": 1 }"
        },
        options: {
          type: "object",
          description: "Optional index options, for example { \"unique\": true, \"name\": \"email_unique_idx\" }"
        }
      },
      required: ["collection", "keys"]
    }
  },
  {
    name: "update_index",
    description: "Replace an existing index by dropping it and creating a new one",
    inputSchema: {
      type: "object",
      properties: {
        database: databaseProperty,
        collection: { type: "string" },
        indexName: { type: "string" },
        keys: {
          type: "object",
          description: "New index keys, for example { \"email\": 1 }"
        },
        options: {
          type: "object",
          description: "Optional new index options, for example { \"unique\": true, \"name\": \"email_unique_idx\" }"
        }
      },
      required: ["collection", "indexName", "keys"]
    }
  },
  {
    name: "delete_index",
    description: "Delete an index from a collection by index name",
    inputSchema: {
      type: "object",
      properties: {
        database: databaseProperty,
        collection: { type: "string" },
        indexName: { type: "string" }
      },
      required: ["collection", "indexName"]
    }
  },
  {
    name: "add_user",
    description: "Add user data to the user collection",
    inputSchema: {
      type: "object",
      properties: {
        firstName: { type: "string" },
        lastName: { type: "string" },
        email: { type: "string" }
      },
      required: ["firstName", "lastName", "email"]
    }
  },
  {
    name: "update_user",
    description: "Update user details in the user collection by id",
    inputSchema: {
      type: "object",
      properties: {
        id: { type: "string" },
        firstName: { type: "string" },
        lastName: { type: "string" },
        email: { type: "string" }
      },
      required: ["id"]
    }
  },
  {
    name: "delete_user",
    description: "Delete a user from the user collection by id",
    inputSchema: {
      type: "object",
      properties: {
        id: { type: "string" }
      },
      required: ["id"]
    }
  }
];

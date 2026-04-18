export const validateCollectionName = (collection) => {
  if (typeof collection !== "string" || collection.trim() === "") {
    throw new Error("collection must be a non-empty string");
  }
};

export const validatePlainObject = (value, fieldName) => {
  if (value === null || Array.isArray(value) || typeof value !== "object") {
    throw new Error(`${fieldName} must be an object`);
  }
};

export const validateNonEmptyPlainObject = (value, fieldName) => {
  validatePlainObject(value, fieldName);

  if (Object.keys(value).length === 0) {
    throw new Error(`${fieldName} must not be empty`);
  }
};

export const validateOptionalBoolean = (value, fieldName) => {
  if (value !== undefined && typeof value !== "boolean") {
    throw new Error(`${fieldName} must be a boolean`);
  }
};

export const validateOptionalNumber = (value, fieldName) => {
  if (value !== undefined && typeof value !== "number") {
    throw new Error(`${fieldName} must be a number`);
  }
};

export const validateDocuments = (documents) => {
  if (!Array.isArray(documents) || documents.length === 0) {
    throw new Error("documents must be a non-empty array");
  }

  documents.forEach((document, index) => {
    validatePlainObject(document, `documents[${index}]`);
  });
};

export const validateAggregationPipeline = (pipeline) => {
  if (!Array.isArray(pipeline)) {
    throw new Error("pipeline must be an array");
  }

  pipeline.forEach((stage, index) => {
    validateNonEmptyPlainObject(stage, `pipeline[${index}]`);
  });
};

export const validateCreateCollectionOptions = (options) => {
  if (options !== undefined) {
    validatePlainObject(options, "options");
  }
};

export const validateConfirmed = (confirm) => {
  if (confirm !== true) {
    throw new Error("confirm must be true for this destructive operation");
  }
};

export const validateIndexKeys = (keys) => {
  if (
    keys === null ||
    Array.isArray(keys) ||
    typeof keys !== "object" ||
    Object.keys(keys).length === 0
  ) {
    throw new Error("keys must be a non-empty object");
  }
};

export const validateIndexOptions = (options) => {
  if (
    options !== undefined &&
    (options === null || Array.isArray(options) || typeof options !== "object")
  ) {
    throw new Error("options must be an object when provided");
  }
};

export const validateIndexName = (indexName) => {
  if (typeof indexName !== "string" || indexName.trim() === "") {
    throw new Error("indexName must be a non-empty string");
  }

  if (indexName === "_id_") {
    throw new Error("The default _id_ index cannot be modified or deleted");
  }
};

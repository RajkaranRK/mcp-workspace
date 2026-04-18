import { constants } from "node:fs";
import fs from "node:fs/promises";
import path from "node:path";
import { repositoriesRoot } from "./config.js";

export const validateRelativePath = (relativePath) => {
  if (typeof relativePath !== "string" || relativePath.trim() === "") {
    throw new Error("relativePath must be a non-empty string");
  }
};

export const validateContent = (content) => {
  if (typeof content !== "string") {
    throw new Error("content must be a string");
  }
};

export const resolveInsideRoot = (relativePath = ".") => {
  if (typeof relativePath !== "string") {
    throw new Error("relativePath must be a string");
  }

  const resolvedPath = path.resolve(repositoriesRoot, relativePath);
  const relativeToRoot = path.relative(repositoriesRoot, resolvedPath);

  if (
    relativeToRoot === ".." ||
    relativeToRoot.startsWith(`..${path.sep}`) ||
    path.isAbsolute(relativeToRoot)
  ) {
    throw new Error("Path is outside the configured repositories root");
  }

  return resolvedPath;
};

export const pathExists = async (filePath) => {
  try {
    await fs.access(filePath, constants.F_OK);
    return true;
  } catch {
    return false;
  }
};

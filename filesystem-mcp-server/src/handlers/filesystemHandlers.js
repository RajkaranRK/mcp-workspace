import fs from "node:fs/promises";
import path from "node:path";
import { repositoriesRoot } from "../config.js";
import {
  pathExists,
  resolveInsideRoot,
  validateContent,
  validateRelativePath
} from "../pathUtils.js";
import { jsonContent } from "../response.js";

export const filesystemHandlers = {
  get_workspace_root: async () => {
    return jsonContent({
      repositoriesRoot
    });
  },

  list_repositories: async () => {
    const entries = await fs.readdir(repositoriesRoot, { withFileTypes: true });
    const repositories = entries
      .filter((entry) => entry.isDirectory())
      .map((entry) => entry.name)
      .sort();

    return jsonContent({
      repositoriesRoot,
      repositories
    });
  },

  list_directory: async ({ relativePath }) => {
    validateRelativePath(relativePath);

    const directoryPath = resolveInsideRoot(relativePath);
    const entries = await fs.readdir(directoryPath, { withFileTypes: true });
    const items = entries
      .map((entry) => ({
        name: entry.name,
        type: entry.isDirectory() ? "directory" : "file",
        relativePath: path.relative(
          repositoriesRoot,
          path.join(directoryPath, entry.name)
        )
      }))
      .sort((a, b) => a.relativePath.localeCompare(b.relativePath));

    return jsonContent({
      relativePath,
      items
    });
  },

  read_file: async ({ relativePath }) => {
    validateRelativePath(relativePath);

    const filePath = resolveInsideRoot(relativePath);
    const content = await fs.readFile(filePath, "utf8");

    return jsonContent({
      relativePath,
      content
    });
  },

  write_file: async ({ relativePath, content }) => {
    validateRelativePath(relativePath);
    validateContent(content);

    const filePath = resolveInsideRoot(relativePath);
    await fs.mkdir(path.dirname(filePath), { recursive: true });
    await fs.writeFile(filePath, content, "utf8");

    return jsonContent({
      relativePath,
      bytesWritten: Buffer.byteLength(content, "utf8")
    });
  },

  append_file: async ({ relativePath, content }) => {
    validateRelativePath(relativePath);
    validateContent(content);

    const filePath = resolveInsideRoot(relativePath);
    await fs.mkdir(path.dirname(filePath), { recursive: true });
    await fs.appendFile(filePath, content, "utf8");

    return jsonContent({
      relativePath,
      bytesAppended: Buffer.byteLength(content, "utf8")
    });
  },

  create_directory: async ({ relativePath }) => {
    validateRelativePath(relativePath);

    const directoryPath = resolveInsideRoot(relativePath);
    const existedBefore = await pathExists(directoryPath);
    await fs.mkdir(directoryPath, { recursive: true });

    return jsonContent({
      relativePath,
      created: !existedBefore
    });
  }
};

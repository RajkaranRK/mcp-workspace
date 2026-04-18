export const tools = [
  {
    name: "get_workspace_root",
    description: "Get the configured local repositories workspace root",
    inputSchema: {
      type: "object",
      properties: {}
    }
  },
  {
    name: "list_repositories",
    description: "List directories directly inside the repositories workspace root",
    inputSchema: {
      type: "object",
      properties: {}
    }
  },
  {
    name: "list_directory",
    description: "List files and folders inside a directory under the repositories workspace root",
    inputSchema: {
      type: "object",
      properties: {
        relativePath: {
          type: "string",
          description: "Path relative to the repositories root. Use . for the root."
        }
      },
      required: ["relativePath"]
    }
  },
  {
    name: "read_file",
    description: "Read a UTF-8 text file under the repositories workspace root",
    inputSchema: {
      type: "object",
      properties: {
        relativePath: {
          type: "string",
          description: "File path relative to the repositories root"
        }
      },
      required: ["relativePath"]
    }
  },
  {
    name: "write_file",
    description: "Create or replace a UTF-8 text file under the repositories workspace root",
    inputSchema: {
      type: "object",
      properties: {
        relativePath: {
          type: "string",
          description: "File path relative to the repositories root"
        },
        content: {
          type: "string",
          description: "Full file content to write"
        }
      },
      required: ["relativePath", "content"]
    }
  },
  {
    name: "append_file",
    description: "Append UTF-8 text to a file under the repositories workspace root",
    inputSchema: {
      type: "object",
      properties: {
        relativePath: {
          type: "string",
          description: "File path relative to the repositories root"
        },
        content: {
          type: "string",
          description: "Text content to append"
        }
      },
      required: ["relativePath", "content"]
    }
  },
  {
    name: "create_directory",
    description: "Create a directory under the repositories workspace root",
    inputSchema: {
      type: "object",
      properties: {
        relativePath: {
          type: "string",
          description: "Directory path relative to the repositories root"
        }
      },
      required: ["relativePath"]
    }
  }
];

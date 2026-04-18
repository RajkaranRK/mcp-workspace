import { filesystemHandlers } from "./filesystemHandlers.js";

export const callTool = async ({ name, args = {} }) => {
  const handler = filesystemHandlers[name];

  if (!handler) {
    throw new Error("Unknown tool");
  }

  return handler(args);
};

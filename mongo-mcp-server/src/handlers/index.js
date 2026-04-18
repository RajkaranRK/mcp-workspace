import { databaseHandlers } from "./databaseHandlers.js";
import { documentHandlers } from "./documentHandlers.js";
import { indexHandlers } from "./indexHandlers.js";
import { userHandlers } from "./userHandlers.js";

const handlers = {
  ...databaseHandlers,
  ...documentHandlers,
  ...indexHandlers,
  ...userHandlers
};

export const callTool = async ({ name, args = {} }) => {
  const handler = handlers[name];

  if (!handler) {
    throw new Error("Unknown tool");
  }

  return handler(args);
};

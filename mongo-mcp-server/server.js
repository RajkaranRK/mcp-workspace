import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema
} from "@modelcontextprotocol/sdk/types.js";
import { connectMongo } from "./src/mongo.js";
import { callTool } from "./src/handlers/index.js";
import { tools } from "./src/toolDefinitions.js";

const server = new Server(
  {
    name: "mongo-mcp",
    version: "1.0.0"
  },
  {
    capabilities: {
      tools: {}
    }
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools }));

server.setRequestHandler(CallToolRequestSchema, async (req) => {
  return callTool({
    name: req.params.name,
    args: req.params.arguments
  });
});

await connectMongo();

const transport = new StdioServerTransport();
await server.connect(transport);
console.error("Mongo MCP server started and connected over stdio");

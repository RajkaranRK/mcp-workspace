# Python MCP Workspace

Python versions of the MCP servers from the Node.js workspace.

## Servers

- `mongo_mcp_server`: MongoDB tools for databases, collections, documents, indexes, aggregation, and legacy user helpers.
- `filesystem_mcp_server`: local filesystem tools restricted to `REPOSITORIES_ROOT`.

## Setup

```bash
cd /Users/rajkaran/Desktop/mcp/mcp-workspace/python-mcp-workspace
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run Manually

Mongo MCP:

```bash
python mongo_server.py
```

Filesystem MCP:

```bash
python filesystem_server.py
```

These are stdio MCP servers, so they are normally started by Claude Desktop.

## Claude Desktop Config

Add these entries inside `mcpServers`:

```json
{
  "mcpServers": {
    "mongo-mcp-python": {
      "command": "/Users/rajkaran/Desktop/mcp/mcp-workspace/python-mcp-workspace/.venv/bin/python",
      "args": [
        "/Users/rajkaran/Desktop/mcp/mcp-workspace/python-mcp-workspace/mongo_server.py"
      ],
      "env": {
        "MONGO_URI": "mongodb://localhost:27017",
        "MONGO_DEFAULT_DATABASE": "users"
      }
    },
    "filesystem-mcp-python": {
      "command": "/Users/rajkaran/Desktop/mcp/mcp-workspace/python-mcp-workspace/.venv/bin/python",
      "args": [
        "/Users/rajkaran/Desktop/mcp/mcp-workspace/python-mcp-workspace/filesystem_server.py"
      ],
      "env": {
        "REPOSITORIES_ROOT": "/Users/rajkaran/Desktop/mcp/mcp-workspace"
      }
    }
  }
}
```

Restart Claude Desktop after changing the config.

# Python MCP Workspace

Python versions of the MCP servers from the Node.js workspace.

## Servers

- `mongo_mcp_server`: MongoDB tools for databases, collections, documents, indexes, aggregation, and legacy user helpers.
- `filesystem_mcp_server`: local filesystem tools restricted to `REPOSITORIES_ROOT`.
- `bitbucket_mcp_server`: Bitbucket Cloud pull request tools plus local Git branch and merge-conflict helpers.

## Setup

```bash
cd /Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace
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

Bitbucket MCP:

```bash
python bitbucket_server.py
```

These are stdio MCP servers, so they are normally started by Claude Desktop.

## Bitbucket Environment

The Bitbucket server supports either an access token or a username plus app
password.

```bash
export BITBUCKET_URL="https://bitbucket.axisb.com"
export BITBUCKET_USERNAME="FC607387"
export BITBUCKET_APP_PASSWORD="your-bitbucket-app-password"
export REPOSITORIES_ROOT="/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace"
```

Alternatively:

```bash
export BITBUCKET_ACCESS_TOKEN="your-access-token"
```

Available tool areas:

- Pull requests: list, get, create, approve, request changes, merge, diffstat.
- Comments: list comments, add global or inline comments, resolve comment threads.
- Local Git: checkout branches, merge branches locally, list conflicted files, mark conflicts resolved, continue or abort merges.

## Claude Desktop Config

Add these entries inside `mcpServers`:

```json
{
  "mcpServers": {
    "mongo-mcp-python": {
      "command": "/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/.venv/bin/python",
      "args": [
        "/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/mongo_server.py"
      ],
      "env": {
        "MONGO_URI": "mongodb://localhost:27017",
        "MONGO_DEFAULT_DATABASE": "users"
      }
    },
    "filesystem-mcp-python": {
      "command": "/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/.venv/bin/python",
      "args": [
        "/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/filesystem_server.py"
      ],
      "env": {
        "REPOSITORIES_ROOT": "/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace"
      }
    },
    "bitbucket-mcp-python": {
      "command": "/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/.venv/bin/python",
      "args": [
        "/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/bitbucket_server.py"
      ],
      "env": {
        "BITBUCKET_URL": "https://bitbucket.axisb.com",
        "BITBUCKET_USERNAME": "FC607387",
        "BITBUCKET_APP_PASSWORD": "your-bitbucket-app-password",
        "REPOSITORIES_ROOT": "/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace"
      }
    }
  }
}
```

Restart Claude Desktop after changing the config.

## GitHub Copilot in VS Code

Use this example as `.vscode/mcp.json` in the workspace where you want Copilot
to use these tools:

```bash
python-mcp-workspace/config-examples/vscode-mcp.json
```

In VS Code, open the command palette and run:

```text
MCP: List Servers
```

Then start `mongo-mcp-python`, `filesystem-mcp-python`, and `bitbucket-mcp-python`.

## GitHub Copilot in IntelliJ IDEA

Open GitHub Copilot Chat in IntelliJ IDEA, switch to Agent mode, open the tools
or MCP configuration, and add the contents of:

```bash
python-mcp-workspace/config-examples/jetbrains-copilot-mcp.json
```

The JetBrains Copilot MCP config also uses a `servers` object, so the same local
stdio server definitions work there.

For global setup in VS Code, IntelliJ IDEA, and Claude Desktop, see:

```bash
python-mcp-workspace/GLOBAL_COPILOT_SETUP.md
```

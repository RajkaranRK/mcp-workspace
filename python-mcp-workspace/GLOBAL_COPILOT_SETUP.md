# Global MCP Setup

This guide configures the Python MCP servers globally for:

- VS Code with GitHub Copilot
- IntelliJ IDEA with GitHub Copilot
- Claude Desktop
- Codex CLI

The MCP servers live here:

```text
/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace
```

## 1. Install Python Dependencies

Run this once:

```bash
cd /Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Verify the servers import correctly:

```bash
.venv/bin/python -c 'import mongo_mcp_server.server, filesystem_mcp_server.server, bitbucket_mcp_server.server; print("ok")'
```

## 2. MCP Servers

Mongo MCP server:

```text
/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/mongo_server.py
```

Filesystem MCP server:

```text
/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/filesystem_server.py
```

Bitbucket MCP server:

```text
/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/bitbucket_server.py
```

Python executable:

```text
/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/.venv/bin/python
```

## 3. Global VS Code Setup

Use the VS Code user-level MCP config, not a workspace `.vscode/mcp.json`.

On macOS, create or edit:

```text
~/Library/Application Support/Code/User/mcp.json
```

You can open it from terminal:

```bash
mkdir -p ~/Library/Application\ Support/Code/User
open -e ~/Library/Application\ Support/Code/User/mcp.json
```

Add this config:

```json
{
  "servers": {
    "mongo-mcp-python": {
      "type": "stdio",
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
      "type": "stdio",
      "command": "/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/.venv/bin/python",
      "args": [
        "/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/filesystem_server.py"
      ],
      "env": {
        "REPOSITORIES_ROOT": "/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace"
      }
    },
    "bitbucket-mcp-python": {
      "type": "stdio",
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

Then restart VS Code.

To verify:

1. Open Command Palette.
2. Run `MCP: List Servers`.
3. Start `mongo-mcp-python`, `filesystem-mcp-python`, and `bitbucket-mcp-python` if needed.
4. Open Copilot Chat in Agent mode.

Try:

```text
Use filesystem-mcp-python to list my workspace root.
```

Or:

```text
Use mongo-mcp-python to list collections in the users database.
```

## 4. Global IntelliJ IDEA Setup

In IntelliJ IDEA:

1. Open GitHub Copilot Chat.
2. Switch to `Agent` mode.
3. Click the tools/settings icon in the Copilot Chat panel.
4. Open the MCP configuration.
5. Add this config:

```json
{
  "servers": {
    "mongo-mcp-python": {
      "type": "stdio",
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
      "type": "stdio",
      "command": "/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/.venv/bin/python",
      "args": [
        "/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/filesystem_server.py"
      ],
      "env": {
        "REPOSITORIES_ROOT": "/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace"
      }
    },
    "bitbucket-mcp-python": {
      "type": "stdio",
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

Save the config.

Then:

1. Restart IntelliJ IDEA if the tools do not appear automatically.
2. Open Copilot Chat.
3. Switch to `Agent` mode.
4. Open the tools list and verify all three servers are available.

Try:

```text
Use filesystem-mcp-python to list my workspace root.
```

Or:

```text
Use mongo-mcp-python to list collections in the users database.
```

Validation note:

- IntelliJ IDEA with GitHub Copilot uses a top-level `servers` object.
- Claude Desktop uses a top-level `mcpServers` object.
- For IntelliJ IDEA, do not use `mcpServers`.

Correct IntelliJ/Copilot shape:

```json
{
  "servers": {}
}
```

Incorrect for IntelliJ/Copilot:

```json
{
  "mcpServers": {}
}
```

## 5. Choosing Filesystem Access Scope

The filesystem server is restricted by `REPOSITORIES_ROOT`.

Current global example:

```json
"REPOSITORIES_ROOT": "/Users/rajkaran"
```

This gives access to your home directory.

Safer alternatives:

```json
"REPOSITORIES_ROOT": "/Users/rajkaran/Desktop"
```

or:

```json
"REPOSITORIES_ROOT": "/Users/rajkaran/Desktop/mcp"
```

Use the narrowest root that still covers the repositories you want your MCP client to access.

## 6. MongoDB Requirement

The Mongo server expects MongoDB at:

```text
mongodb://localhost:27017
```

Check MongoDB before using Mongo tools:

```bash
mongosh
```

Or if installed through Homebrew:

```bash
brew services list | grep mongodb
```

## 7. Bitbucket Requirement

The Bitbucket server uses Bitbucket Cloud REST API credentials. Configure either:

```json
"BITBUCKET_ACCESS_TOKEN": "your-access-token"
```

or:

```json
"BITBUCKET_URL": "https://bitbucket.axisb.com",
"BITBUCKET_USERNAME": "FC607387",
"BITBUCKET_APP_PASSWORD": "your-bitbucket-app-password"
```

Set these defaults if you do not want to pass workspace and repository on every
tool call:

```json
"BITBUCKET_DEFAULT_WORKSPACE": "your-workspace",
"BITBUCKET_DEFAULT_REPO_SLUG": "your-repo-slug"
```

## 8. Troubleshooting

If tools do not appear:

- Restart the IDE.
- Check that `.venv/bin/python` exists.
- Check that dependencies are installed.
- Check JSON syntax.
- For Mongo tools, confirm MongoDB is running.
- For Bitbucket tools, confirm credentials and default workspace/repository env vars.

Validate the JSON config:

```bash
python3 -m json.tool ~/Library/Application\ Support/Code/User/mcp.json
```

Validate Python imports:

```bash
cd /Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace
.venv/bin/python -c 'import mongo_mcp_server.server, filesystem_mcp_server.server, bitbucket_mcp_server.server; print("ok")'
```

## 9. Claude Desktop Setup

Claude Desktop uses a global app-level config file.

On macOS, create or edit:

```text
~/Library/Application Support/Claude/claude_desktop_config.json
```

Open it from terminal:

```bash
mkdir -p ~/Library/Application\ Support/Claude
open -e ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

If the file is empty, use this full config:

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
        "REPOSITORIES_ROOT": "/Users/rajkaran"
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

If your file already has preferences, keep them and add `mcpServers` at the same
top level:

```json
{
  "preferences": {
    "sidebarMode": "chat"
  },
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
        "REPOSITORIES_ROOT": "/Users/rajkaran"
      }
    },
    "bitbucket-mcp-python": {
      "command": "/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/.venv/bin/python",
      "args": [
        "/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/bitbucket_server.py"
      ],
      "env": {
        "BITBUCKET_USERNAME": "your-bitbucket-username",
        "BITBUCKET_APP_PASSWORD": "your-bitbucket-app-password",
        "BITBUCKET_DEFAULT_WORKSPACE": "your-workspace",
        "BITBUCKET_DEFAULT_REPO_SLUG": "your-repo-slug",
        "REPOSITORIES_ROOT": "/Users/rajkaran"
      }
    }
  }
}
```

Validate the Claude config:

```bash
python3 -m json.tool ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

Restart Claude Desktop:

```bash
osascript -e 'quit app "Claude"'
open -a Claude
```

Then ask Claude:

```text
Use filesystem-mcp-python to list my workspace root.
```

Or:

```text
Use mongo-mcp-python to list collections in the users database.
```

Claude Desktop notes:

- Claude uses `mcpServers`, while VS Code and IntelliJ Copilot use `servers`.
- Claude stdio servers should not print normal logs to stdout.
- The Python MCP SDK handles protocol output correctly.
- MongoDB must be running before Mongo tools can work.

## 10. Codex CLI Setup

Codex stores global MCP server config in:

```text
~/.codex/config.toml
```

The easiest way to configure the servers is with `codex mcp add`.

Add Mongo MCP:

```bash
codex mcp add mongo-mcp-python \
  --env MONGO_URI=mongodb://localhost:27017 \
  --env MONGO_DEFAULT_DATABASE=users \
  -- /Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/.venv/bin/python \
  /Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/mongo_server.py
```

Add filesystem MCP:

```bash
codex mcp add filesystem-mcp-python \
  --env REPOSITORIES_ROOT=/Users/rajkaran \
  -- /Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/.venv/bin/python \
  /Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/filesystem_server.py
```

Add Bitbucket MCP:

```bash
codex mcp add bitbucket-mcp-python \
  --env BITBUCKET_URL=https://bitbucket.axisb.com \
  --env BITBUCKET_USERNAME=FC607387 \
  --env BITBUCKET_APP_PASSWORD=your-bitbucket-app-password \
  --env REPOSITORIES_ROOT=/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace \
  -- /Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/.venv/bin/python \
  /Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/bitbucket_server.py
```

Verify the configured servers:

```bash
codex mcp list
codex mcp get mongo-mcp-python
codex mcp get filesystem-mcp-python
codex mcp get bitbucket-mcp-python
```

The generated TOML should look like this:

```toml
[mcp_servers.mongo-mcp-python]
command = "/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/.venv/bin/python"
args = ["/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/mongo_server.py"]

[mcp_servers.mongo-mcp-python.env]
MONGO_DEFAULT_DATABASE = "users"
MONGO_URI = "mongodb://localhost:27017"

[mcp_servers.filesystem-mcp-python]
command = "/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/.venv/bin/python"
args = ["/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/filesystem_server.py"]

[mcp_servers.filesystem-mcp-python.env]
REPOSITORIES_ROOT = "/Users/rajkaran"

[mcp_servers.bitbucket-mcp-python]
command = "/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/.venv/bin/python"
args = ["/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace/python-mcp-workspace/bitbucket_server.py"]

[mcp_servers.bitbucket-mcp-python.env]
BITBUCKET_APP_PASSWORD = "your-bitbucket-app-password"
BITBUCKET_URL = "https://bitbucket.axisb.com"
BITBUCKET_USERNAME = "FC607387"
REPOSITORIES_ROOT = "/Users/rajkaran.01/Desktop/mcp-server-workspace/mcp-workspace"
```

Restart Codex after changing MCP config so the tools are loaded into the next session.

Try:

```text
Use filesystem-mcp-python to list my workspace root.
```

Or:

```text
Use mongo-mcp-python to list collections in the users database.
```

Codex notes:

- Codex uses TOML under `mcp_servers`, not JSON.
- Codex does not use the Copilot `servers` object.
- Codex does not use the Claude Desktop `mcpServers` object.
- MongoDB must be running before Mongo tools can work.
- Bitbucket credentials must be configured before remote PR tools can work.

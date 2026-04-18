import os
from pathlib import Path


BITBUCKET_BASE_URL = os.getenv(
    "BITBUCKET_BASE_URL",
    "https://api.bitbucket.org/2.0",
).rstrip("/")
BITBUCKET_USERNAME = os.getenv("BITBUCKET_USERNAME", "")
BITBUCKET_APP_PASSWORD = os.getenv("BITBUCKET_APP_PASSWORD", "")
BITBUCKET_ACCESS_TOKEN = os.getenv("BITBUCKET_ACCESS_TOKEN", "")
BITBUCKET_DEFAULT_WORKSPACE = os.getenv("BITBUCKET_DEFAULT_WORKSPACE", "")
BITBUCKET_DEFAULT_REPO_SLUG = os.getenv("BITBUCKET_DEFAULT_REPO_SLUG", "")

REPOSITORIES_ROOT = Path(
    os.getenv("REPOSITORIES_ROOT", "/Users/rajkaran/Desktop/mcp/mcp-workspace")
).expanduser().resolve()

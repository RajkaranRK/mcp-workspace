import os
from pathlib import Path


def _env_first(*names: str, default: str = "") -> str:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return default


BITBUCKET_BASE_URL = _env_first(
    "BITBUCKET_URL",
    "BITBUCKET_BASE_URL",
    default="https://api.bitbucket.org/2.0",
).rstrip("/")
BITBUCKET_USERNAME = os.getenv("BITBUCKET_USERNAME", "")
BITBUCKET_APP_PASSWORD = os.getenv("BITBUCKET_APP_PASSWORD", "")
BITBUCKET_ACCESS_TOKEN = os.getenv("BITBUCKET_ACCESS_TOKEN", "")
BITBUCKET_DEFAULT_WORKSPACE = os.getenv("BITBUCKET_DEFAULT_WORKSPACE", "")
BITBUCKET_DEFAULT_REPO_SLUG = os.getenv("BITBUCKET_DEFAULT_REPO_SLUG", "")

REPOSITORIES_ROOT = Path(
    os.getenv("REPOSITORIES_ROOT", str(Path(__file__).resolve().parents[2]))
).expanduser().resolve()

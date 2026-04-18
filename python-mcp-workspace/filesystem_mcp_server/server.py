from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .config import REPOSITORIES_ROOT
from .path_utils import (
    resolve_inside_root,
    validate_content,
    validate_relative_path,
)

mcp = FastMCP("filesystem-mcp")


@mcp.tool()
def get_workspace_root() -> dict:
    """Get the configured local repositories workspace root."""
    return {"repositoriesRoot": str(REPOSITORIES_ROOT)}


@mcp.tool()
def list_repositories() -> dict:
    """List directories directly inside the repositories workspace root."""
    repositories = sorted(
        entry.name for entry in REPOSITORIES_ROOT.iterdir() if entry.is_dir()
    )

    return {
        "repositoriesRoot": str(REPOSITORIES_ROOT),
        "repositories": repositories,
    }


@mcp.tool()
def list_directory(relative_path: str) -> dict:
    """List files and folders inside a directory under the repositories workspace root."""
    validate_relative_path(relative_path)

    directory_path = resolve_inside_root(relative_path)
    items = []

    for entry in directory_path.iterdir():
        items.append(
            {
                "name": entry.name,
                "type": "directory" if entry.is_dir() else "file",
                "relativePath": str(entry.relative_to(REPOSITORIES_ROOT)),
            }
        )

    return {
        "relativePath": relative_path,
        "items": sorted(items, key=lambda item: item["relativePath"]),
    }


@mcp.tool()
def read_file(relative_path: str) -> dict:
    """Read a UTF-8 text file under the repositories workspace root."""
    validate_relative_path(relative_path)

    file_path = resolve_inside_root(relative_path)

    return {
        "relativePath": relative_path,
        "content": file_path.read_text(encoding="utf-8"),
    }


@mcp.tool()
def write_file(relative_path: str, content: str) -> dict:
    """Create or replace a UTF-8 text file under the repositories workspace root."""
    validate_relative_path(relative_path)
    validate_content(content)

    file_path = resolve_inside_root(relative_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")

    return {
        "relativePath": relative_path,
        "bytesWritten": len(content.encode("utf-8")),
    }


@mcp.tool()
def append_file(relative_path: str, content: str) -> dict:
    """Append UTF-8 text to a file under the repositories workspace root."""
    validate_relative_path(relative_path)
    validate_content(content)

    file_path = resolve_inside_root(relative_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("a", encoding="utf-8") as file:
        file.write(content)

    return {
        "relativePath": relative_path,
        "bytesAppended": len(content.encode("utf-8")),
    }


@mcp.tool()
def create_directory(relative_path: str) -> dict:
    """Create a directory under the repositories workspace root."""
    validate_relative_path(relative_path)

    directory_path = resolve_inside_root(relative_path)
    existed_before = directory_path.exists()
    directory_path.mkdir(parents=True, exist_ok=True)

    return {
        "relativePath": relative_path,
        "created": not existed_before,
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")

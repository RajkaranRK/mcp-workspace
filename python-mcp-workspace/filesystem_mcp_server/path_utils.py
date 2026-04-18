from pathlib import Path

from .config import REPOSITORIES_ROOT


def validate_relative_path(relative_path: str) -> None:
    if not isinstance(relative_path, str) or not relative_path.strip():
        raise ValueError("relative_path must be a non-empty string")


def validate_content(content: str) -> None:
    if not isinstance(content, str):
        raise ValueError("content must be a string")


def resolve_inside_root(relative_path: str = ".") -> Path:
    if not isinstance(relative_path, str):
        raise ValueError("relative_path must be a string")

    resolved_path = (REPOSITORIES_ROOT / relative_path).resolve()

    try:
      resolved_path.relative_to(REPOSITORIES_ROOT)
    except ValueError as exc:
        raise ValueError("Path is outside the configured repositories root") from exc

    return resolved_path

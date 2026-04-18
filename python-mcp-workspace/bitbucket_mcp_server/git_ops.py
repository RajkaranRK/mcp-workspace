import subprocess
from pathlib import Path

from .config import REPOSITORIES_ROOT


def resolve_repository(repository_path: str) -> Path:
    if not isinstance(repository_path, str) or not repository_path.strip():
        raise ValueError("repository_path must be a non-empty string")

    resolved = (REPOSITORIES_ROOT / repository_path).resolve()
    try:
        resolved.relative_to(REPOSITORIES_ROOT)
    except ValueError as exc:
        raise ValueError("Repository path is outside REPOSITORIES_ROOT") from exc

    if not resolved.exists() or not resolved.is_dir():
        raise ValueError(f"Repository path does not exist: {repository_path}")

    git_dir = resolved / ".git"
    if not git_dir.exists():
        raise ValueError(f"Repository path is not a Git repository: {repository_path}")

    return resolved


def run_git(repository_path: str, args: list[str], check: bool = True) -> dict:
    repository = resolve_repository(repository_path)
    result = subprocess.run(
        ["git", *args],
        cwd=repository,
        text=True,
        capture_output=True,
        check=False,
    )

    output = {
        "repositoryPath": repository_path,
        "command": ["git", *args],
        "returnCode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }

    if check and result.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed with code {result.returncode}: "
            f"{result.stderr.strip() or result.stdout.strip()}"
        )

    return output


def status(repository_path: str) -> dict:
    return run_git(repository_path, ["status", "--short"], check=True)


def checkout_branch(
    repository_path: str,
    branch: str,
    create: bool = False,
    start_point: str = "",
) -> dict:
    if not branch:
        raise ValueError("branch is required")

    args = ["checkout"]
    if create:
        args.append("-b")
    args.append(branch)
    if start_point:
        args.append(start_point)

    result = run_git(repository_path, args, check=True)
    result["branch"] = branch
    result["created"] = create
    return result


def fetch(repository_path: str, remote: str = "origin") -> dict:
    return run_git(repository_path, ["fetch", remote], check=True)


def merge_branch(
    repository_path: str,
    source_branch: str,
    destination_branch: str,
    remote: str = "origin",
) -> dict:
    if not source_branch:
        raise ValueError("source_branch is required")
    if not destination_branch:
        raise ValueError("destination_branch is required")

    fetch_result = fetch(repository_path, remote)
    checkout_result = checkout_branch(repository_path, destination_branch)
    merge_result = run_git(repository_path, ["merge", source_branch], check=False)
    conflicts = conflicted_files(repository_path)

    return {
        "repositoryPath": repository_path,
        "sourceBranch": source_branch,
        "destinationBranch": destination_branch,
        "remote": remote,
        "fetch": fetch_result,
        "checkout": checkout_result,
        "merge": merge_result,
        "hasConflicts": bool(conflicts["files"]),
        "conflicts": conflicts["files"],
    }


def conflicted_files(repository_path: str) -> dict:
    result = run_git(
        repository_path,
        ["diff", "--name-only", "--diff-filter=U"],
        check=True,
    )
    files = [line for line in result["stdout"].splitlines() if line]
    return {
        "repositoryPath": repository_path,
        "files": files,
    }


def mark_resolved(
    repository_path: str,
    files: list[str],
    commit_message: str = "",
) -> dict:
    if not files:
        raise ValueError("files must contain at least one path")

    add_result = run_git(repository_path, ["add", *files], check=True)
    commit_result = None
    if commit_message:
        commit_result = run_git(repository_path, ["commit", "-m", commit_message], check=True)

    return {
        "repositoryPath": repository_path,
        "files": files,
        "add": add_result,
        "commit": commit_result,
    }


def continue_merge(repository_path: str, message: str = "") -> dict:
    args = ["commit", "--no-edit"]
    if message:
        args = ["commit", "-m", message]
    return run_git(repository_path, args, check=True)


def abort_merge(repository_path: str) -> dict:
    return run_git(repository_path, ["merge", "--abort"], check=True)

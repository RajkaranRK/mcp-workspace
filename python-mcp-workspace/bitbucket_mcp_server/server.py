from typing import Any

from mcp.server.fastmcp import FastMCP

from . import git_ops
from .client import BitbucketClient, quote_path, repo_slug_or_default, workspace_or_default
from .config import (
    BITBUCKET_ACCESS_TOKEN,
    BITBUCKET_APP_PASSWORD,
    BITBUCKET_BASE_URL,
    BITBUCKET_DEFAULT_REPO_SLUG,
    BITBUCKET_DEFAULT_WORKSPACE,
    BITBUCKET_USERNAME,
    REPOSITORIES_ROOT,
)

mcp = FastMCP("bitbucket-mcp")
client = BitbucketClient()


def _pr_path(workspace: str, repo_slug: str, pull_request_id: int | None = None) -> str:
    base = (
        f"/repositories/{quote_path(workspace_or_default(workspace))}/"
        f"{quote_path(repo_slug_or_default(repo_slug))}/pullrequests"
    )
    if pull_request_id is None:
        return base
    return f"{base}/{pull_request_id}"


@mcp.tool()
def bitbucket_config_status() -> dict:
    """Show Bitbucket MCP configuration status without exposing secrets."""
    return {
        "baseUrl": BITBUCKET_BASE_URL,
        "defaultWorkspace": BITBUCKET_DEFAULT_WORKSPACE,
        "defaultRepoSlug": BITBUCKET_DEFAULT_REPO_SLUG,
        "repositoriesRoot": str(REPOSITORIES_ROOT),
        "auth": {
            "hasAccessToken": bool(BITBUCKET_ACCESS_TOKEN),
            "hasUsername": bool(BITBUCKET_USERNAME),
            "hasAppPassword": bool(BITBUCKET_APP_PASSWORD),
        },
    }


@mcp.tool()
def list_pull_requests(
    workspace: str = "",
    repo_slug: str = "",
    state: str = "OPEN",
    page: int = 1,
    pagelen: int = 10,
) -> dict:
    """List pull requests for a Bitbucket Cloud repository."""
    return client.request(
        "GET",
        _pr_path(workspace, repo_slug),
        {"state": state, "page": page, "pagelen": pagelen},
    )


@mcp.tool()
def get_pull_request(
    pull_request_id: int,
    workspace: str = "",
    repo_slug: str = "",
) -> dict:
    """Get a Bitbucket Cloud pull request by id."""
    return client.request("GET", _pr_path(workspace, repo_slug, pull_request_id))


@mcp.tool()
def create_pull_request(
    title: str,
    source_branch: str,
    destination_branch: str = "",
    description: str = "",
    reviewers: list[dict[str, Any]] | None = None,
    close_source_branch: bool = False,
    draft: bool = False,
    workspace: str = "",
    repo_slug: str = "",
) -> dict:
    """Create a Bitbucket Cloud pull request."""
    if not title:
        raise ValueError("title is required")
    if not source_branch:
        raise ValueError("source_branch is required")

    body: dict[str, Any] = {
        "title": title,
        "source": {"branch": {"name": source_branch}},
        "close_source_branch": close_source_branch,
        "draft": draft,
    }
    if description:
        body["description"] = description
    if destination_branch:
        body["destination"] = {"branch": {"name": destination_branch}}
    if reviewers:
        body["reviewers"] = reviewers

    return client.request("POST", _pr_path(workspace, repo_slug), body=body)


@mcp.tool()
def approve_pull_request(
    pull_request_id: int,
    workspace: str = "",
    repo_slug: str = "",
) -> dict:
    """Approve a Bitbucket Cloud pull request as the authenticated user."""
    return client.request(
        "POST",
        f"{_pr_path(workspace, repo_slug, pull_request_id)}/approve",
    )


@mcp.tool()
def request_pull_request_changes(
    pull_request_id: int,
    workspace: str = "",
    repo_slug: str = "",
) -> dict:
    """Request changes on a Bitbucket Cloud pull request."""
    return client.request(
        "POST",
        f"{_pr_path(workspace, repo_slug, pull_request_id)}/request-changes",
    )


@mcp.tool()
def merge_pull_request(
    pull_request_id: int,
    confirm: bool,
    workspace: str = "",
    repo_slug: str = "",
    merge_strategy: str = "merge_commit",
    close_source_branch: bool = False,
    message: str = "",
) -> dict:
    """Merge a Bitbucket Cloud pull request. Requires confirm: true."""
    if not confirm:
        raise ValueError("confirm must be true to merge a pull request")

    body: dict[str, Any] = {
        "merge_strategy": merge_strategy,
        "close_source_branch": close_source_branch,
    }
    if message:
        body["message"] = message

    return client.request(
        "POST",
        f"{_pr_path(workspace, repo_slug, pull_request_id)}/merge",
        body=body,
    )


@mcp.tool()
def list_pull_request_comments(
    pull_request_id: int,
    workspace: str = "",
    repo_slug: str = "",
    page: int = 1,
    pagelen: int = 20,
) -> dict:
    """List comments on a Bitbucket Cloud pull request."""
    return client.request(
        "GET",
        f"{_pr_path(workspace, repo_slug, pull_request_id)}/comments",
        {"page": page, "pagelen": pagelen},
    )


@mcp.tool()
def add_pull_request_comment(
    pull_request_id: int,
    content: str,
    workspace: str = "",
    repo_slug: str = "",
    inline_path: str = "",
    line_to: int | None = None,
    line_from: int | None = None,
    pending: bool = False,
) -> dict:
    """Add a global or inline comment to a Bitbucket Cloud pull request."""
    if not content:
        raise ValueError("content is required")

    body: dict[str, Any] = {
        "content": {"raw": content},
        "pending": pending,
    }
    if inline_path:
        inline: dict[str, Any] = {"path": inline_path}
        if line_to is not None:
            inline["to"] = line_to
        if line_from is not None:
            inline["from"] = line_from
        body["inline"] = inline

    return client.request(
        "POST",
        f"{_pr_path(workspace, repo_slug, pull_request_id)}/comments",
        body=body,
    )


@mcp.tool()
def resolve_pull_request_comment(
    pull_request_id: int,
    comment_id: int,
    workspace: str = "",
    repo_slug: str = "",
) -> dict:
    """Resolve a pull request comment thread."""
    return client.request(
        "POST",
        f"{_pr_path(workspace, repo_slug, pull_request_id)}/comments/{comment_id}/resolve",
    )


@mcp.tool()
def list_pull_request_diffstat(
    pull_request_id: int,
    workspace: str = "",
    repo_slug: str = "",
    page: int = 1,
    pagelen: int = 50,
) -> dict:
    """List changed files and diff stats for a pull request."""
    return client.request(
        "GET",
        f"{_pr_path(workspace, repo_slug, pull_request_id)}/diffstat",
        {"page": page, "pagelen": pagelen},
    )


@mcp.tool()
def checkout_branch(
    repository_path: str,
    branch: str,
    create: bool = False,
    start_point: str = "",
) -> dict:
    """Checkout a local Git branch under REPOSITORIES_ROOT."""
    return git_ops.checkout_branch(repository_path, branch, create, start_point)


@mcp.tool()
def merge_branch_locally(
    repository_path: str,
    source_branch: str,
    destination_branch: str,
    remote: str = "origin",
) -> dict:
    """Fetch, checkout destination branch, and merge source branch locally."""
    return git_ops.merge_branch(repository_path, source_branch, destination_branch, remote)


@mcp.tool()
def get_merge_conflicts(repository_path: str) -> dict:
    """List files currently in Git merge conflict."""
    return git_ops.conflicted_files(repository_path)


@mcp.tool()
def mark_conflicts_resolved(
    repository_path: str,
    files: list[str],
    commit_message: str = "",
) -> dict:
    """Mark conflict files resolved with git add, optionally committing them."""
    return git_ops.mark_resolved(repository_path, files, commit_message)


@mcp.tool()
def continue_merge(repository_path: str, message: str = "") -> dict:
    """Continue a merge after conflicts are resolved."""
    return git_ops.continue_merge(repository_path, message)


@mcp.tool()
def abort_merge(repository_path: str) -> dict:
    """Abort the current Git merge."""
    return git_ops.abort_merge(repository_path)


if __name__ == "__main__":
    mcp.run(transport="stdio")

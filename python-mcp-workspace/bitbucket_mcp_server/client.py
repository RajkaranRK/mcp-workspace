import base64
import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from .config import (
    BITBUCKET_ACCESS_TOKEN,
    BITBUCKET_APP_PASSWORD,
    BITBUCKET_BASE_URL,
    BITBUCKET_DEFAULT_REPO_SLUG,
    BITBUCKET_DEFAULT_WORKSPACE,
    BITBUCKET_USERNAME,
)


class BitbucketApiError(RuntimeError):
    def __init__(self, status: int | None, message: str, response: Any = None):
        super().__init__(message)
        self.status = status
        self.response = response


def _required(value: str, name: str) -> str:
    if not value:
        raise ValueError(f"{name} is required")
    return value


def workspace_or_default(workspace: str = "") -> str:
    return _required(workspace or BITBUCKET_DEFAULT_WORKSPACE, "workspace")


def repo_slug_or_default(repo_slug: str = "") -> str:
    return _required(repo_slug or BITBUCKET_DEFAULT_REPO_SLUG, "repo_slug")


def quote_path(value: str) -> str:
    return quote(str(value), safe="")


class BitbucketClient:
    def __init__(self) -> None:
        self.base_url = BITBUCKET_BASE_URL

    def request(
        self,
        method: str,
        path: str,
        query: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
    ) -> Any:
        url = f"{self.base_url}{path}"
        if query:
            clean_query = {
                key: value
                for key, value in query.items()
                if value is not None and value != ""
            }
            if clean_query:
                url = f"{url}?{urlencode(clean_query, doseq=True)}"

        data = None
        headers = {
            "Accept": "application/json",
            "User-Agent": "bitbucket-mcp-python/1.0",
        }
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"

        auth_header = self._auth_header()
        if auth_header:
            headers["Authorization"] = auth_header

        request = Request(url, data=data, headers=headers, method=method.upper())

        try:
            with urlopen(request, timeout=30) as response:
                response_body = response.read().decode("utf-8")
                if not response_body:
                    return {"status": response.status}
                return json.loads(response_body)
        except HTTPError as exc:
            response_text = exc.read().decode("utf-8", errors="replace")
            parsed_response: Any
            try:
                parsed_response = json.loads(response_text)
            except json.JSONDecodeError:
                parsed_response = response_text

            raise BitbucketApiError(
                exc.code,
                f"Bitbucket API request failed with HTTP {exc.code}",
                parsed_response,
            ) from exc
        except URLError as exc:
            raise BitbucketApiError(None, f"Bitbucket API request failed: {exc}") from exc

    def _auth_header(self) -> str:
        if BITBUCKET_ACCESS_TOKEN:
            return f"Bearer {BITBUCKET_ACCESS_TOKEN}"

        if BITBUCKET_USERNAME and BITBUCKET_APP_PASSWORD:
            credentials = f"{BITBUCKET_USERNAME}:{BITBUCKET_APP_PASSWORD}".encode(
                "utf-8"
            )
            encoded = base64.b64encode(credentials).decode("ascii")
            return f"Basic {encoded}"

        return ""

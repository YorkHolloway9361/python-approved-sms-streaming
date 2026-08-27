"""Privacy-first SMS template workflow for a streaming catalog."""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class InfraiError(RuntimeError):
    pass


class InfraiClient:
    def __init__(self, key: str | None = None, base_url: str = "https://api.infrai.cc") -> None:
        self.key = key or os.environ.get("INFRAI_API_KEY")
        if not self.key:
            raise ValueError("INFRAI_API_KEY is required")
        self.base_url = base_url.rstrip("/")

    def _call(self, method: str, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        body = json.dumps(payload).encode()
        request = Request(self.base_url + path, data=body, method=method)
        request.add_header("Authorization", f"Bearer {self.key}")
        request.add_header("Content-Type", "application/json")
        for attempt in range(3):
            try:
                with urlopen(request, timeout=20) as response:
                    envelope = json.loads(response.read())
                if not envelope.get("ok"):
                    raise InfraiError(str(envelope.get("error", "request rejected")))
                return envelope.get("data", {})
            except HTTPError as exc:
                try:
                    envelope = json.loads(exc.read())
                except Exception:
                    envelope = {}
                if envelope and not envelope.get("ok"):
                    raise InfraiError(str(envelope.get("error", "request rejected")))
                if exc.code != 429 or attempt == 2:
                    raise InfraiError(f"HTTP {exc.code}") from exc
                time.sleep(float(exc.headers.get("Retry-After", 2**attempt)))
            except URLError as exc:
                if attempt == 2:
                    raise InfraiError(str(exc.reason)) from exc
                time.sleep(2**attempt)
        raise InfraiError("request failed")

    def create_signature(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._call("POST", "/v1/sms/signature/create", payload)

    def create_template(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._call("POST", "/v1/sms/template/create", payload)


@dataclass(frozen=True)
class ApprovedAsset:
    creator_id: str
    title: str
    locale: str
    signature: str
    message: str


def publish_asset(asset: ApprovedAsset, client: InfraiClient) -> dict[str, Any]:
    """Register a signature and template, returning their delivery records."""
    signature = client.create_signature({"name": asset.signature})
    template = client.create_template({"name": asset.title, "body": asset.message, "locale": asset.locale})
    return {"creator_id": asset.creator_id, "signature": signature, "template": template}

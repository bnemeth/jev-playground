import os
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv("../.env")

def call_jev(
    payload: dict[str, Any],
    timeout: float = 10.0,
    base_url: str | None = None,
    api_key: str | None = None,
    path: str = "v1/systemone",
) -> dict[str, Any]:
    api_key_value = api_key or os.environ.get("TYPESAFE_API_KEY")
    if not api_key_value:
        raise ValueError(
            "JEV API key not found. Pass api_key or set TYPESAFE_API_KEY."
        )

    api_base_url = base_url or os.environ.get("TYPESAFE_BASE_URL")
    if not api_base_url:
        raise ValueError(
            "JEV base URL not found. Pass base_url or set TYPESAFE_BASE_URL."
        )

    response = httpx.post(
        url=f"{api_base_url.rstrip('/')}/{path.lstrip('/')}",
        headers={"Authorization": f"Bearer {api_key_value}"},
        json=payload,
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()

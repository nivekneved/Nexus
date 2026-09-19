"""
HTTP Connection Pool Singleton for Nexus Subagents.
Eliminates TCP connection exhaustion and overhead by sharing persistent httpx.AsyncClient sessions.
"""

from __future__ import annotations

import asyncio
from typing import Optional, Dict, Any
import httpx

class HttpClientPool:
    _instance: Optional[HttpClientPool] = None
    _client: Optional[httpx.AsyncClient] = None
    _lock: asyncio.Lock = asyncio.Lock()

    def __new__(cls) -> HttpClientPool:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    async def get_client(cls, timeout: float = 30.0, max_connections: int = 100, max_keepalive: int = 20) -> httpx.AsyncClient:
        """Returns the shared httpx.AsyncClient instance, initializing lazily if needed."""
        if cls._client is None or cls._client.is_closed:
            async with cls._lock:
                if cls._client is None or cls._client.is_closed:
                    limits = httpx.Limits(
                        max_connections=max_connections,
                        max_keepalive_connections=max_keepalive,
                        keepalive_expiry=60.0
                    )
                    cls._client = httpx.AsyncClient(
                        limits=limits,
                        timeout=httpx.Timeout(timeout, connect=10.0),
                        follow_redirects=True
                    )
        return cls._client

    @classmethod
    async def close(cls) -> None:
        """Gracefully close the pooled client."""
        async with cls._lock:
            if cls._client is not None and not cls._client.is_closed:
                await cls._client.aclose()
                cls._client = None

    @classmethod
    async def request(
        cls,
        method: str,
        url: str,
        retries: int = 2,
        backoff_factor: float = 0.5,
        **kwargs: Any
    ) -> httpx.Response:
        """Execute a pooled HTTP request with automatic retry on network glitches."""
        client = await cls.get_client()
        last_err: Optional[Exception] = None
        for attempt in range(retries + 1):
            try:
                response = await client.request(method, url, **kwargs)
                return response
            except (httpx.ConnectError, httpx.ReadTimeout, httpx.NetworkError) as err:
                last_err = err
                if attempt < retries:
                    await asyncio.sleep(backoff_factor * (2 ** attempt))
                else:
                    raise last_err
        raise RuntimeError("Unreachable retry state in HttpClientPool")

# Convenience module-level functions
async def get_http_client() -> httpx.AsyncClient:
    return await HttpClientPool.get_client()

async def close_http_client() -> None:
    await HttpClientPool.close()

async def pooled_request(method: str, url: str, **kwargs: Any) -> httpx.Response:
    return await HttpClientPool.request(method, url, **kwargs)

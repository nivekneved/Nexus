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


# ============================================================================
# SYNCHRONOUS POOLED CLIENT + TTL RESPONSE CACHE FOR SYNC AGENTS & OSINT
# ============================================================================
import time
import threading

_SYNC_CLIENT: Optional[httpx.Client] = None
_SYNC_LOCK = threading.Lock()
_HTTP_TTL_CACHE: Dict[str, Dict[str, Any]] = {}

def get_sync_http_client(timeout: float = 15.0) -> httpx.Client:
    """Returns a persistent thread-safe synchronous httpx.Client with connection pooling."""
    global _SYNC_CLIENT
    if _SYNC_CLIENT is None or _SYNC_CLIENT.is_closed:
        with _SYNC_LOCK:
            if _SYNC_CLIENT is None or _SYNC_CLIENT.is_closed:
                limits = httpx.Limits(
                    max_connections=50,
                    max_keepalive_connections=20,
                    keepalive_expiry=60.0
                )
                _SYNC_CLIENT = httpx.Client(
                    limits=limits,
                    timeout=httpx.Timeout(timeout, connect=8.0),
                    follow_redirects=True
                )
    return _SYNC_CLIENT

def cached_sync_request(
    method: str,
    url: str,
    ttl_seconds: int = 600,
    headers: Optional[Dict[str, str]] = None,
    json_payload: Optional[Dict[str, Any]] = None,
    timeout: float = 15.0
) -> Dict[str, Any]:
    """
    Executes a pooled synchronous HTTP request with in-memory TTL caching for GET requests.
    Eliminates redundant TCP/TLS handshakes and duplicate external API hits.
    """
    m = method.upper()
    from security.shield import shield
    if not shield.validate_outgoing_url(url):
        return {
            "success": False,
            "status_code": 403,
            "url": url,
            "execution_time_ms": 0.0,
            "content": "",
            "headers": {},
            "cache_hit": False,
            "error": f"Zero-Day SSRF / Cloud Metadata Guard blocked URL: {url}"
        }
    cache_key = f"{m}:{url}"
    now = time.time()

    if m == "GET" and ttl_seconds > 0 and cache_key in _HTTP_TTL_CACHE:
        entry = _HTTP_TTL_CACHE[cache_key]
        if now - entry["ts"] < ttl_seconds:
            cached_res = dict(entry["data"])
            cached_res["cache_hit"] = True
            return cached_res

    client = get_sync_http_client(timeout=timeout)
    t0 = time.time()
    req_kwargs: Dict[str, Any] = {"timeout": timeout}
    if headers:
        req_kwargs["headers"] = headers
    if json_payload is not None and m in ("POST", "PUT", "PATCH"):
        req_kwargs["json"] = json_payload

    resp = client.request(m, url, **req_kwargs)
    elapsed_ms = round((time.time() - t0) * 1000.0, 1)
    raw_snippet = resp.text[:15000]
    sanitized_snippet = shield.sanitize_indirect_prompt_injection(raw_snippet)["clean_text"]
    result = {
        "success": 200 <= resp.status_code < 400,
        "status_code": resp.status_code,
        "url": str(resp.url),
        "execution_time_ms": elapsed_ms,
        "content": sanitized_snippet,
        "headers": dict(resp.headers),
        "cache_hit": False
    }
    if m == "GET" and result["success"] and ttl_seconds > 0:
        if len(_HTTP_TTL_CACHE) > 500:
            _HTTP_TTL_CACHE.clear()
        _HTTP_TTL_CACHE[cache_key] = {"ts": now, "data": result}
    return result

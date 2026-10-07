"""
LeadScout-Core: Network Client Wrapper
======================================
Async HTTP/2, DNS, and zero-send SMTP client wrapper.
"""

import asyncio
import httpx
import dns.resolver
import smtplib
import socket
from typing import List, Dict, Any, Optional

class NetworkClient:
    @staticmethod
    async def get_http_client() -> httpx.AsyncClient:
        return httpx.AsyncClient(http2=True, timeout=10.0, follow_redirects=True, headers={"User-Agent": "LeadScout-Core/1.0"})

    @staticmethod
    async def resolve_dns_mx(domain: str) -> List[str]:
        loop = asyncio.get_running_loop()
        try:
            answers = await loop.run_in_executor(None, dns.resolver.resolve, domain, 'MX')
            return [str(r.exchange).rstrip('.') for r in answers]
        except Exception:
            return []

    @staticmethod
    async def resolve_dns_txt(domain: str) -> List[str]:
        loop = asyncio.get_running_loop()
        try:
            answers = await loop.run_in_executor(None, dns.resolver.resolve, domain, 'TXT')
            return [str(r).strip('"') for r in answers]
        except Exception:
            return []

    @staticmethod
    async def test_smtp_handshake(mx_host: str, recipient: str, sender: str = "probe@leadscout.io") -> bool:
        loop = asyncio.get_running_loop()
        def _smtp_check():
            try:
                server = smtplib.SMTP(timeout=5)
                server.connect(mx_host, 25)
                server.helo("leadscout.io")
                server.mail(sender)
                code, _ = server.rcpt(recipient)
                server.quit()
                return code == 250
            except Exception:
                return False
        return await loop.run_in_executor(None, _smtp_check)

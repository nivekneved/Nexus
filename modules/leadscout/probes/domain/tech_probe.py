"""
LeadScout-Core: Tech Stack Probe
================================
Inspects HTTP response headers and markup signatures to detect technology stack.
"""

from typing import Dict, Any
from leadscout.probes.base import BaseProbe
from leadscout.core.card import LeadCard
from leadscout.core.network import NetworkClient

class InspectWebTechStackTask(BaseProbe):
    name = "InspectWebTechStackTask"

    async def execute(self, card: LeadCard) -> Dict[str, Any]:
        if not card.domain:
            return {}

        tech_stack = []
        url = f"https://{card.domain}"
        client = await NetworkClient.get_http_client()
        try:
            resp = await client.get(url)
            headers = {k.lower(): v.lower() for k, v in resp.headers.items()}
            html = resp.text.lower()

            if "server" in headers:
                tech_stack.append(headers["server"])
            if "x-powered-by" in headers:
                tech_stack.append(headers["x-powered-by"])
            if "wordpress" in html or "wp-content" in html:
                tech_stack.append("WordPress")
            if "react" in html or "__next" in html:
                tech_stack.append("React / Next.js")
            if "shopify" in html:
                tech_stack.append("Shopify")
            if "tailwind" in html:
                tech_stack.append("Tailwind CSS")
        except Exception:
            pass
        finally:
            await client.aclose()

        return {"tech_stack": list(set(tech_stack))}

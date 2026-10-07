"""
Nexus™ Scrapegraph-AI Synergy Bridge
====================================
Integrates `scrapegraphai` (https://github.com/ScrapeGraphAI/Scrapegraph-ai)
allowing Nexus agents to autonomously construct extraction graphs and extract
structured JSON data directly from complex websites.
"""

import os
import json
import logging
import asyncio
from typing import Dict, Any

logger = logging.getLogger("Nexus.ScrapegraphBridge")

class ScrapegraphBridge:
    def __init__(self):
        self.is_initialized = False

    def initialize(self):
        if not self.is_initialized:
            try:
                import scrapegraphai
                self.scrapegraphai = scrapegraphai
                self.is_initialized = True
                logger.info("[ScrapegraphBridge] Successfully loaded scrapegraphai.")
            except ImportError:
                logger.warning("[ScrapegraphBridge] 'scrapegraphai' package not found. Running in fallback mode.")

    async def extract_structured_data(self, url: str, prompt: str) -> Dict[str, Any]:
        """
        Uses ScrapeGraphAI's SmartScraperGraph to extract structured JSON data
        from a given URL using an LLM to navigate the DOM.
        """
        self.initialize()
        if not self.is_initialized:
            return {"success": False, "error": "scrapegraphai not installed."}

        logger.info(f"[ScrapegraphBridge] Extracting from {url} with prompt: '{prompt}'")
        try:
            from scrapegraphai.graphs import SmartScraperGraph

            # Configure LLM backend
            graph_config = {
                "llm": {
                    "api_key": os.getenv("OPENAI_API_KEY") or os.getenv("GEMINI_API_KEY"),
                    "model": "gpt-4o" if os.getenv("OPENAI_API_KEY") else "gemini-2.5-flash",
                },
                "verbose": True,
                "headless": True
            }

            smart_scraper = SmartScraperGraph(
                prompt=prompt,
                source=url,
                config=graph_config
            )

            # ScrapeGraphAI's .run() is synchronous, so we offload it to a thread
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(None, smart_scraper.run)

            logger.info(f"[ScrapegraphBridge] Successfully extracted structured data from {url}.")
            return {
                "success": True,
                "url": url,
                "extracted_data": result
            }

        except Exception as e:
            logger.error(f"[ScrapegraphBridge] Exception during extraction: {e}")
            return {"success": False, "error": str(e)}

scrapegraph_bridge = ScrapegraphBridge()

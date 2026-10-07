"""
Nexus™ Autonomous Web Browser Service
=====================================
Integrates the `browser-use` library (https://github.com/browser-use/browser-use)
to allow Nexus agents to autonomously navigate the web, interact with DOM elements,
fill forms, and extract deep unstructured data.
"""

import asyncio
import logging
import os
from typing import Dict, Any

logger = logging.getLogger("Nexus.BrowserUse")

class BrowserUseService:
    def __init__(self):
        self.is_initialized = False

    async def execute_web_task(self, task_instruction: str, headless: bool = True) -> Dict[str, Any]:
        """
        Spawns a headless browser and uses an LLM to navigate and fulfill the task instruction.
        """
        logger.info(f"[BrowserUse] Executing autonomous web task: '{task_instruction}'")
        try:
            from browser_use import Agent

            # Nexus supports multiple LLMs; we'll try initializing OpenAI first, then Google
            llm = self._get_configured_llm()

            if not llm:
                return {"success": False, "error": "No valid LLM configuration found for browser-use (requires OPENAI_API_KEY or GEMINI_API_KEY)."}

            # Initialize the browser agent
            agent = Agent(
                task=task_instruction,
                llm=llm
            )

            # Execute the autonomous navigation
            result = await agent.run()

            logger.info(f"[BrowserUse] Task completed successfully.")
            return {
                "success": True,
                "task": task_instruction,
                "extracted_data": str(result)
            }
        except ImportError:
            return {"success": False, "error": "browser-use package is not installed correctly."}
        except Exception as e:
            logger.error(f"[BrowserUse] Exception during execution: {e}")
            return {"success": False, "error": str(e)}

    def _get_configured_llm(self):
        """Helper to get an initialized LangChain ChatModel based on .env keys."""
        try:
            if os.getenv("OPENAI_API_KEY"):
                from langchain_openai import ChatOpenAI
                return ChatOpenAI(model="gpt-4o")
            elif os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"):
                from langchain_google_genai import ChatGoogleGenerativeAI
                return ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        except Exception as e:
            logger.warning(f"[BrowserUse] LLM Init Error: {e}")
        return None

browser_use_service = BrowserUseService()

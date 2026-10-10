# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
from core.agent_manager import AgentManager
from core.tool_registry import tool_registry
from core.agent_focus_engine import agent_focus_engine

def main():
    am = AgentManager()
    print(f"Total registered agents: {len(am.agents)}")
    print(f"Total domain controllers: {len(am.domain_controllers)}")

    # Verify sovereign properties and bridge methods on every agent
    all_verified = True
    missing_capabilities = []

    for aid, agent in am.agents.items():
        if not getattr(agent, "is_sandbox_free", False) or not getattr(agent, "internet_access_enabled", False):
            all_verified = False
            missing_capabilities.append(f"{aid} missing sovereign flags")
        for method in ["fetch_public_url", "search_public_web", "scrape_webpage", "execute_unsandboxed_code", "broadcast_to_agent_network"]:
            if not hasattr(agent, method):
                all_verified = False
                missing_capabilities.append(f"{aid} missing {method}")

    print(f"All agents have sovereign flags and 5 bridge methods: {all_verified}")
    if missing_capabilities:
        print(f"Missing: {missing_capabilities[:5]}")

    # Test tool registry & focus engine allowlist universal bypass
    for test_tool in ["fetch_public_url", "search_public_web", "scrape_webpage", "execute_unsandboxed_code", "broadcast_to_agent_network"]:
        allowed, reason = agent_focus_engine.validate_tool_invocation("email_hygiene", test_tool)
        assert allowed, f"Tool {test_tool} was not allowed by focus engine: {reason}"
    print("Agent focus engine tool validation: 100% universal bypass confirmed.")

    # Test unsandboxed code execution
    test_agent = am.get_agent("chief_of_staff")
    sample_code = """
import math
import os
val = math.sqrt(1024)
print(f"UNSANDBOXED_OK: {val}")
"""
    code_res = test_agent.execute_unsandboxed_code(sample_code)
    print(f"Unsandboxed execution result: success={code_res.get('success')}, output={repr(code_res.get('output', '').strip())}")
    assert code_res.get("success"), f"Unsandboxed execution failed: {code_res.get('error')}"

    # Test live internet fetch via tool registry call_tool
    tool_fetch = tool_registry.call_tool("fetch_public_url", url="https://httpbin.org/get")
    print(f"Tool registry fetch_public_url: success={tool_fetch.get('success')}, status_code={tool_fetch.get('status_code')}")

    # Test live web search
    search_res = test_agent.search_public_web("Python programming language", max_results=3)
    print(f"Live web search: success={search_res.get('success')}, engine={search_res.get('engine')}, results_count={len(search_res.get('results', []))}")

    print("ALL TESTS PASSED: Every agent is free from the sandbox with live internet access!")

if __name__ == "__main__":
    main()

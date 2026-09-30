import sys
import os
import traceback

# Enforce Vercel runtime flag
os.environ["VERCEL"] = "1"

# Add root directory to sys.path so server and core modules import cleanly on Vercel
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

try:
    from server import app as fastapi_app

    async def app(scope, receive, send):
        """Universal ASGI entrypoint for Vercel Serverless."""
        if scope["type"] == "http":
            path = scope.get("path", "")
            # Normalize path so routes match whether Vercel preserves or strips /api prefix
            if not path.startswith("/api/") and not path.startswith("/static/") and not path.startswith("/download/"):
                if path == "/status" or path.startswith("/triage") or path.startswith("/partner") or path.startswith("/ledger") or path.startswith("/outreach") or path.startswith("/email") or path.startswith("/tasks") or path.startswith("/leads") or path.startswith("/agents") or path.startswith("/events") or path.startswith("/scheduler") or path.startswith("/workspace") or path.startswith("/finance") or path.startswith("/growth") or path.startswith("/security"):
                    scope = dict(scope)
                    scope["path"] = "/api" + path
        await fastapi_app(scope, receive, send)

except Exception as e:
    import logging
    logging.exception("Fatal error importing server on Vercel")
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse

    fallback_app = FastAPI(title="Nexus Error Handler")
    tb = traceback.format_exc()

    @fallback_app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    async def catch_all_error(path_name: str):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Serverless Initialization Error",
                "detail": str(e),
                "traceback": tb.splitlines()[-15:]
            }
        )

    app = fallback_app

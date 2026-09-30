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
    from server import app
except Exception as e:
    import logging
    logging.exception("Fatal error importing server on Vercel")
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse

    app = FastAPI(title="Nexus Error Handler")
    tb = traceback.format_exc()

    @app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    async def catch_all_error(path_name: str):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Serverless Initialization Error",
                "detail": str(e),
                "traceback": tb.splitlines()[-15:]
            }
        )

import sys
import os
import traceback
from fastapi import FastAPI
from fastapi.responses import JSONResponse

os.environ["VERCEL"] = "1"

# Add root directory to sys.path so server and core modules import cleanly on Vercel
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

try:
    from server import app
except Exception as e:
    err_tb = traceback.format_exc()
    app = FastAPI()
    @app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    def error_debug(full_path: str):
        return JSONResponse(status_code=200, content={
            "import_failed": True,
            "error_type": type(e).__name__,
            "error_msg": str(e),
            "traceback": err_tb.splitlines()
        })

import sys
import os
import traceback
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/api/health")
def health():
    diag = {
        "status": "healthy",
        "python_version": sys.version,
        "platform": sys.platform,
        "cwd": os.getcwd(),
        "env_vercel": os.getenv("VERCEL"),
    }
    try:
        ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if ROOT_DIR not in sys.path:
            sys.path.insert(0, ROOT_DIR)
        import server
        diag["server_import"] = "SUCCESS"
    except Exception as e:
        diag["server_import"] = "FAILED"
        diag["error"] = str(e)
        diag["traceback"] = traceback.format_exc().splitlines()
    return diag

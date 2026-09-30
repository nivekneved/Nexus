from fastapi import FastAPI

app = FastAPI()

@app.get("/api/status")
@app.get("/status")
def status():
    return {"status": "ok", "message": "Direct minimal api/index works"}

@app.get("/api/health")
@app.get("/health")
def health():
    return {"status": "healthy"}

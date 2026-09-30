import re

try:
    with open('server.py', 'r', encoding='utf-8') as f:
        server_code = f.read()

    imports_to_add = """
from core.freelance_arbitrage import freelance_arbitrage
from core.android_compiler import android_compiler
from core.programmatic_seo import seo_engine
"""
    server_code = server_code.replace("from core.treasury_engine import treasury_engine", "from core.treasury_engine import treasury_engine" + imports_to_add)

    endpoints_to_add = """
# --- Revenue & Skills API Endpoints ---

@app.post("/api/skills/freelance-arbitrage")
def trigger_freelance_arbitrage():
    return freelance_arbitrage.scan_and_bid()

@app.post("/api/skills/android-compiler")
def trigger_android_compiler(data: dict):
    return android_compiler.build_white_label_apk(
        app_name=data.get("app_name", "Nexus App"),
        package_name=data.get("package_name", "com.nexus.app"),
        web_url=data.get("web_url", "https://nexus.mu")
    )

@app.post("/api/skills/programmatic-seo")
def trigger_seo_engine(data: dict):
    return seo_engine.generate_pages(
        niche=data.get("niche", "SaaS"),
        locations=data.get("locations", ["Port Louis", "Grand Baie"])
    )

@app.post("/api/skills/dunning")
def trigger_dunning_cycle():
    return treasury_engine.run_dunning_cycle()

"""
    # Insert right before the uvicorn.run call or at the bottom
    server_code = server_code.replace("if __name__ == \"__main__\":", endpoints_to_add + "\nif __name__ == \"__main__\":")

    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(server_code)

    print("Server successfully patched with 4 new Revenue Skill APIs!")
except Exception as e:
    print(f"Error: {e}")

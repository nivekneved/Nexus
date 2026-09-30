with open('server.py', 'r', encoding='utf-8') as f:
    code = f.read()

bad_imports = """
from core.freelance_arbitrage import freelance_arbitrage
from core.android_compiler import android_compiler
from core.programmatic_seo import seo_engine
"""
code = code.replace(bad_imports, "")

# Add them safely to the top instead
code = code.replace("from fastapi import FastAPI, HTTPException", "from fastapi import FastAPI, HTTPException" + bad_imports)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("Fixed indentation!")
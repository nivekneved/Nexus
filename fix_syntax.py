with open('server.py', 'r', encoding='utf-8') as f:
    code = f.read()

# I accidentally broke the import by injecting in the middle of a multi-line import
# "from fastapi import FastAPI, HTTPException" might have been part of "from fastapi import FastAPI, HTTPException, Request, Body"
code = code.replace("from fastapi import FastAPI, HTTPException\nfrom core.freelance_arbitrage import freelance_arbitrage\nfrom core.android_compiler import android_compiler\nfrom core.programmatic_seo import seo_engine\n", "from fastapi import FastAPI, HTTPException")

# Add it safely at the very top instead, after standard library imports
code = code.replace("import uvicorn", "import uvicorn\nfrom core.freelance_arbitrage import freelance_arbitrage\nfrom core.android_compiler import android_compiler\nfrom core.programmatic_seo import seo_engine\n")

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("Syntax fixed")
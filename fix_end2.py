with open('server.py', 'r', encoding='utf-8') as f:
    code = f.read()

bad_block = """if __name__ == "__main__":
    import uvicorn
from core.freelance_arbitrage import freelance_arbitrage
from core.android_compiler import android_compiler
from core.programmatic_seo import seo_engine

    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)"""

good_block = """if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)"""

code = code.replace(bad_block, good_block)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(code)

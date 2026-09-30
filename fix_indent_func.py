with open('server.py', 'r', encoding='utf-8') as f:
    code = f.read()

bad_snippet = """    from core.treasury_engine import treasury_engine
    import os

from core.freelance_arbitrage import freelance_arbitrage
from core.android_compiler import android_compiler
from core.programmatic_seo import seo_engine

    db_ok = os.path.exists("data/nexus_workforce.db")"""

good_snippet = """    from core.treasury_engine import treasury_engine
    import os

    db_ok = os.path.exists("data/nexus_workforce.db")"""

code = code.replace(bad_snippet, good_snippet)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("Indentation inside function fixed!")

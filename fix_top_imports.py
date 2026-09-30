with open('server.py', 'r', encoding='utf-8') as f:
    code = f.read()

new_imports = """
from core.freelance_arbitrage import freelance_arbitrage
from core.android_compiler import android_compiler
from core.programmatic_seo import seo_engine
"""

if "from core.freelance_arbitrage import freelance_arbitrage" not in code:
    code = code.replace("import os", "import os\n" + new_imports)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Top imports added successfully!")
else:
    print("Imports already present.")

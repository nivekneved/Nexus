import sys
import os

# Enforce Vercel runtime flag
os.environ["VERCEL"] = "1"

# Add root directory to sys.path so server and core modules import cleanly on Vercel
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from server import app

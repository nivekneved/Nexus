import sys
import os

# Add root directory to sys.path so server and core modules import cleanly on Vercel
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import app

"""
CompetitorPoacher: Database Connection & SQLite Setup
===================================================
"""

import os
import sqlite3
from typing import List, Dict, Any

DB_PATH = "competitor_poacher.db"

class PoacherDB:
    @staticmethod
    def initialize():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS poacher_cards (
                card_id TEXT PRIMARY KEY,
                competitor_name TEXT,
                target_domain TEXT,
                poaching_score REAL,
                status TEXT,
                payload TEXT
            )
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def save_card(card_id: str, competitor_name: str, target_domain: str, poaching_score: float, status: str, payload_json: str):
        PoacherDB.initialize()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO poacher_cards (card_id, competitor_name, target_domain, poaching_score, status, payload)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (card_id, competitor_name, target_domain, poaching_score, status, payload_json))
        conn.commit()
        conn.close()

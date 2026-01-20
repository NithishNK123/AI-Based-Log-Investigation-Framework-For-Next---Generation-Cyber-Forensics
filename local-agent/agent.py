"""
agent.py
--------
Local Log Collection Agent (FINAL VERSION)

Features:
- Collects system & application logs
- Registers system with server
- Stores logs offline in SQLite
- Syncs logs in batch
- Runs continuously
"""

import time
import yaml
import sqlite3
import platform
import requests
from datetime import datetime

from collectors.linux_logs import collect_linux_logs
from collectors.windows_logs import collect_windows_logs
from collectors.app_logs import collect_app_logs
from sender.sync_logs import sync_logs
from utils.system_id import get_system_id
from utils.logger import setup_logger

# ========================================================
# CONSTANTS
# ========================================================
DB_PATH = "storage/local_logs.db"
CONFIG_PATH = "config/agent_config.yaml"


# ========================================================
# DATABASE INITIALIZATION
# ========================================================
def init_database():
    """Initialize local SQLite DB"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            system_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            source TEXT NOT NULL,
            level TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def store_logs(logs):
    """Store logs locally"""
    if not logs:
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for log in logs:
        cursor.execute("""
            INSERT INTO logs (system_id, timestamp, source, level, message)
            VALUES (?, ?, ?, ?, ?)
        """, (
            log["system_id"],
            log["timestamp"],
            log["source"],
            log["level"],
            log["message"]
        ))

    conn.commit()
    conn.close()


# ========================================================
# CONFIG
# ========================================================
def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


# ========================================================
# SYSTEM REGISTRATION (FIXED)
# ========================================================
def register_system(server_url, api_key, system_id):
    """
    Register agent with central server
    """
    try:
        base_url = server_url.replace("/api/logs", "")

        requests.post(
            f"{base_url}/register/system",
            json={
                "system_id": system_id,
                "hostname": platform.node()
            },
            headers={"Authorization": api_key},
            timeout=5
        )
    except Exception:
        pass  # offline safe


# ========================================================
# MAIN AGENT LOOP
# ========================================================
def run_agent():
    logger = setup_logger()
    logger.info("Starting Local Log Collection Agent")

    config = load_config()
    init_database()

    system_id = get_system_id()
    logger.info(f"System ID initialized: {system_id}")

    server_url = config["server"]["url"]
    api_key = config["server"]["api_key"]
    sync_interval = config["agent"]["sync_interval_seconds"]
    max_lines = config["agent"]["max_lines_per_file"]

    # ✅ REGISTER SYSTEM ONCE (CORRECT URL)
    register_system(server_url, api_key, system_id)
    logger.info("System registered with server")

    while True:
        collected_logs = []

        try:
            os_type = platform.system()

            # ---------------- SYSTEM LOGS ----------------
            if os_type == "Linux":
                collected_logs.extend(
                    collect_linux_logs(system_id, max_lines)
                )
            elif os_type == "Windows":
                collected_logs.extend(
                    collect_windows_logs(system_id)
                )

            # ---------------- APP LOGS ----------------
            collected_logs.extend(
                collect_app_logs(system_id, max_lines)
            )

            # ---------------- STORE LOCAL ----------------
            if collected_logs:
                store_logs(collected_logs)
                logger.info(f"Collected {len(collected_logs)} logs")

            # ---------------- SYNC ----------------
            try:
                sync_logs(
                    server_url,   # already /api/logs
                    api_key
                )
                logger.info("Logs synced successfully")
            except Exception:
                logger.warning("Offline mode – logs stored locally")

        except Exception as e:
            logger.error(f"Agent error: {str(e)}")

        time.sleep(sync_interval)


# ========================================================
# ENTRY POINT
# ========================================================
if __name__ == "__main__":
    run_agent()

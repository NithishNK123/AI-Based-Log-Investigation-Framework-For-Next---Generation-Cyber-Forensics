"""
sync_logs.py
------------
Synchronizes locally stored logs with the central web server.

Fixes:
- No empty payload sent
- No duplicate sync
- No false error logs
"""

import sqlite3
import requests
import json

DB_PATH = "storage/local_logs.db"


def sync_logs(server_url, api_key):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT system_id, timestamp, source, level, message
        FROM logs
        ORDER BY id ASC
    """)
    rows = cursor.fetchall()

    # --------------------------------------------------
    # ✅ DO NOT CALL SERVER IF NO LOGS
    # --------------------------------------------------
    if not rows:
        conn.close()
        return

    payload = {
        "system_id": rows[0][0],
        "logs": []
    }

    for row in rows:
        payload["logs"].append({
            "timestamp": row[1],
            "source": row[2],
            "level": row[3],
            "message": row[4]
        })

    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            server_url,
            headers=headers,
            json=payload,
            timeout=10
        )

        if response.status_code == 201:
            # Delete logs only after success
            cursor.execute("DELETE FROM logs")
            conn.commit()
        else:
            print("❌ Sync failed:", response.text)

    except Exception as e:
        print("❌ Sync error:", e)

    conn.close()

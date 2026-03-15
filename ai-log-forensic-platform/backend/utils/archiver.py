import os
import json
import sqlite3
from datetime import datetime, timedelta
import gzip
import shutil

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "forensic.db")
ARCHIVE_DIR = os.path.join(os.path.dirname(__file__), "..", "archives")

def archive_old_logs(days_threshold=30):
    """
    Archives logs older than `days_threshold` to a compressed JSON file and 
    deletes them from the SQLite database to save space.
    """
    if not os.path.exists(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR)

    cutoff_date = datetime.utcnow() - timedelta(days=days_threshold)
    cutoff_str = cutoff_date.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[*] Starting log archiving for logs older than {cutoff_str}...")

    if not os.path.exists(DB_PATH):
        print("[-] Database not found. Aborting.")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Extract old logs
        cursor.execute("SELECT * FROM logs WHERE timestamp < ?", (cutoff_str,))
        old_logs = cursor.fetchall()

        if not old_logs:
            print("[✓] No logs older than the threshold found. Nothing to archive.")
            return

        archive_data = [dict(row) for row in old_logs]
        
        # Format filename
        timestamp_slug = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        archive_filename = f"log_archive_{timestamp_slug}.json"
        archive_filepath = os.path.join(ARCHIVE_DIR, archive_filename)

        # Write to JSON
        with open(archive_filepath, 'w') as f:
            json.dump(archive_data, f, indent=2)

        # Compress to gzip
        comp_filepath = f"{archive_filepath}.gz"
        with open(archive_filepath, 'rb') as f_in:
            with gzip.open(comp_filepath, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        # Remove uncompressed JSON
        os.remove(archive_filepath)
        print(f"[+] Archived {len(old_logs)} logs to {comp_filepath}")

        # Delete from database
        cursor.execute("DELETE FROM logs WHERE timestamp < ?", (cutoff_str,))
        conn.commit()
        print(f"[+] Cleaned up {len(old_logs)} logs from active database.")

    except Exception as e:
        print(f"[-] Error archiving logs: {str(e)}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    archive_old_logs(30)

"""
linux_logs.py
-------------
Collects Linux system and authentication logs for the local agent.

Target log files:
- /var/log/syslog
- /var/log/auth.log

The collector reads the latest N lines to avoid heavy processing.
"""

from utils.formatter import format_log
from datetime import datetime

# Default Linux log locations
LINUX_LOG_FILES = [
    "/var/log/syslog",
    "/var/log/auth.log"
]

def collect_linux_logs(system_id, max_lines=50):
    """
    Collect recent Linux system logs.

    Args:
        system_id (str): Unique system identifier
        max_lines (int): Number of recent log lines to read

    Returns:
        list: List of structured log dictionaries
    """
    logs = []

    for log_file in LINUX_LOG_FILES:
        try:
            with open(log_file, "r", errors="ignore") as file:
                lines = file.readlines()[-max_lines:]

                for line in lines:
                    line = line.strip()
                    if not line:
                        continue

                    logs.append(
                        format_log(
                            system_id=system_id,
                            source="linux",
                            message=line,
                            level="INFO"
                        )
                    )

        except FileNotFoundError:
            # Log file not present on system
            continue
        except PermissionError:
            # Insufficient permissions to read log file
            continue
        except Exception:
            # Catch-all to prevent agent crash
            continue

    return logs

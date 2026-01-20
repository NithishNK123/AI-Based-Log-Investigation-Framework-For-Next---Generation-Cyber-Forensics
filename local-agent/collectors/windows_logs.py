"""
windows_logs.py
----------------
Collects Windows Event Logs for the local agent.

Requirements:
- Windows OS
- pywin32 library (pip install pywin32)

If pywin32 is not available or OS is not Windows,
this module safely returns an empty log list.
"""

from datetime import datetime

def collect_windows_logs(system_id, max_events=20):
    logs = []

    try:
        import win32evtlog
        import win32evtlogutil

        server = "localhost"
        log_types = ["System", "Security", "Application"]

        for log_type in log_types:
            handle = win32evtlog.OpenEventLog(server, log_type)

            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
            events = win32evtlog.ReadEventLog(handle, flags, 0)

            for event in events[:max_events]:
                try:
                    message = win32evtlogutil.SafeFormatMessage(event, log_type)
                except Exception:
                    message = "Unable to parse event message"

                logs.append({
                    "system_id": system_id,
                    "timestamp": event.TimeGenerated.Format("%Y-%m-%d %H:%M:%S"),
                    "source": f"windows:{log_type}",
                    "level": "INFO",
                    "event_id": event.EventID & 0xFFFF,
                    "message": message.strip()
                })

    except ImportError:
        # pywin32 not installed
        pass
    except Exception:
        # Any Windows log access error
        pass

    return logs

"""
timeline.py
-----------
Builds a forensic timeline from collected logs.

Purpose:
- Reconstruct sequence of events
- Help investigators understand attack progression
- Support post-incident cyber forensics
"""

from datetime import datetime


def build_timeline(logs):
    """
    Build a chronological timeline of events from logs.

    Args:
        logs (list): List of log dictionaries with keys:
            - system_id
            - timestamp
            - source
            - level
            - message

    Returns:
        list: Ordered list of timeline events
    """

    timeline = []

    if not logs:
        return timeline

    for log in logs:
        try:
            # Parse timestamp (ISO format expected)
            timestamp = log.get("timestamp")
            if isinstance(timestamp, str):
                event_time = datetime.fromisoformat(
                    timestamp.replace("Z", "")
                )
            else:
                continue

            timeline.append({
                "system_id": log.get("system_id"),
                "time": event_time,
                "source": log.get("source"),
                "level": log.get("level"),
                "message": log.get("message")
            })

        except Exception:
            # Skip malformed log entries
            continue

    # Sort events by time
    timeline.sort(key=lambda x: x["time"])

    return timeline

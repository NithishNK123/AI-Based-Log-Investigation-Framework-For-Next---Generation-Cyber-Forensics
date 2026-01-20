"""
formatter.py
------------
Formats raw log messages into a structured JSON-compatible format
for storage, encryption, and transmission.
"""

from datetime import datetime


def format_log(system_id, source, message, level="INFO"):
    """
    Convert a raw log message into structured format.

    Args:
        system_id (str): Unique system identifier
        source (str): Log source (linux / windows / application)
        message (str): Raw log message
        level (str): Log severity level

    Returns:
        dict: Structured log dictionary
    """

    return {
        "system_id": system_id,
        "timestamp": datetime.utcnow().isoformat(),
        "source": source,
        "level": level,
        "message": message
    }

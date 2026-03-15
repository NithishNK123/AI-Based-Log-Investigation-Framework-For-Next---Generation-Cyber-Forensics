"""
run_logai.py
------------
Triggers AI-based log analysis using LogAI.

Responsibilities:
- Fetch logs from database
- Prepare logs for analysis
- Call LogAI-based anomaly detection
- Generate alerts for suspicious activity
"""

from database.models import Log, Alert
from database.db import db
from ai_engine.anomaly_detection import detect_anomaly
from datetime import datetime


def run_logai_analysis(limit=500):
    """
    Run AI analysis on recently collected logs.

    Args:
        limit (int): Number of recent logs to analyze
    """

    # Fetch recent logs
    logs = Log.query.order_by(Log.id.desc()).limit(limit).all()

    if not logs:
        print("[LogAI] No logs available for analysis")
        return

    print(f"[LogAI] Running analysis on {len(logs)} logs")

    # Analyze each log
    for log in logs:
        try:
            is_anomaly = detect_anomaly({
                "system_id": log.system_id,
                "timestamp": log.timestamp,
                "source": log.source,
                "level": log.level,
                "message": log.message
            })

            if is_anomaly:
                alert = Alert()
                alert.system_id = log.system_id
                alert.description = f"Suspicious activity detected: {log.message}"
                alert.severity = "High"
                alert.alert_type = "anomaly"

                db.session.add(alert)

        except Exception as e:
            print(f"[LogAI] Error analyzing log {log.id}: {e}")

    db.session.commit()
    print("[LogAI] Analysis completed")

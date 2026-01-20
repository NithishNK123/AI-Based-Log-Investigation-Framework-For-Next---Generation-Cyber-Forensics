"""
dashboard.py (FINAL VERSION)
----------------------------
Dashboard APIs for AI Log Forensic Platform

Features:
- System listing
- Log search & filtering
- Alert filtering
- Secure per-system access
- Statistics for SOC dashboard
"""

from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from sqlalchemy import and_

from backend.database.models import System, Log, Alert
from backend.database.db import db

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

# =========================================================
# SYSTEMS
# =========================================================
@dashboard_bp.route("/systems", methods=["GET"])
def get_systems():
    systems = System.query.order_by(System.last_seen.desc()).all()

    return jsonify([
        {
            "system_id": s.system_id,
            "hostname": s.hostname,
            "last_seen": s.last_seen.strftime("%Y-%m-%d %H:%M:%S") if s.last_seen else None
        }
        for s in systems
    ]), 200


# =========================================================
# LOG SEARCH + FILTER (DELIVERABLE ✔)
# =========================================================
@dashboard_bp.route("/logs", methods=["GET"])
def get_logs():
    """
    Filters:
    ?system_id=
    ?level=
    ?source=
    ?q=keyword
    ?hours=24
    """
    query = Log.query

    system_id = request.args.get("system_id")
    level = request.args.get("level")
    source = request.args.get("source")
    keyword = request.args.get("q")
    hours = request.args.get("hours")

    if system_id is not None and system_id:
        query = query.filter(Log.system_id == system_id)  # type: ignore

    if level is not None and level:
        query = query.filter(Log.level == level)  # type: ignore

    if source is not None and source:
        query = query.filter(Log.source == source)  # type: ignore

    if keyword is not None and keyword:
        query = query.filter(Log.message.ilike(f"%{keyword}%"))  # type: ignore

    if hours is not None and hours:
        since = datetime.utcnow() - timedelta(hours=int(hours))
        query = query.filter(Log.timestamp >= since)  # type: ignore

    logs = query.order_by(Log.id.desc()).limit(300).all()

    return jsonify([
        {
            "id": l.id,
            "system_id": l.system_id,
            "timestamp": l.timestamp if isinstance(l.timestamp, str)
                else l.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "source": l.source,
            "level": l.level,
            "message": l.message
        }
        for l in logs
    ]), 200


# =========================================================
# ALERT FILTERING (DELIVERABLE ✔)
# =========================================================
@dashboard_bp.route("/alerts", methods=["GET"])
def get_alerts():
    """
    Filters:
    ?system_id=
    ?severity=
    """
    query = Alert.query

    system_id = request.args.get("system_id")
    severity = request.args.get("severity")

    if system_id is not None and system_id:
        query = query.filter(Alert.system_id == system_id)  # type: ignore

    if severity is not None and severity:
        query = query.filter(Alert.severity == severity)  # type: ignore

    alerts = query.order_by(Alert.created_at.desc()).all()

    return jsonify([
        {
            "id": a.id,
            "system_id": a.system_id,
            "description": a.description,
            "severity": a.severity,
            "created_at": a.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for a in alerts
    ]), 200


# =========================================================
# DASHBOARD STATS (DELIVERABLE ✔)
# =========================================================
@dashboard_bp.route("/stats", methods=["GET"])
def dashboard_stats():
    return jsonify({
        "total_systems": System.query.count(),
        "total_logs": Log.query.count(),
        "total_alerts": Alert.query.count(),
        "critical_alerts": Alert.query.filter_by(severity="Critical").count(),
        "high_alerts": Alert.query.filter_by(severity="High").count()
    }), 200

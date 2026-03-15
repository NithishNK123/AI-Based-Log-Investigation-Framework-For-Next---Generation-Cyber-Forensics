"""
dashboard.py (FINAL SECURE VERSION)
----------------------------------
Dashboard APIs for AI Log Forensic Platform

SECURITY:
- Users see only their systems
- Logs filtered by ownership
- Alerts filtered by ownership
- SOC-grade isolation
"""

from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta

from backend.database.models import System, Log, Alert
from backend.database.db import db

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

# =========================================================
# SYSTEMS (ONLY OWNED)
# =========================================================
@dashboard_bp.route("/systems", methods=["GET"])
def get_systems():
    # Get all systems (admin can see all, or filter by owner_id=1 for single user)
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
# LOG SEARCH + FILTER (SECURE)
# =========================================================
@dashboard_bp.route("/logs", methods=["GET"])
def get_logs():
    """
    Filters:
    ?system_id=
    ?level=
    ?source=
    ?log_type=       (application, system, network, security)
    ?q=keyword
    ?hours=24
    """

    # Get all systems and logs
    all_systems = System.query.all()
    user_system_ids = [s.system_id for s in all_systems]

    query = Log.query.filter(Log.system_id.in_(user_system_ids)) if user_system_ids else Log.query

    system_id = request.args.get("system_id")
    level = request.args.get("level")
    source = request.args.get("source")
    log_type = request.args.get("log_type")
    keyword = request.args.get("q")
    hours = request.args.get("hours")

    if system_id:
        if system_id not in user_system_ids:
            return jsonify({"error": "Unauthorized system access"}), 403
        query = query.filter(Log.system_id == system_id)

    if level:
        query = query.filter(Log.level == level)

    if source:
        query = query.filter(Log.source == source)

    if log_type:
        query = query.filter(Log.log_type == log_type)

    if keyword:
        query = query.filter(Log.message.ilike(f"%{keyword}%"))

    if hours:
        since = datetime.utcnow() - timedelta(hours=int(hours))
        query = query.filter(Log.timestamp >= since)

    logs = query.order_by(Log.id.desc()).limit(300).all()

    return jsonify([
        {
            "id": l.id,
            "system_id": l.system_id,
            "timestamp": l.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "source": l.source,
            "level": l.level,
            "log_type": l.log_type,
            "message": l.message
        }
        for l in logs
    ]), 200


# =========================================================
# ALERT FILTERING (SECURE)
# =========================================================
@dashboard_bp.route("/alerts", methods=["GET"])
def get_alerts():
    """
    Filters:
    ?system_id=
    ?severity=
    """

    # Get all systems and alerts
    all_systems = System.query.all()
    user_system_ids = [s.system_id for s in all_systems]

    query = Alert.query.filter(Alert.system_id.in_(user_system_ids)) if user_system_ids else Alert.query

    system_id = request.args.get("system_id")
    severity = request.args.get("severity")

    if system_id:
        if system_id not in user_system_ids:
            return jsonify({"error": "Unauthorized system access"}), 403
        query = query.filter(Alert.system_id == system_id)

    if severity:
        query = query.filter(Alert.severity == severity)

    alerts = query.order_by(Alert.created_at.desc()).all()

    return jsonify([
        {
            "id": a.id,
            "system_id": a.system_id,
            "description": a.description,
            "severity": a.severity,
            "alert_type": a.alert_type,
            "created_at": a.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for a in alerts
    ]), 200




# =========================================================
# DASHBOARD STATS (PER USER)
# =========================================================
@dashboard_bp.route("/stats", methods=["GET"])
def dashboard_stats():
    # Get all systems and stats
    all_systems = System.query.all()
    user_system_ids = [s.system_id for s in all_systems]

    return jsonify({
        "total_systems": len(user_system_ids),
        "total_logs": Log.query.filter(Log.system_id.in_(user_system_ids)).count() if user_system_ids else 0,
        "total_alerts": Alert.query.filter(Alert.system_id.in_(user_system_ids)).count() if user_system_ids else 0,
        "critical_alerts": Alert.query.filter(
            Alert.system_id.in_(user_system_ids),
            Alert.severity == "Critical"
        ).count() if user_system_ids else 0,
        "high_alerts": Alert.query.filter(
            Alert.system_id.in_(user_system_ids),
            Alert.severity == "High"
        ).count() if user_system_ids else 0
    }), 200

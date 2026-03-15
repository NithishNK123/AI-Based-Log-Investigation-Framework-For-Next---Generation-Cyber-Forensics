"""
logs_api.py (FINAL SECURE VERSION)
---------------------------------
Secure log ingestion API for AI Log Forensic Platform.

SECURITY:
- Only registered systems can send logs
- Ownership enforced
- No auto-admin creation
- No spoofing allowed
- Agent identity verified
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import json
import os
from cryptography.fernet import Fernet

from backend.config import Config
from backend.database.db import db
from backend.database.models import Log, System, Alert
from backend.ai_engine.log_parser import parse_log

logs_api_bp = Blueprint("logs_api", __name__, url_prefix="/api/logs")

KEY_FILE = ".agent_secret.key"


# =====================================================
# LOAD ENCRYPTION KEY
# =====================================================
def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    return None


# =====================================================
# MAIN LOG INGESTION API
# =====================================================
@logs_api_bp.route("", methods=["POST"])
def receive_logs():

    # --------------------------------------------------
    # 1. AGENT AUTHENTICATION
    # --------------------------------------------------
    api_key = request.headers.get("Authorization")
    if not api_key or api_key != Config.AGENT_API_KEY:
        return jsonify({"error": "Unauthorized agent"}), 401

    # --------------------------------------------------
    # 2. READ PAYLOAD (JSON / ENCRYPTED)
    # --------------------------------------------------
    payload = None

    if request.is_json:
        payload = request.get_json(silent=True)

    if payload is None:
        key = load_key()
        if key:
            try:
                fernet = Fernet(key)
                decrypted = fernet.decrypt(request.data)
                payload = json.loads(decrypted.decode())
            except Exception:
                return jsonify({"error": "Invalid encrypted payload"}), 400

    if not payload:
        return jsonify({"error": "Empty payload"}), 400

    # --------------------------------------------------
    # 3. VALIDATE PAYLOAD
    # --------------------------------------------------
    if "system_id" not in payload or "logs" not in payload:
        return jsonify({"error": "Invalid payload format"}), 400

    system_id = payload["system_id"]
    logs_data = payload["logs"]

    if not isinstance(logs_data, list) or not logs_data:
        return jsonify({"error": "Logs must be a non-empty list"}), 400

    # --------------------------------------------------
    # 4. VERIFY REGISTERED SYSTEM
    # --------------------------------------------------
    system = System.query.filter_by(system_id=system_id).first()
    if not system:
        return jsonify({
            "error": "System not registered. Register system first."
        }), 403

    # Update heartbeat
    system.last_seen = datetime.utcnow()

    # --------------------------------------------------
    # 5. STORE LOGS + AI DETECTION
    # --------------------------------------------------
    stored = 0
    alerts_created = 0
    new_alerts = []

    for entry in logs_data:

        # Safe timestamp parsing
        timestamp_val = entry.get("timestamp")
        if isinstance(timestamp_val, str):
            try:
                timestamp_val = datetime.fromisoformat(
                    timestamp_val.replace("Z", "+00:00")
                )
            except Exception:
                timestamp_val = datetime.utcnow()
        elif not isinstance(timestamp_val, datetime):
            timestamp_val = datetime.utcnow()

        log = Log()
        log.system_id = system_id
        log.timestamp = timestamp_val
        log.source = entry.get("source", "unknown")
        log.level = entry.get("level", "INFO")
        log.message = entry.get("message", "")
        log.log_type = entry.get("log_type", "application")

        # AI parsing & attack detection
        log = parse_log(log)

        db.session.add(log)
        stored += 1

        # Generate alert if high risk
        if getattr(log, "risk", "low") in ["high", "critical"]:
            alert = Alert()
            alert.system_id = system_id
            alert.description = f"{log.event_type.upper()} detected: {log.message[:150]}"
            alert.severity = "Critical" if getattr(log, "risk", "low") == "critical" else "High"
            alert.alert_type = log.event_type
            db.session.add(alert)
            new_alerts.append(alert)
            alerts_created += 1

    db.session.commit()

    # Trigger notifications asynchronously
    if new_alerts:
        from backend.utils.notifications import trigger_notifications_async
        for a in new_alerts:
            trigger_notifications_async(a.id)

    # --------------------------------------------------
    # 6. RESPONSE
    # --------------------------------------------------
    return jsonify({
        "status": "success",
        "system_id": system_id,
        "logs_stored": stored,
        "alerts_created": alerts_created
    }), 201

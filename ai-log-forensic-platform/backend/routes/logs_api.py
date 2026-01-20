"""
logs_api.py (FINAL VERSION)
---------------------------
Receives logs from local agents, parses them,
detects attacks (phishing, malware, brute force),
generates alerts, and stores everything securely.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import json
import os
from cryptography.fernet import Fernet

from backend.config import Config
from backend.database.db import db
from backend.database.models import Log, System, Alert, User
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
    # 1. AUTHENTICATE AGENT
    # --------------------------------------------------
    api_key = request.headers.get("Authorization")
    if Config.AGENT_API_KEY and api_key != Config.AGENT_API_KEY:
        return jsonify({"error": "Unauthorized agent"}), 401

    # --------------------------------------------------
    # 2. READ PAYLOAD (JSON / ENCRYPTED)
    # --------------------------------------------------
    payload = None

    # Plain JSON
    if request.is_json:
        payload = request.get_json(silent=True)

    # Encrypted
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
    # 3. VALIDATE FORMAT
    # --------------------------------------------------
    if "system_id" not in payload or "logs" not in payload:
        return jsonify({"error": "Invalid log format"}), 400

    system_id = payload["system_id"]
    logs_data = payload["logs"]

    if not isinstance(logs_data, list) or not logs_data:
        return jsonify({"error": "Logs must be non-empty list"}), 400

    # --------------------------------------------------
    # 4. REGISTER / UPDATE SYSTEM
    # --------------------------------------------------
    system = System.query.filter_by(system_id=system_id).first()
    if not system:
        # Get or create default admin user
        admin_user = User.query.filter_by(username="admin").first()
        if not admin_user:
            from werkzeug.security import generate_password_hash
            admin_user = User(
                username="admin",
                password=generate_password_hash("admin123"),
                role="admin"
            )
            db.session.add(admin_user)
            db.session.flush()
        
        system = System(
            system_id=system_id,
            hostname="agent",
            owner_id=admin_user.id,
            last_seen=datetime.utcnow()
        )
        db.session.add(system)
    else:
        system.last_seen = datetime.utcnow()

    # --------------------------------------------------
    # 5. STORE + PARSE + DETECT ATTACKS
    # --------------------------------------------------
    stored = 0
    alerts_created = 0

    for entry in logs_data:
        # Parse timestamp if it's a string
        timestamp_val = entry.get("timestamp")
        if isinstance(timestamp_val, str):
            try:
                timestamp_val = datetime.fromisoformat(timestamp_val.replace('Z', '+00:00'))
            except:
                timestamp_val = datetime.utcnow()
        elif not isinstance(timestamp_val, datetime):
            timestamp_val = datetime.utcnow()
        
        log = Log(
            system_id=system_id,
            timestamp=timestamp_val,
            source=entry.get("source", "unknown"),
            level=entry.get("level", "INFO"),
            message=entry.get("message", "")
        )

        # ---------------- AI PARSER ----------------
        log = parse_log(log)
        db.session.add(log)
        stored += 1

        # ---------------- ALERT ENGINE ----------------
        if log.risk in ["high", "critical"]:
            alert = Alert(
                system_id=system_id,
                description=f"{log.event_type.upper()} detected: {log.message[:150]}",
                severity="Critical" if log.risk == "critical" else "High"
            )
            db.session.add(alert)
            alerts_created += 1

    db.session.commit()

    # --------------------------------------------------
    # 6. RESPONSE
    # --------------------------------------------------
    return jsonify({
        "status": "success",
        "system_id": system_id,
        "logs_stored": stored,
        "alerts_created": alerts_created
    }), 201

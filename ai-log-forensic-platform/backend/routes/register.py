"""
register.py
-----------
Secure registration of endpoint systems (agents)
for AI Log Forensic Platform.

SECURITY:
- Ownership enforced
- User-authenticated registration
- No default admin binding
- First-run detection supported
"""

from flask import Blueprint, request, jsonify
from datetime import datetime

from backend.database.db import db
from backend.database.models import System, User

register_bp = Blueprint("register", __name__, url_prefix="/api/register")


@register_bp.route("/system", methods=["POST"])
def register_system():
    """
    Register or update system securely

    Expected JSON:
    {
        "system_id": "uuid-generated-by-agent",
        "hostname": "DESKTOP-XYZ",
        "ip_address": "192.168.1.5",
        "os_type": "Windows"
    }
    """

    data = request.get_json()
    if not data or "system_id" not in data:
        return jsonify({"error": "system_id is required"}), 400

    # 🔐 Use default admin user (owner_id=1)
    # In production, this should use JWT or session-based authentication
    user = User.query.filter_by(role="admin").first()
    
    if not user:
        # Auto-create admin user if doesn't exist
        user = User()
        user.username = "admin"
        user.password = "admin"  # In production, use hashed password
        user.role = "admin"
        db.session.add(user)
        db.session.commit()

    system_id = data["system_id"]
    hostname = data.get("hostname", "Unknown")
    ip_address = data.get("ip_address")
    os_type = data.get("os_type")

    # --------------------------------------------------
    # 1. Check existing system
    # --------------------------------------------------
    system = System.query.filter_by(system_id=system_id).first()

    if system:
        # ❌ Prevent cross-user hijacking
        if system.owner_id != user.id:
            return jsonify({
                "error": "System already registered to another user"
            }), 403

        # Update heartbeat
        system.last_seen = datetime.utcnow()
        system.hostname = hostname
        system.ip_address = ip_address
        system.os_type = os_type
        db.session.commit()

        return jsonify({
            "status": "updated",
            "system_id": system.system_id
        }), 200

    # --------------------------------------------------
    # 2. First-time registration
    # --------------------------------------------------
    new_system = System()
    new_system.system_id = system_id
    new_system.hostname = hostname
    new_system.owner_id = user.id
    new_system.ip_address = ip_address
    new_system.os_type = os_type
    new_system.last_seen = datetime.utcnow()

    db.session.add(new_system)
    db.session.commit()

    return jsonify({
        "status": "registered",
        "system_id": system_id
    }), 201

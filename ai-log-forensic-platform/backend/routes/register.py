"""
register.py
-----------
Handles registration of endpoint systems (local agents)
with the central AI Log Forensic Platform.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime

from backend.database.db import db
from backend.database.models import System, User

# Blueprint for system registration
register_bp = Blueprint("register", __name__, url_prefix="/api/register")


@register_bp.route("/system", methods=["POST"])
def register_system():
    """
    Register a new system or update an existing system.

    Expected JSON:
    {
        "system_id": "<unique-system-id>",
        "hostname": "<system-hostname>",
        "ip_address": "<optional-ip>",
        "os_type": "<optional-os>"
    }
    """

    data = request.get_json()

    if not data or "system_id" not in data:
        return jsonify({"error": "system_id is required"}), 400

    system_id = data["system_id"]
    hostname = data.get("hostname", "Unknown")
    ip_address = data.get("ip_address")
    os_type = data.get("os_type")

    # Check if system already exists
    system = System.query.filter_by(system_id=system_id).first()

    if system:
        # Update last seen timestamp
        system.last_seen = datetime.utcnow()
        system.hostname = hostname
        system.ip_address = ip_address
        system.os_type = os_type
        db.session.commit()

        return jsonify({
            "status": "updated",
            "system_id": system_id
        }), 200

    # Register new system
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
    
    new_system = System(
        system_id=system_id,
        hostname=hostname,
        owner_id=admin_user.id,
        ip_address=ip_address,
        os_type=os_type
    )

    db.session.add(new_system)
    db.session.commit()

    return jsonify({
        "status": "registered",
        "system_id": system_id
    }), 201

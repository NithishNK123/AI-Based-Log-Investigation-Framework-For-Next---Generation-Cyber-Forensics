"""
settings.py
-----------
API routes for user Settings (Notification Rules, etc).
"""

from flask import Blueprint, jsonify, request
from backend.database.models import NotificationRule, User
from backend.database.db import db

settings_bp = Blueprint("settings", __name__, url_prefix="/api/settings")

@settings_bp.route("/notifications", methods=["GET"])
def get_rules():
    """Fetch all notification rules."""
    rules = NotificationRule.query.all()
    
    return jsonify([{
        "id": r.id,
        "channel": r.channel,
        "destination": r.destination,
        "target_severity": r.target_severity,
        "is_active": r.is_active,
        "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S")
    } for r in rules]), 200

@settings_bp.route("/notifications", methods=["POST"])
def create_rule():
    """Create a new notification rule."""
    data = request.json
    
    # In a real app, user_id comes from session. Hardcoding fallback to first user for demo.
    user_id = data.get("user_id")
    if not user_id:
        u = User.query.first()
        if not u:
            return jsonify({"error": "No user available"}), 400
        user_id = u.id
        
    rule = NotificationRule(
        user_id=user_id,
        channel=data.get("channel", "Email"),
        destination=data.get("destination"),
        target_severity=data.get("target_severity", "ALL"),
        is_active=True
    )
    
    db.session.add(rule)
    db.session.commit()
    
    return jsonify({"message": "Rule created", "id": rule.id}), 201

@settings_bp.route("/notifications/<int:rule_id>", methods=["DELETE"])
def delete_rule(rule_id):
    """Delete a rule."""
    rule = NotificationRule.query.get_or_404(rule_id)
    db.session.delete(rule)
    db.session.commit()
    return jsonify({"message": "Rule deleted"}), 200

@settings_bp.route("/notifications/<int:rule_id>/toggle", methods=["PUT"])
def toggle_rule(rule_id):
    """Toggle the active state of a rule."""
    rule = NotificationRule.query.get_or_404(rule_id)
    rule.is_active = not rule.is_active
    db.session.commit()
    return jsonify({"message": "Status toggled", "is_active": rule.is_active}), 200

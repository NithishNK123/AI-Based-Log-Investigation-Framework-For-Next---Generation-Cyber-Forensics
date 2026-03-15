"""
incidents.py
------------
API routes for Incident Case Management.
"""

from flask import Blueprint, jsonify, request
from datetime import datetime

from backend.database.models import IncidentTicket, TicketComment, Alert, User
from backend.database.db import db

incidents_bp = Blueprint("incidents", __name__, url_prefix="/api/incidents")

@incidents_bp.route("", methods=["GET"])
def get_incidents():
    """Get all incident tickets."""
    status_filter = request.args.get("status")
    
    query = IncidentTicket.query
    if status_filter:
        query = query.filter_by(status=status_filter)
        
    tickets = query.order_by(IncidentTicket.updated_at.desc()).all()
    
    result = []
    for t in tickets:
        alert = Alert.query.get(t.alert_id)
        system_id = alert.system_id if alert else "Unknown"
        severity = alert.severity if alert else "Unknown"
        
        assigned_user = User.query.get(t.assigned_to) if t.assigned_to else None
        assignee_name = assigned_user.username if assigned_user else "Unassigned"
        
        result.append({
            "id": t.id,
            "title": t.title,
            "status": t.status,
            "system_id": system_id,
            "severity": severity,
            "assigned_to": assignee_name,
            "created_at": t.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": t.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        })
        
    return jsonify(result), 200

@incidents_bp.route("", methods=["POST"])
def create_incident():
    """Create a new incident ticket from an alert."""
    data = request.json
    alert_id = data.get("alert_id")
    title = data.get("title")
    description = data.get("description", "")
    
    if not alert_id or not title:
        return jsonify({"error": "alert_id and title are required"}), 400
        
    # Check if ticket already exists for this alert
    existing = IncidentTicket.query.filter_by(alert_id=alert_id).first()
    if existing:
        return jsonify({"error": "A ticket already exists for this alert", "ticket_id": existing.id}), 400
        
    ticket = IncidentTicket(
        title=title,
        description=description,
        alert_id=alert_id,
        status="Open"
    )
    
    db.session.add(ticket)
    db.session.commit()
    
    return jsonify({"message": "Incident ticket created successfully", "ticket_id": ticket.id}), 201

@incidents_bp.route("/<int:ticket_id>", methods=["GET"])
def get_incident(ticket_id):
    """Get details of a specific ticket, including comments."""
    t = IncidentTicket.query.get_or_404(ticket_id)
    alert = Alert.query.get(t.alert_id)
    
    assigned_user = User.query.get(t.assigned_to) if t.assigned_to else None
    
    comments = []
    for c in t.comments.order_by(TicketComment.created_at.asc()):
        author = User.query.get(c.user_id)
        comments.append({
            "id": c.id,
            "author": author.username if author else "Unknown",
            "text": c.comment_text,
            "created_at": c.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
        
    return jsonify({
        "id": t.id,
        "title": t.title,
        "description": t.description,
        "status": t.status,
        "alert_id": t.alert_id,
        "system_id": alert.system_id if alert else "Unknown",
        "severity": alert.severity if alert else "Unknown",
        "alert_description": alert.description if alert else "",
        "mitre_tactic": alert.mitre_tactic if alert else None,
        "mitre_technique": alert.mitre_technique if alert else None,
        "assigned_to": assigned_user.username if assigned_user else None,
        "assigned_to_id": t.assigned_to,
        "created_at": t.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": t.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        "comments": comments
    }), 200

@incidents_bp.route("/<int:ticket_id>", methods=["PUT"])
def update_incident(ticket_id):
    """Update ticket status or assignee."""
    ticket = IncidentTicket.query.get_or_404(ticket_id)
    data = request.json
    
    if "status" in data:
        ticket.status = data["status"]
    if "assigned_to" in data:
        # Expecting a user ID
        ticket.assigned_to = data["assigned_to"]
        
    db.session.commit()
    return jsonify({"message": "Ticket updated successfully"}), 200

@incidents_bp.route("/<int:ticket_id>/comments", methods=["POST"])
def add_comment(ticket_id):
    """Add a comment to a ticket."""
    ticket = IncidentTicket.query.get_or_404(ticket_id)
    data = request.json
    
    text = data.get("text")
    user_id = data.get("user_id") # Normally from session, accepting from payload for now
    
    if not text or not user_id:
        return jsonify({"error": "text and user_id are required"}), 400
        
    # verify user exists
    user = User.query.get(user_id)
    if not user:
        # Fallback to demo user if not found (for easy testing without full auth setup)
        user = User.query.first()
        if not user:
            return jsonify({"error": "No valid user found to author comment"}), 400
        user_id = user.id
        
    comment = TicketComment(
        ticket_id=ticket_id,
        user_id=user_id,
        comment_text=text
    )
    
    db.session.add(comment)
    
    # Update ticket's updated_at timestamp
    ticket.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({"message": "Comment added", "comment_id": comment.id}), 201

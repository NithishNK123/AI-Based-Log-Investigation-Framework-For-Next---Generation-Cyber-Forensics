"""
models.py
---------
Database models for the AI Log Forensic Platform.

SECURITY GOALS:
- Enforce ownership of systems
- Prevent cross-user log access
- Enable forensic integrity
- Support AI correlation & detection

TABLES:
- User
- System
- Log
- Alert
"""

from datetime import datetime
from backend.database.db import db


# ==========================================================
# USER MODEL
# ==========================================================
class User(db.Model):
    """
    Platform users (SOC analysts / admins)
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="analyst", index=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One user -> many systems
    systems = db.relationship(
        "System",
        backref="owner",
        lazy="dynamic",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"


# ==========================================================
# SYSTEM MODEL
# ==========================================================
class System(db.Model):
    """
    Registered endpoint systems (agents)
    Each system belongs to ONE user (ownership enforced)
    """
    __tablename__ = "systems"

    id = db.Column(db.Integer, primary_key=True)

    # Agent identity
    system_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    hostname = db.Column(db.String(100), nullable=False)

    ip_address = db.Column(db.String(50))
    os_type = db.Column(db.String(50))

    # 🔐 Owner binding (CRITICAL SECURITY FIELD)
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    last_seen = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Relationships
    logs = db.relationship(
        "Log",
        backref="system",
        lazy="dynamic",
        cascade="all, delete-orphan"
    )

    alerts = db.relationship(
        "Alert",
        backref="system",
        lazy="dynamic",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<System {self.system_id} | {self.hostname}>"


# ==========================================================
# LOG MODEL
# ==========================================================
class Log(db.Model):
    """
    Logs collected from agents
    Used by AI engine for detection & correlation
    """
    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key=True)

    # FK to system
    system_id = db.Column(
        db.String(100),
        db.ForeignKey("systems.system_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    source = db.Column(db.String(50), nullable=False, index=True)
    level = db.Column(db.String(20), nullable=False, index=True)
    message = db.Column(db.Text, nullable=False)

    # Log type categorization (application, system, network, security)
    log_type = db.Column(db.String(50), default="application", index=True)

    # AI enrichment
    event_type = db.Column(db.String(50), default="normal", index=True)
    risk = db.Column(db.String(20), default="low", index=True)

    def __repr__(self):
        return f"<Log {self.system_id} | {self.level} | {self.event_type}>"


# ==========================================================
# ALERT MODEL
# ==========================================================
class Alert(db.Model):
    """
    AI-generated forensic alerts

    Types:
    - phishing
    - malware
    - brute_force
    - port_scan
    - anomaly
    - policy_violation
    """
    __tablename__ = "alerts"

    id = db.Column(db.Integer, primary_key=True)

    system_id = db.Column(
        db.String(100),
        db.ForeignKey("systems.system_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    description = db.Column(db.Text, nullable=False)

    severity = db.Column(db.String(20), default="Medium", index=True)
    alert_type = db.Column(db.String(50), default="generic", index=True)
    
    # MITRE ATT&CK Mapping
    mitre_tactic = db.Column(db.String(100), nullable=True)
    mitre_technique = db.Column(db.String(100), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Incident Ticket Relationship
    ticket = db.relationship("IncidentTicket", backref="alert", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Alert {self.system_id} | {self.alert_type} | {self.severity}>"


# ==========================================================
# INCIDENT TICKETING (CASE MANAGEMENT)
# ==========================================================
class IncidentTicket(db.Model):
    """
    Case management for tracking security investigations.
    """
    __tablename__ = "incident_tickets"

    id = db.Column(db.Integer, primary_key=True)
    
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Status: Open, Investigating, Remediated, Closed
    status = db.Column(db.String(50), default="Open", index=True)
    
    # Linked Alert
    alert_id = db.Column(db.Integer, db.ForeignKey("alerts.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Assigned User Validator (Optional mapping)
    assigned_to = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Comments
    comments = db.relationship("TicketComment", backref="ticket", lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<IncidentTicket {self.id} | Status: {self.status}>"


class TicketComment(db.Model):
    """
    Comments / notes for an Incident Ticket.
    """
    __tablename__ = "ticket_comments"

    id = db.Column(db.Integer, primary_key=True)
    
    ticket_id = db.Column(db.Integer, db.ForeignKey("incident_tickets.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    comment_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Associated author relationship
    author = db.relationship("User", backref="comments")

    def __repr__(self):
        return f"<TicketComment {self.id} | Ticket {self.ticket_id}>"

# ==========================================================
# NOTIFICATION RULES
# ==========================================================
class NotificationRule(db.Model):
    """
    User-defined rules for alerting via external channels (Slack, Email).
    """
    __tablename__ = "notification_rules"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    channel = db.Column(db.String(50), nullable=False) # e.g. 'Email', 'Slack'
    destination = db.Column(db.String(255), nullable=False)
    target_severity = db.Column(db.String(50), nullable=True) # e.g. 'Critical', 'High'
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<NotificationRule {self.channel} -> {self.destination}>"

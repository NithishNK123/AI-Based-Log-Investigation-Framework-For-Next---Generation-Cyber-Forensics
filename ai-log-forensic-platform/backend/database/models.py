"""
models.py
---------
Database models for the AI Log Forensic Platform.

Defines tables:
- User      : Platform users (Admin / Analyst)
- System    : Registered endpoint systems (ownership enforced)
- Log       : Collected logs from agents
- Alert     : AI-generated forensic alerts (phishing, malware, anomalies)
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

    # One user → many systems
    systems = db.relationship(
        "System",
        backref="owner",
        lazy="dynamic",
        cascade="all, delete-orphan"
    )

    def __init__(self, username, password, role="analyst"):
        self.username = username
        self.password = password
        self.role = role

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"


# ==========================================================
# SYSTEM MODEL
# ==========================================================
class System(db.Model):
    """
    Registered endpoint systems
    Each system belongs to ONE user (ownership enforced)
    """
    __tablename__ = "systems"

    id = db.Column(db.Integer, primary_key=True)

    system_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    hostname = db.Column(db.String(100), nullable=False)

    ip_address = db.Column(db.String(50))
    os_type = db.Column(db.String(50))

    # 🔐 Ownership enforcement
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    last_seen = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # One system → many logs & alerts
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

    def __init__(self, system_id, hostname, owner_id, ip_address=None, os_type=None, last_seen=None):
        self.system_id = system_id
        self.hostname = hostname
        self.owner_id = owner_id
        self.ip_address = ip_address
        self.os_type = os_type
        if last_seen:
            self.last_seen = last_seen

    def __repr__(self):
        return f"<System {self.system_id} | {self.hostname}>"


# ==========================================================
# LOG MODEL
# ==========================================================
class Log(db.Model):
    """
    Logs collected from agents
    Used by AI engine for correlation & detection
    """
    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key=True)

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

    def __init__(self, system_id, timestamp, source, level, message):
        self.system_id = system_id
        self.timestamp = timestamp
        self.source = source
        self.level = level
        self.message = message

    def __repr__(self):
        return f"<Log {self.system_id} | {self.level}>"


# ==========================================================
# ALERT MODEL
# ==========================================================
class Alert(db.Model):
    """
    AI-generated alerts:
    - Phishing detection
    - Malware detection
    - Anomaly detection
    - Policy violations
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
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __init__(self, system_id, description, severity="Medium", alert_type="generic"):
        self.system_id = system_id
        self.description = description
        self.severity = severity
        self.alert_type = alert_type

    def __repr__(self):
        return f"<Alert {self.system_id} | {self.severity}>"

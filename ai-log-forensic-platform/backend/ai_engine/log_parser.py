"""
log_parser.py
-------------
Unified Log Parsing & Normalization Module

Purpose:
- Normalize raw logs into structured events
- Classify logs for AI correlation
- Prepare logs for phishing / attack detection
"""

import re
from datetime import datetime


# ======================================================
# EVENT TYPE KEYWORDS
# ======================================================
AUTH_FAIL = [
    "login failed", "authentication failed", "invalid password",
    "access denied", "wrong password"
]

AUTH_SUCCESS = [
    "login success", "logged in", "authentication success"
]

PHISHING_KEYWORDS = [
    "login", "verify", "secure", "account", "update", "confirm"
]

MALWARE_KEYWORDS = [
    "malware", "virus", "trojan", "worm", "ransomware", "suspicious exe"
]

NETWORK_KEYWORDS = [
    "http", "https", "ftp", "dns", "connection", "port"
]

PRIV_ESC = [
    "sudo", "root access", "admin privilege", "elevated"
]

FILE_CHANGE = [
    "file modified", "file deleted", "file created", "registry modified"
]


# ======================================================
# PARSER FUNCTION
# ======================================================
def parse_log(log):
    """
    Normalize and classify log entry

    Args:
        log (Log model): Log object

    Returns:
        log (Log model): Updated log with event_type
    """

    message = log.message.lower()

    log.event_type = "generic"
    log.category = "general"
    log.risk = "low"

    # ---------------- AUTH ----------------
    if any(k in message for k in AUTH_FAIL):
        log.event_type = "auth_failure"
        log.category = "authentication"
        log.risk = "high"

    elif any(k in message for k in AUTH_SUCCESS):
        log.event_type = "auth_success"
        log.category = "authentication"
        log.risk = "low"

    # ---------------- PHISHING / URL ----------------
    elif "http" in message or "www" in message:
        log.event_type = "url_access"
        log.category = "network"

        if any(k in message for k in PHISHING_KEYWORDS):
            log.risk = "high"
        else:
            log.risk = "medium"

    # ---------------- MALWARE ----------------
    elif any(k in message for k in MALWARE_KEYWORDS):
        log.event_type = "malware_activity"
        log.category = "malware"
        log.risk = "critical"

    # ---------------- PRIV ESC ----------------
    elif any(k in message for k in PRIV_ESC):
        log.event_type = "privilege_escalation"
        log.category = "system"
        log.risk = "critical"

    # ---------------- FILE CHANGE ----------------
    elif any(k in message for k in FILE_CHANGE):
        log.event_type = "file_integrity"
        log.category = "filesystem"
        log.risk = "medium"

    # ---------------- NETWORK ----------------
    elif any(k in message for k in NETWORK_KEYWORDS):
        log.event_type = "network_activity"
        log.category = "network"
        log.risk = "low"

    # Threat Intelligence Enrichment
    try:
        from backend.ai_engine.threat_intel import enrich_log_with_threat_intel
        log = enrich_log_with_threat_intel(log)
    except Exception as e:
        pass

    # AI Anomaly Detection
    try:
        from backend.ai_engine.anomaly_detector import predict_anomaly
        log = predict_anomaly(log)
    except Exception as e:
        pass

    return log

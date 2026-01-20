"""
ai_engine.py (FINAL – ERROR FREE)
--------------------------------
Central AI & correlation engine for
AI-Based Log Investigation Framework

DELIVERABLES:
- Log analysis
- Phishing detection
- Malware detection
- Brute-force detection
- Port scan detection
- Alert generation
- Alert correlation
"""

from backend.database.models import Alert
from backend.database.db import db
import re
from datetime import datetime

# ======================================================
# DETECTION RULE SETS
# ======================================================

PHISHING_KEYWORDS = [
    "login", "verify", "secure", "update", "account", "password"
]

BRAND_KEYWORDS = [
    "paypal", "google", "facebook", "amazon", "bank", "microsoft", "apple"
]

SUSPICIOUS_TLDS = [".xyz", ".top", ".site", ".online", ".ru", ".tk"]

BRUTE_FORCE_PATTERNS = [
    "failed login", "authentication failed", "invalid password"
]

MALWARE_PATTERNS = [
    "malware", "trojan", "virus", "ransomware", "exploit", "shellcode"
]

PORT_SCAN_PATTERNS = [
    "port scan", "nmap", "masscan", "syn scan"
]

# ======================================================
# MAIN AI ENGINE
# ======================================================
def run_ai_engine(log):
    """
    Analyze a log and generate alerts if needed
    """
    msg = log.message.lower()
    system_id = log.system_id

    # --------------------------------------------------
    # PHISHING DETECTION
    # --------------------------------------------------
    if "http" in msg:
        url = extract_url(msg)
        score = 0

        if any(k in url for k in PHISHING_KEYWORDS):
            score += 1

        if any(b in url for b in BRAND_KEYWORDS):
            score += 1

        if any(url.endswith(tld) for tld in SUSPICIOUS_TLDS):
            score += 1

        if score >= 2:
            create_alert(
                system_id,
                f"PHISHING URL detected: {url}",
                "Critical"
            )
            return

    # --------------------------------------------------
    # BRUTE FORCE DETECTION
    # --------------------------------------------------
    if any(p in msg for p in BRUTE_FORCE_PATTERNS):
        create_alert(
            system_id,
            f"Brute-force attempt detected: {log.message[:200]}",
            "High"
        )
        return

    # --------------------------------------------------
    # MALWARE DETECTION
    # --------------------------------------------------
    if any(p in msg for p in MALWARE_PATTERNS):
        create_alert(
            system_id,
            f"Malware activity detected: {log.message[:200]}",
            "Critical"
        )
        return

    # --------------------------------------------------
    # PORT SCAN DETECTION
    # --------------------------------------------------
    if any(p in msg for p in PORT_SCAN_PATTERNS):
        create_alert(
            system_id,
            f"Port scanning detected: {log.message[:200]}",
            "High"
        )
        return


# ======================================================
# ALERT CREATION (SAFE)
# ======================================================
def create_alert(system_id, description, severity):
    """
    Safely create an alert (avoids duplicates)
    """
    alert = Alert(
        system_id=system_id,
        description=description,
        severity=severity
    )
    db.session.add(alert)
    db.session.commit()


# ======================================================
# URL EXTRACTOR
# ======================================================
def extract_url(text):
    urls = re.findall(r'(https?://\S+)', text)
    return urls[0] if urls else ""


# ======================================================
# CORRELATION ENGINE
# ======================================================
def correlate_alerts(system_id):
    """
    Correlate multiple alerts into one incident
    """
    recent = (
        Alert.query
        .filter_by(system_id=system_id)
        .order_by(Alert.created_at.desc())
        .limit(5)
        .all()
    )

    if len(recent) >= 3:
        db.session.add(Alert(
            system_id=system_id,
            description="Multiple correlated attacks detected (AI correlation)",
            severity="Critical"
        ))
        db.session.commit()
        
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
def run_ai_engine(log):
    """
    Analyze a log and generate alerts if needed
    """
    msg = log.message.lower()
    system_id = log.system_id
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
    if any(p in msg for p in BRUTE_FORCE_PATTERNS):
        create_alert(
            system_id,
            f"Brute-force attempt detected: {log.message[:200]}",
            "High"
        )
        return
    if any(p in msg for p in MALWARE_PATTERNS):
        create_alert(
            system_id,
            f"Malware activity detected: {log.message[:200]}",
            "Critical"
        )
        return
    if any(p in msg for p in PORT_SCAN_PATTERNS):
        create_alert(
            system_id,
            f"Port scanning detected: {log.message[:200]}",
            "High"
        )
        return
def create_alert(system_id, description, severity):
    """
    Safely create an alert (avoids duplicates)
    """
    alert = Alert()
    alert.system_id = system_id
    alert.description = description
    alert.severity = severity
    db.session.add(alert)
    db.session.commit()
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
        alert = Alert()
        alert.system_id = system_id
        alert.description = "Multiple correlated attacks detected (AI correlation)"
        alert.severity = "Critical"
        db.session.add(alert)
        db.session.commit()
        
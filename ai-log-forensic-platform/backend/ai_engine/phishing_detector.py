"""
phishing_detector.py (FINAL VERSION)
------------------------------------
Detects phishing links and phishing pages
from logs collected by local agents.

DELIVERABLES:
- Phishing URL detection
- Phishing page detection
- Brand impersonation detection
- Risk scoring
- Alert generation
- SOC ready logic
"""

import re
from datetime import datetime
from backend.database.models import Alert
from backend.database.db import db

# =====================================================
# CONFIGURATION
# =====================================================

PHISHING_KEYWORDS = [
    "login", "verify", "secure", "update", "account",
    "password", "signin", "confirm", "bank"
]

SUSPICIOUS_TLDS = [
    ".xyz", ".top", ".site", ".online", ".tk", ".ru",
    ".ml", ".cf", ".ga", ".gq"
]

BRAND_NAMES = [
    "paypal", "google", "facebook", "amazon", "microsoft",
    "apple", "bank", "instagram", "netflix"
]


# =====================================================
# MAIN DETECTION FUNCTION
# =====================================================
def detect_phishing(log):
    """
    Detect phishing attacks from log message

    Args:
        log (Log): Log model object

    Returns:
        tuple: (risk, event_type)
    """

    msg = log.message.lower()

    # Only process if URL present
    urls = extract_urls(msg)
    if not urls:
        return "low", "normal"

    for url in urls:
        score = 0

        # Keyword based detection
        if any(k in url for k in PHISHING_KEYWORDS):
            score += 1

        # Suspicious TLD
        if any(url.endswith(tld) for tld in SUSPICIOUS_TLDS):
            score += 1

        # Brand impersonation
        if any(b in url for b in BRAND_NAMES):
            score += 1

        # IP-based URL
        if re.match(r"http[s]?://\d+\.\d+\.\d+\.\d+", url):
            score += 1

        # Final decision
        if score >= 2:
            create_alert(log, url, score)
            return "critical", "phishing"

    return "low", "normal"


# =====================================================
# ALERT CREATION
# =====================================================
def create_alert(log, url, score):
    """
    Store phishing alert
    """
    severity = "Critical" if score >= 3 else "High"

    alert = Alert()
    alert.system_id = log.system_id
    alert.description = f"Phishing page/link detected: {url}"
    alert.severity = severity
    alert.alert_type = "phishing"

    db.session.add(alert)
    db.session.commit()


# =====================================================
# URL EXTRACTION
# =====================================================
def extract_urls(text):
    """
    Extract all URLs from text
    """
    return re.findall(r"(https?://[^\s]+)", text)

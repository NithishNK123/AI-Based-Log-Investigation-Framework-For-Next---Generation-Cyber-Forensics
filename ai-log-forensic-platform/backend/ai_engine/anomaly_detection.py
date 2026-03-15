
SUSPICIOUS_KEYWORDS = [
    "failed password",
    "unauthorized",
    "permission denied",
    "access denied",
    "authentication failure",
    "invalid user",
    "root login",
    "sql injection",
    "malware",
    "exploit",
    "brute force"
]


def detect_anomaly(log):
    """
    Detect whether a log entry is anomalous.

    Args:
        log (dict): Log dictionary containing:
            - system_id
            - timestamp
            - source
            - level
            - message

    Returns:
        bool: True if anomaly detected, else False
    """

    if not log or "message" not in log:
        return False

    message = log["message"].lower()

    # -------- Rule 1: Keyword-based detection --------
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in message:
            return True

    # -------- Rule 2: High severity level --------
    if log.get("level", "").upper() in ["ERROR", "CRITICAL"]:
        return True

    # -------- Rule 3: Abnormal source behavior --------
    if log.get("source") == "authentication" and "failed" in message:
        return True

    return False

def detect_anomalies(logs):
    """
    Detect anomalies in a batch of logs.

    Args:
        logs (list): List of log dictionaries

    Returns:
        list: Indices of logs that are anomalous
    """
    anomalous_indices = []
    
    for idx, log in enumerate(logs):
        if detect_anomaly(log):
            anomalous_indices.append(idx)
    
    return anomalous_indices
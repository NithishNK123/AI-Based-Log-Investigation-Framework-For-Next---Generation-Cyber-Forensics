"""
agent_identity.py
-----------------
Secure identity manager for local log agent.

Responsibilities:
- Detect first run
- Generate unique system ID
- Generate agent secret
- Persist identity securely
- Prevent identity regeneration
- Provide identity to log sender

Used by:
- log_collector.py
- log_sender.py
- agent_installer.py
"""

import os
import json
import uuid
import hashlib
import platform
from datetime import datetime

# -------------------------------------------------------
# CONFIG
# -------------------------------------------------------
AGENT_DIR = os.path.join(os.path.expanduser("~"), ".ai_log_agent")
IDENTITY_FILE = os.path.join(AGENT_DIR, "identity.json")


# -------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------

def _machine_fingerprint():
    """
    Create stable fingerprint for this machine
    (used to detect reinstall or tampering)
    """
    raw = f"{platform.node()}-{platform.system()}-{platform.processor()}"
    return hashlib.sha256(raw.encode()).hexdigest()


# -------------------------------------------------------
# MAIN IDENTITY MANAGER
# -------------------------------------------------------

def load_or_create_identity():
    """
    Load agent identity or create on first run.

    Returns:
        dict: system_id, agent_secret, fingerprint, created_at
    """

    # Ensure agent directory exists
    os.makedirs(AGENT_DIR, exist_ok=True)

    # First run
    if not os.path.exists(IDENTITY_FILE):
        identity = {
            "system_id": str(uuid.uuid4()),
            "agent_secret": str(uuid.uuid4()),
            "fingerprint": _machine_fingerprint(),
            "created_at": datetime.utcnow().isoformat(),
            "version": "1.0"
        }

        with open(IDENTITY_FILE, "w") as f:
            json.dump(identity, f, indent=4)

        return identity

    # Subsequent runs
    with open(IDENTITY_FILE, "r") as f:
        identity = json.load(f)

    # Tamper detection (optional warning)
    if identity.get("fingerprint") != _machine_fingerprint():
        print("[WARNING] Agent identity fingerprint mismatch (possible copy/move)")

    return identity

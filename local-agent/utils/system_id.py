"""
system_id.py
------------
Generates and manages a unique system identifier for the local agent.

The system ID is:
- Generated once
- Stored locally
- Reused across agent restarts
"""

import uuid
import os

# File where system ID is stored
SYSTEM_ID_FILE = ".system_id"


def get_system_id():
    """
    Retrieve or generate a unique system ID.

    Returns:
        str: Unique system identifier
    """

    # If system ID already exists, read and return it
    if os.path.exists(SYSTEM_ID_FILE):
        try:
            with open(SYSTEM_ID_FILE, "r") as file:
                system_id = file.read().strip()
                if system_id:
                    return system_id
        except Exception:
            pass

    # Generate new system ID
    system_id = str(uuid.uuid4())

    # Save system ID locally
    try:
        with open(SYSTEM_ID_FILE, "w") as file:
            file.write(system_id)
    except Exception:
        pass

    return system_id

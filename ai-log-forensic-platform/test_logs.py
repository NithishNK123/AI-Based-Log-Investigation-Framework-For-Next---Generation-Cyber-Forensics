"""
Test script to send sample logs to the backend for populating the dashboard
"""
import requests
import json
from datetime import datetime
import uuid

# Configuration
SERVER_URL = "http://127.0.0.1:8000/api/logs"
API_KEY = "TEST_API_KEY_123"
SYSTEM_ID = str(uuid.uuid4())

# Sample logs with various security events
sample_logs = [
    {
        "timestamp": datetime.utcnow().isoformat(),
        "source": "AUTH",
        "level": "ERROR",
        "message": "Failed password for invalid user from 192.168.1.100"
    },
    {
        "timestamp": datetime.utcnow().isoformat(),
        "source": "AUTH",
        "level": "CRITICAL",
        "message": "Possible brute force attempt: 10 failed logins in 5 minutes from 10.0.0.50"
    },
    {
        "timestamp": datetime.utcnow().isoformat(),
        "source": "MALWARE",
        "level": "CRITICAL",
        "message": "Trojan.Generic detected in C:\\Users\\Admin\\Downloads\\file.exe"
    },
    {
        "timestamp": datetime.utcnow().isoformat(),
        "source": "WEB",
        "level": "WARNING",
        "message": "Phishing attempt detected: URL http://195.154.12.34/verify-paypal-login.html"
    },
    {
        "timestamp": datetime.utcnow().isoformat(),
        "source": "NETWORK",
        "level": "WARNING",
        "message": "Port scan detected from 203.0.113.45 scanning ports 20-1024"
    },
    {
        "timestamp": datetime.utcnow().isoformat(),
        "source": "PRIVILEGE",
        "level": "CRITICAL",
        "message": "Unauthorized privilege escalation: user 'guest' granted root privileges"
    },
    {
        "timestamp": datetime.utcnow().isoformat(),
        "source": "FILE",
        "level": "HIGH",
        "message": "File integrity violation: /etc/passwd modified"
    },
    {
        "timestamp": datetime.utcnow().isoformat(),
        "source": "AUTH",
        "level": "INFO",
        "message": "User 'admin' successfully authenticated from 192.168.1.10"
    },
]

def send_logs():
    """Send logs to the backend"""
    payload = {
        "system_id": SYSTEM_ID,
        "logs": sample_logs
    }
    
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(SERVER_URL, json=payload, headers=headers, timeout=5)
        print(f"✓ Sent {len(sample_logs)} logs to server")
        print(f"Response Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 201
    except Exception as e:
        print(f"✗ Error sending logs: {e}")
        return False

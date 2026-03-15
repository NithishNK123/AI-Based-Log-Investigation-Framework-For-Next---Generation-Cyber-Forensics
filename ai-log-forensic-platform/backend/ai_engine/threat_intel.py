"""
threat_intel.py
---------------
Integrates with external Threat Intelligence feeds (e.g., AbuseIPDB, VirusTotal)
to enrich logs with known malicious indicators (IPs, Hashes).
"""

import re
import requests

def extract_ipv4(text):
    """
    Extracts the first valid IPv4 address from a block of text.
    """
    match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', text)
    if match:
        return match.group(0)
    return None

def check_ip_reputation(ip_address):
    """
    Queries a Threat Intelligence feed for the IP reputation.
    MOCK IMPLEMENTATION: Simulates an API call since no actual keys are provided.
    In a real scenario, this would call AbuseIPDB or VirusTotal.
    """
    # Mocking standard malicious IP blocks for testing purposes
    malicious_prefixes = ["185.15", "45.22", "192.168.100.99"]
    
    score = 0
    description = "Clean"
    
    for prefix in malicious_prefixes:
        if ip_address.startswith(prefix):
            score = 95
            description = "Known malicious actor (Botnet/Spam)"
            break
            
    # Simulate a slow API call occasionally or network latency
    # time.sleep(0.1) 
    
    return {
        "ip": ip_address,
        "is_malicious": score > 50,
        "abuse_score": score,
        "intel_source": "MockFeed",
        "description": description
    }

def enrich_log_with_threat_intel(log):
    """
    Extracts indicators from the log message and checks their reputation.
    Updates the log's risk and event_type if a severe threat is found.
    """
    ip = extract_ipv4(log.message)
    if not ip:
        # Check source field if message doesn't contain an IP
        ip = extract_ipv4(log.source)
        
    if ip:
        result = check_ip_reputation(ip)
        
        # Attach the result to the log message for context
        if result["is_malicious"]:
            log.message += f" | [THREAT INTEL] IP {ip} flagged! Score: {result['abuse_score']}. Info: {result['description']}"
            
            # Elevate risk
            log.risk = "critical"
            log.event_type = "known_threat_actor"
            log.category = "threat_intel"
            
    return log

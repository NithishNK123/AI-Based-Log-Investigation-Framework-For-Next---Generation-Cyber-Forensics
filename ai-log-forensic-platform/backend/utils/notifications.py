"""
notifications.py
----------------
Utility for pushing real-time alerts to external channels (Slack, Email, etc.)
based on user-defined NotificationRules.
"""
import threading
from backend.database.models import NotificationRule

def send_slack_message(webhook_url, text):
    """Stub for sending a Slack message via Webhook."""
    # In a real app: requests.post(webhook_url, json={"text": text})
    print(f"[SLACK STUB] Sending to {webhook_url}: {text}")

def send_email_alert(email_address, subject, text):
    """Stub for sending an Email alert."""
    # In a real app: use smtplib or an API like SendGrid
    print(f"[EMAIL STUB] Sending to {email_address} | Subject: {subject} | Body: {text}")

def process_alert_notifications(alert):
    """
    Evaluate all active notification rules against a new Alert.
    If conditions match, dispatch the notification.
    """
    # Fetch all active rules
    # In a fully multi-tenant setup, we'd only fetch rules for the alert's system owner.
    # We'll fetch all rules for the owner of the system this alert is tied to.
    rules = NotificationRule.query.filter_by(is_active=True).all()
    
    for rule in rules:
        # Check conditions
        match = True
        
        # Severity condition
        if rule.target_severity and rule.target_severity.upper() != "ALL":
            if alert.severity.upper() != rule.target_severity.upper():
                match = False
                
        if match:
            # Dispatch
            msg = f"Alert [{alert.severity}] on System {alert.system_id}: {alert.description}"
            subject = f"Security Alert: {alert.severity} Detected"
            
            if rule.channel.upper() == "SLACK":
                send_slack_message(rule.destination, msg)
            elif rule.channel.upper() == "EMAIL":
                send_email_alert(rule.destination, subject, msg)

def trigger_notifications_async(alert_id):
    """
    Helper to run notification processing in a background thread
    so it doesn't block the main API request.
    """
    from backend.app import create_app
    from backend.database.models import Alert
    
    def task():
        app = create_app()
        with app.app_context():
            alert = Alert.query.get(alert_id)
            if alert:
                process_alert_notifications(alert)
                
    threading.Thread(target=task).start()

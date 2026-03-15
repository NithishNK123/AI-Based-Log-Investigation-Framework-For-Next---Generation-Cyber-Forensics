"""
test_features.py
----------------
A manual test script to verify that the newly implemented
Advanced SIEM capabilities are functioning correctly.
"""

from backend.app import create_app
from backend.database.db import db
from backend.database.models import User, System, Log, Alert, IncidentTicket, NotificationRule

def setup_test_data(app):
    with app.app_context():
        # Clean current database
        db.drop_all()
        db.create_all()

        print("[*] Setting up mock data...")
        admin = User(username="admin_test", password="hashedpassword", role="admin")
        db.session.add(admin)
        db.session.commit()

        sys1 = System(system_id="SYS-DEV-001", hostname="dev-workstation", ip_address="192.168.1.10", owner_id=admin.id)
        db.session.add(sys1)
        db.session.commit()

        # Add Notification Rule
        rule = NotificationRule(user_id=admin.id, channel="Slack", destination="https://hooks.slack.com/stub", target_severity="Critical")
        db.session.add(rule)
        db.session.commit()

        return admin, sys1

def test_log_ingestion_and_threat_intel():
    app = create_app()
    setup_test_data(app)

    print("\n--- Testing Threat Intel & Anomaly parsing ---")
    with app.app_context():
        sys1 = System.query.first()
        from backend.ai_engine.log_parser import parse_log
        
        # Test 1: Normal Log
        log1 = Log(system_id=sys1.system_id, message="User logged in successfully.", source="auth.log")
        log1 = parse_log(log1)
        print(f"Log 1 (Normal): Risk = {getattr(log1, 'risk', 'low')}, Event = {log1.event_type}")
        assert getattr(log1, 'risk', 'low') == "low"

        # Test 2: Threat Intel Log (Malicious IP)
        log2 = Log(system_id=sys1.system_id, message="Connection attempt from 185.15.2.14", source="firewall.log")
        log2 = parse_log(log2)
        print(f"Log 2 (Threat Intel): Risk = {getattr(log2, 'risk', 'unknown')}, Event = {log2.event_type}")
        assert getattr(log2, 'risk', 'unknown') == "critical"
        assert "THREAT INTEL" in getattr(log2, 'message', '')

def test_anomaly_training():
    app = create_app()
    print("\n--- Testing Anomaly Training ---")
    with app.app_context():
        # Assume db already populated from setup_test_data
        sys1 = System.query.first()
        
        # Generate 150 normal logs to train baseline
        for i in range(150):
            l = Log(system_id=sys1.system_id, message=f"Standard ping {i}", source="sys01", level="INFO")
            db.session.add(l)
        db.session.commit()

        from backend.ai_engine.anomaly_detector import train_isolation_forest, predict_anomaly, SKLEARN_AVAILABLE
        
        if not SKLEARN_AVAILABLE:
            print("Skipping training test: scikit-learn not available.")
            return

        success = train_isolation_forest(sys1.system_id)
        print(f"Training success: {success}")
        
        if success:
            # Predict outlier (CRITICAL error at 3am)
            from datetime import datetime
            outlier = Log(system_id=sys1.system_id, message="Kernel panic", source="syslog", level="CRITICAL", timestamp=datetime.utcnow())
            outlier.timestamp = outlier.timestamp.replace(hour=3) # weird time
            outlier = predict_anomaly(outlier)
            print(f"Outlier Risk: {getattr(outlier, 'risk', 'unknown')}")

def run_all():
    print("========================================")
    print("  SIEM FEATURE TESTS RUNNING            ")
    print("========================================")
    test_log_ingestion_and_threat_intel()
    test_anomaly_training()
    print("========================================")
    print("  ALL TESTS COMPLETED                   ")
    print("========================================")

if __name__ == "__main__":
    run_all()

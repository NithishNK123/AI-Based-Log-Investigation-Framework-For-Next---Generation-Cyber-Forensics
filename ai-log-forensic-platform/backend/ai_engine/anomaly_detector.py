"""
anomaly_detector.py
-------------------
AI-Powered Anomaly Detection using Isolation Forest.

Trains a baseline for normal system behavior and detects 
anomalous log patterns (e.g., unusual hours, weird severity spikes).
"""

import os
import joblib
import numpy as np
from datetime import datetime

# Attempt to import sklearn. If missing, we'll gracefully fail in predict_anomaly
try:
    from sklearn.ensemble import IsolationForest
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

MODEL_DIR = "backend/ai_engine/models"

def get_model_path(system_id):
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    return os.path.join(MODEL_DIR, f"iforest_{system_id}.joblib")

def extract_features(log):
    """
    Extract numerical features from a log entry for the ML model.
    """
    # 1. Time of day (0-23)
    hour = log.timestamp.hour if hasattr(log.timestamp, "hour") else 12
    
    # 2. Risk/Level Encoding
    level_map = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3, "CRITICAL": 4}
    level_num = level_map.get(str(log.level).upper(), 1)
    
    # 3. Source hash (simple representation of the log source)
    source_hash = sum(ord(c) for c in str(log.source)) % 100
    
    return [hour, level_num, source_hash]

def train_isolation_forest(system_id):
    """
    Train an Isolation Forest model for the given system using its historical logs.
    """
    if not SKLEARN_AVAILABLE:
        print("[AI ENGINE] scikit-learn is not installed. Run 'pip install scikit-learn'")
        return False
        
    from backend.database.models import Log
    
    # Fetch recent logs for training
    logs = Log.query.filter_by(system_id=system_id).order_by(Log.timestamp.desc()).limit(10000).all()
    if len(logs) < 100:
        print(f"[AI ENGINE] Not enough logs to establish a baseline for {system_id} (Need at least 100)")
        return False
        
    features = [extract_features(l) for l in logs]
    X = np.array(features)
    
    # Contamination defines the expected proportion of anomalies
    model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
    model.fit(X)
    
    joblib.dump(model, get_model_path(system_id))
    print(f"[AI ENGINE] Baseline model trained and saved for {system_id} using {len(logs)} logs.")
    return True

def predict_anomaly(log):
    """
    Predict if a new log is an anomaly using the system's trained model.
    """
    if not SKLEARN_AVAILABLE:
        return log # Skip if no ML library
        
    model_path = get_model_path(log.system_id)
    if not os.path.exists(model_path):
        return log # No model trained yet, act as pass-through
        
    try:
        model = joblib.load(model_path)
        X_new = np.array([extract_features(log)])
        
        # Predict returns 1 for inliers, -1 for outliers
        prediction = model.predict(X_new)[0]
        
        if prediction == -1:
            # If the log was already generic or low risk, bump it up
            if getattr(log, "risk", "low") in ["low", None]:
                log.event_type = "ai_anomaly"
                log.risk = "high"
                log.message = "[AI ANOMALY DETECTED] " + log.message
                log.category = "security_anomaly"
                
    except Exception as e:
        print(f"[AI ENGINE] Error during prediction: {e}")
        
    return log

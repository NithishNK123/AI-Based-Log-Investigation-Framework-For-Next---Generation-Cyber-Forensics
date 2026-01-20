"""
config.py
---------
Central configuration file for the AI Log Forensic Platform backend.

Contains:
- Flask configuration
- Database configuration
- Agent authentication settings
"""

import os


class Config:
    # -----------------------------
    # Flask Core Configuration
    # -----------------------------
    SECRET_KEY = os.environ.get("SECRET_KEY", "forensic-secret-key")

    # -----------------------------
    # Database Configuration
    # -----------------------------
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "sqlite:///" + os.path.join(BASE_DIR, "forensic.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # -----------------------------
    # Agent Authentication
    # -----------------------------
    # Must match agent_config.yaml
    AGENT_API_KEY = os.environ.get("AGENT_API_KEY", "TEST_API_KEY_123")

    # -----------------------------
    # Application Settings
    # -----------------------------
    DEBUG = True

    # -----------------------------
    # LogAI / AI Engine Settings
    # -----------------------------
    LOGAI_ENABLED = True
    LOGAI_ANALYSIS_LIMIT = 500

    # -----------------------------
    # Report Settings
    # -----------------------------
    REPORT_OUTPUT_DIR = os.path.join(BASE_DIR, "generated_reports")

"""
db.py
-----
Initializes and provides the database instance for the
AI Log Forensic Platform using Flask-SQLAlchemy.
"""

from flask_sqlalchemy import SQLAlchemy

# Create SQLAlchemy database instance
db = SQLAlchemy()

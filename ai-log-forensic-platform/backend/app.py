"""
app.py
------
Main Flask application factory for
AI-Based Log Investigation Framework.
"""

from flask import Flask, jsonify, render_template
from flask_cors import CORS

from backend.config import Config
from backend.database.db import db

# Import blueprints
from backend.routes.auth import auth_bp
from backend.routes.register import register_bp
from backend.routes.logs_api import logs_api_bp
from backend.routes.dashboard import dashboard_bp
from backend.routes.incidents import incidents_bp
from backend.routes.settings import settings_bp


def create_app():
    app = Flask(
        __name__,
        template_folder="../frontend/templates",
        static_folder="../frontend/static"
    )

    # Load configuration
    app.config.from_object(Config)

    # Enable CORS
    CORS(app)

    # Initialize database
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(logs_api_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(incidents_bp)
    app.register_blueprint(settings_bp)

    # Create tables if not exist
    with app.app_context():
        db.create_all()

    # ==================================================
    # API Health Check
    # ==================================================
    @app.route("/api")
    def api_home():
        return jsonify({
            "message": "AI Log Forensic Platform API",
            "version": "1.0",
            "status": "running"
        })

    # ==================================================
    # HTML Pages (Frontend)
    # ==================================================
    @app.route("/")
    def login_page():
        return render_template("login.html")

    @app.route("/register")
    def register_page():
        return render_template("register.html")

    @app.route("/dashboard")
    def dashboard_page():
        return render_template("dashboard.html")

    @app.route("/systems")
    def systems_page():
        return render_template("systems.html")

    @app.route("/logs")
    def logs_page():
        return render_template("logs.html")

    @app.route("/reports")
    def reports_page():
        return render_template("reports.html")

    @app.route("/incidents")
    def incidents_page():
        return render_template("incidents.html")

    @app.route("/settings")
    def settings_page():
        return render_template("settings.html")

    # ==================================================
    # Error Handlers
    # ==================================================
    @app.errorhandler(404)
    def not_found(e):
        # Return HTML page for browser, JSON for API
        if str(e).startswith("404"):
            return render_template("login.html")
        return jsonify({"error": "Not Found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal Server Error"}), 500

    return app

"""
auth.py
-------
Handles user authentication for the AI Log Forensic Platform.

Features:
- User registration
- User login
- Password hashing (secure)
- Basic role support
"""

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from backend.database.db import db
from backend.database.models import User

# Blueprint for authentication routes
auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


# ==========================================================
# REGISTER USER
# ==========================================================
@auth_bp.route("/register", methods=["POST"])
def register_user():
    """
    Register a new user (Admin / Analyst)

    Expected JSON:
    {
        "username": "admin",
        "password": "admin123",
        "role": "admin" (optional)
    }
    """

    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password required"}), 400

    # Check if user already exists
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "User already exists"}), 409

    # Hash password (VERY IMPORTANT)
    hashed_password = generate_password_hash(data["password"])

    user = User(
        username=data["username"],
        password=hashed_password,
        role=data.get("role", "analyst")
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "status": "registered",
        "username": user.username,
        "role": user.role
    }), 201


# ==========================================================
# LOGIN USER
# ==========================================================
@auth_bp.route("/login", methods=["POST"])
def login_user():
    """
    Authenticate user login

    Expected JSON:
    {
        "username": "admin",
        "password": "admin123"
    }
    """

    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password required"}), 400

    user = User.query.filter_by(username=data["username"]).first()

    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    # Verify hashed password
    if not check_password_hash(user.password, data["password"]):
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({
        "status": "success",
        "username": user.username,
        "role": user.role
    }), 200

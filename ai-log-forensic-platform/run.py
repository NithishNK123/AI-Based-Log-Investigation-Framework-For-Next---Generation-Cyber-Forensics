"""
run.py
------
Entry point for the AI-Based Log Investigation Platform.

Responsibilities:
- Create Flask application
- Start backend server
"""

from backend.app import create_app

# Create Flask app
app = create_app()

if __name__ == "__main__":
    # Run the application
    app.run(
        host="0.0.0.0",   # Accessible from other devices in network
        port=8000,        # Backend port
        debug=True        # Enable debug for development
    )

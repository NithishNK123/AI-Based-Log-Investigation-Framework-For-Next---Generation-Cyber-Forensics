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
    print("=" * 60)
    print("[LAUNCH] AI-BASED LOG FORENSIC PLATFORM")
    print("=" * 60)
    print("[OK] Starting Flask Backend Server...")
    print("[INFO] Access the application at: http://127.0.0.1:8000")
    print("[INFO] API Health Check: http://127.0.0.1:8000/api")
    print("[INFO] Dashboard: http://127.0.0.1:8000/dashboard")
    print("=" * 60)
    print()
    
    try:
        app.run(host="127.0.0.1", port=8000, debug=True)
    except KeyboardInterrupt:
        print("\n\n[STOP] Server stopped by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")

"""
setup_db.py
-----------
Initialize database with default test user
"""

from backend.app import create_app
from backend.database.db import db
from backend.database.models import User
from werkzeug.security import generate_password_hash

# Create Flask app
app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()
    print("✓ Database tables created")
    
    # Check if admin user exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        # Create default admin user
        admin = User(
            username='admin',
            password=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("✓ Admin user created: username='admin', password='admin123'")
    else:
        print("✓ Admin user already exists")
    
    # Create test user for non-admin
    test_user = User.query.filter_by(username='analyst').first()
    if not test_user:
        analyst = User(
            username='analyst',
            password=generate_password_hash('analyst123'),
            role='analyst'
        )
        db.session.add(analyst)
        db.session.commit()
        print("✓ Analyst user created: username='analyst', password='analyst123'")
    else:
        print("✓ Analyst user already exists")
    
    print("\n✅ Database setup complete!")

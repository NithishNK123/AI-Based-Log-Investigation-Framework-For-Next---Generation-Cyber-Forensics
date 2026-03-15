"""
reset_db.py
-----------
SAFE Database reset script

WARNING: This script will DELETE ALL data and recreate the database!

Usage:
    python reset_db.py
"""

import os
import sys
from backend.app import create_app
from backend.database.db import db
from backend.database.models import User
from werkzeug.security import generate_password_hash


def reset_database():
    """
    Safely reset the database:
    1. Drop all tables
    2. Recreate all tables
    3. Create default users
    """
    
    print("\n" + "="*70)
    print("DATABASE RESET UTILITY")
    print("="*70)
    print("\n⚠️  WARNING: This will DELETE ALL logs, alerts, and systems!")
    print("⚠️  WARNING: Users will NOT be deleted (safe mode)")
    print("\nProceed? (yes/no): ", end="")
    
    response = input().strip().lower()
    
    if response not in ['yes', 'y']:
        print("❌ Reset cancelled.")
        return
    
    print("\n🔄 Starting database reset...\n")
    
    # Create app context
    app = create_app()
    
    with app.app_context():
        try:
            # Drop all tables
            print("📊 Dropping all tables...")
            db.drop_all()
            print("✓ Tables dropped\n")
            
            # Recreate all tables
            print("📊 Creating fresh tables...")
            db.create_all()
            print("✓ Tables created\n")
            
            # Create default users (SAFE MODE - keeps existing users)
            print("👤 Checking default users...\n")
            
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User()
                admin.username = 'admin'
                admin.password = generate_password_hash('admin123')
                admin.role = 'admin'
                db.session.add(admin)
                print("✓ Created admin: username='admin', password='admin123'")
            else:
                print("✓ Admin user already exists (preserved)")
            
            analyst = User.query.filter_by(username='analyst').first()
            if not analyst:
                analyst = User()
                analyst.username = 'analyst'
                analyst.password = generate_password_hash('analyst123')
                analyst.role = 'analyst'
                db.session.add(analyst)
                print("✓ Created analyst: username='analyst', password='analyst123'")
            else:
                print("✓ Analyst user already exists (preserved)")
            
            db.session.commit()
            
            print("\n" + "="*70)
            print("✅ DATABASE RESET COMPLETE!")
            print("="*70)
            print("\n📝 Summary:")
            print("   ✓ All logs deleted")
            print("   ✓ All alerts deleted")
            print("   ✓ All systems deleted")
            print("   ✓ All users PRESERVED (safe mode)")
            print("   ✓ New tables created with log_type support")
            print("\n🚀 You can now start fresh with:")
            print("   python run.py")
            print("\n")
            
        except Exception as e:
            print(f"\n❌ Error during reset: {str(e)}")
            print("Rolling back changes...")
            db.session.rollback()
            sys.exit(1)


if __name__ == "__main__":
    reset_database()

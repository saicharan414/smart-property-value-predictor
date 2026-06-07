#!/usr/bin/env python3
"""
Database Migration Script
Updates existing database to include admin management features
"""

import sqlite3
import os
from datetime import datetime

def migrate_database():
    """Migrate existing database to include new admin features"""
    
    db_path = 'spvp_database.db'
    
    if not os.path.exists(db_path):
        print("Database file not found. Creating new database...")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Starting database migration...")
        
        # Check if is_admin column exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add is_admin column if it doesn't exist
        if 'is_admin' not in columns:
            print("Adding is_admin column...")
            cursor.execute("ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT 0")
        
        # Update existing admin user if exists, or create new one
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        admin_user = cursor.fetchone()
        
        if admin_user:
            print("Updating existing admin user...")
            cursor.execute("UPDATE users SET is_admin = 1, role = 'admin' WHERE username = 'admin'")
        else:
            print("Creating default admin user...")
            # You'll need to hash the password properly or use the app's user creation
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, role, is_admin, is_active, created_at, prediction_count)
                VALUES ('admin', 'admin@spvp.com', 'pbkdf2:sha256:260000$salt$hash', 'admin', 1, 1, ?, 0)
            """, (datetime.utcnow().isoformat(),))
        
        # Commit changes
        conn.commit()
        print("Database migration completed successfully!")
        
        # Verify the changes
        cursor.execute("SELECT username, is_admin, role FROM users WHERE username = 'admin'")
        result = cursor.fetchone()
        print(f"Admin user verified: {result}")
        
    except Exception as e:
        print(f"Migration error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()

#!/usr/bin/env python3
"""
Database migration script to add prediction_count column to users table
"""

from app import app, db
from models import User
from sqlalchemy import text

def add_prediction_count_column():
    """Add prediction_count column to existing users table"""
    with app.app_context():
        try:
            # Check if column already exists
            inspector = db.inspect(db.engine)
            columns = inspector.get_columns('users')
            column_names = [col['name'] for col in columns]
            
            if 'prediction_count' not in column_names:
                print("Adding prediction_count column to users table...")
                
                # Add the column using raw SQL
                db.session.execute(text('ALTER TABLE users ADD COLUMN prediction_count INTEGER DEFAULT 0'))
                db.session.commit()
                
                print("✅ prediction_count column added successfully")
                
                # Update all existing users to have prediction_count = 0
                existing_users = User.query.all()
                for user in existing_users:
                    if user.prediction_count is None:
                        user.prediction_count = 0
                
                db.session.commit()
                print(f"✅ Updated {len(existing_users)} existing users with prediction_count = 0")
                
            else:
                print("✅ prediction_count column already exists")
                
        except Exception as e:
            print(f"❌ Error adding prediction_count column: {e}")
            db.session.rollback()
            return False
        
        return True

if __name__ == '__main__':
    add_prediction_count_column()

#!/usr/bin/env python3
"""
Script to check users in the database
"""
import psycopg2
from psycopg2.extras import RealDictCursor
import sys
import os

# Database connection configuration
DB_CONFIG = {
    "host": "127.0.0.1",
    "database": "pickup_football",
    "user": "postgres", 
    "password": "kingdoms",
    "port": 5432
}

def get_db_connection():
    """Get database connection"""
    try:
        print(f"Connecting to database with config: {DB_CONFIG}")
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        print("✅ Database connection successful!")
        return conn
    except psycopg2.Error as e:
        print(f"❌ Database connection error: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return None

def check_users():
    """Check all users in the database"""
    conn = get_db_connection()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    try:
        # Check if users table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'users'
            );
        """)
        table_exists = cursor.fetchone()[0]
        
        if not table_exists:
            print("❌ Users table does not exist!")
            return
            
        print("✅ Users table exists!")
        
        # Get count of users
        cursor.execute("SELECT COUNT(*) FROM users;")
        user_count = cursor.fetchone()[0]
        print(f"📊 Total users in database: {user_count}")
        
        if user_count > 0:
            # Get all users
            cursor.execute("""
                SELECT id, username, first_name, last_name, age_range, 
                       skill_level, preferred_position, playing_style, 
                       is_active, is_verified, created_at
                FROM users 
                ORDER BY created_at DESC;
            """)
            users = cursor.fetchall()
            
            print("\n👥 Users in database:")
            print("=" * 80)
            for user in users:
                print(f"ID: {user['id']}")
                print(f"Username: {user['username']}")
                print(f"Name: {user['first_name']} {user['last_name']}")
                print(f"Age Range: {user['age_range'] or 'Not specified'}")
                print(f"Skill Level: {user['skill_level']}/10")
                print(f"Preferred Position: {user['preferred_position'] or 'Not specified'}")
                print(f"Playing Style: {user['playing_style'] or 'Not specified'}")
                print(f"Active: {user['is_active']}")
                print(f"Verified: {user['is_verified']}")
                print(f"Created: {user['created_at']}")
                print("-" * 40)
        else:
            print("📭 No users found in database")
            
    except Exception as e:
        print(f"❌ Error checking users: {str(e)}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    check_users()

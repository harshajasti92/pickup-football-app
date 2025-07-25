#!/usr/bin/env python3
"""
Simple script to check if john_striker user exists
"""
import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection configuration
DB_CONFIG = {
    "host": "127.0.0.1",
    "database": "pickup_football",
    "user": "postgres", 
    "password": "kingdoms",
    "port": 5432
}

def check_users():
    try:
        print("🔗 Connecting to pickup_football database...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get all users
        print("📋 All users in database:")
        cursor.execute("SELECT id, username, first_name, last_name, skill_level, is_active FROM users ORDER BY id;")
        users = cursor.fetchall()
        
        for user in users:
            status = "🟢" if user['is_active'] else "🔴"
            print(f"  {status} {user['username']} ({user['first_name']} {user['last_name']}) - Skill: {user['skill_level']}")
        
        # Check specifically for john_striker
        print("\n🔍 Checking for john_striker...")
        cursor.execute("SELECT username, first_name, last_name, is_active, password_hash FROM users WHERE username = %s;", ("john_striker",))
        john = cursor.fetchone()
        
        if john:
            print("✅ john_striker found!")
            print(f"   Name: {john['first_name']} {john['last_name']}")
            print(f"   Active: {john['is_active']}")
            print(f"   Has password: {'Yes' if john['password_hash'] else 'No'}")
        else:
            print("❌ john_striker not found!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_users()

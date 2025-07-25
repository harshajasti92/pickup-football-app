#!/usr/bin/env python3
"""
Fix all sample users' password hashes
"""
import bcrypt
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

def fix_all_passwords():
    try:
        print("🔗 Connecting to database...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get all users
        cursor.execute("SELECT id, username FROM users ORDER BY id;")
        users = cursor.fetchall()
        
        print(f"🔄 Fixing password hashes for {len(users)} users...")
        
        # Create a fresh hash for "test123"
        password = "test123"
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        hashed_str = hashed.decode('utf-8')
        
        print(f"🆕 Using hash: {hashed_str[:50]}...")
        
        for user in users:
            cursor.execute("""
                UPDATE users 
                SET password_hash = %s 
                WHERE id = %s
            """, (hashed_str, user['id']))
            
            print(f"  ✅ Updated {user['username']}")
        
        conn.commit()
        print(f"\n🎉 All {len(users)} users can now login with password 'test123'!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fix_all_passwords()

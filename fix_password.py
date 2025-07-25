#!/usr/bin/env python3
"""
Fix john_striker password hash
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

def fix_password():
    try:
        print("🔗 Connecting to database...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Create a fresh hash for "test123"
        password = "test123"
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        hashed_str = hashed.decode('utf-8')
        
        print(f"🔄 Creating new password hash for 'test123'...")
        print(f"🆕 New hash: {hashed_str[:50]}...")
        
        # Update john_striker's password
        cursor.execute("""
            UPDATE users 
            SET password_hash = %s 
            WHERE username = %s
        """, (hashed_str, "john_striker"))
        
        conn.commit()
        
        # Verify the update worked
        cursor.execute("SELECT username, password_hash FROM users WHERE username = %s;", ("john_striker",))
        user = cursor.fetchone()
        
        if user:
            print("✅ Password updated successfully!")
            
            # Test verification
            is_valid = bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8'))
            print(f"🧪 Verification test: {is_valid}")
            
            if is_valid:
                print("🎉 john_striker can now login with password 'test123'!")
            else:
                print("❌ Something still wrong with password verification")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fix_password()

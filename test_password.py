#!/usr/bin/env python3
"""
Test password verification directly
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

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def test_password_verification():
    try:
        print("🔗 Connecting to database...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get john_striker's password hash
        cursor.execute("SELECT username, password_hash FROM users WHERE username = %s;", ("john_striker",))
        user = cursor.fetchone()
        
        if user:
            print(f"✅ Found user: {user['username']}")
            print(f"🔑 Password hash: {user['password_hash'][:50]}...")
            
            # Test password verification
            test_password = "test123"
            print(f"🧪 Testing password: '{test_password}'")
            
            try:
                is_valid = verify_password(test_password, user['password_hash'])
                print(f"🎯 Password verification result: {is_valid}")
                
                if is_valid:
                    print("✅ Password verification PASSED!")
                else:
                    print("❌ Password verification FAILED!")
                    
                    # Let's try to create a new hash for test123 and compare
                    print("\n🔄 Creating new hash for 'test123'...")
                    new_hash = bcrypt.hashpw("test123".encode('utf-8'), bcrypt.gensalt())
                    print(f"🆕 New hash: {new_hash.decode('utf-8')[:50]}...")
                    
                    # Test the new hash
                    new_verify = verify_password("test123", new_hash.decode('utf-8'))
                    print(f"🧪 New hash verification: {new_verify}")
                    
            except Exception as e:
                print(f"❌ Password verification error: {e}")
        else:
            print("❌ User john_striker not found!")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    test_password_verification()

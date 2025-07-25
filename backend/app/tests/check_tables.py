#!/usr/bin/env python3
"""
Script to check what tables exist in the database
"""
import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection configuration
DB_CONFIG = {
    "host": "127.0.0.1",
    "database": "postgres",
    "user": "postgres", 
    "password": "kingdoms",
    "port": 5432
}

def check_tables():
    """Check what tables exist in the database"""
    conn = None
    try:
        print("Connecting to PostgreSQL database...")
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        
        print("✅ Database connection successful!")
        
        # Get all tables in the public schema
        cursor.execute("""
            SELECT table_name, table_type 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        print(f"\n📋 Tables in 'public' schema: {len(tables)} found")
        print("=" * 50)
        
        if tables:
            for table in tables:
                print(f"📁 {table['table_name']} ({table['table_type']})")
        else:
            print("📭 No tables found in the public schema")
            
        # Also check if users table specifically exists and get its structure
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'users'
            );
        """)
        users_table_exists = cursor.fetchone()['exists']
        
        print(f"\n🔍 Users table exists: {'✅ YES' if users_table_exists else '❌ NO'}")
        
        if users_table_exists:
            print("\n📊 Users table structure:")
            cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_schema = 'public' AND table_name = 'users' 
                ORDER BY ordinal_position;
            """)
            columns = cursor.fetchall()
            
            for col in columns:
                nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
                default = f" DEFAULT {col['column_default']}" if col['column_default'] else ""
                print(f"  📌 {col['column_name']} ({col['data_type']}) {nullable}{default}")
                
            # Check if there are any users
            cursor.execute("SELECT COUNT(*) as count FROM users;")
            user_count = cursor.fetchone()['count']
            print(f"\n👥 Number of users in table: {user_count}")
            
            if user_count > 0:
                print("\n📋 Recent users:")
                cursor.execute("""
                    SELECT id, username, first_name, last_name, created_at
                    FROM users 
                    ORDER BY created_at DESC 
                    LIMIT 5;
                """)
                recent_users = cursor.fetchall()
                for user in recent_users:
                    print(f"  🙋 ID: {user['id']}, Username: {user['username']}, Name: {user['first_name']} {user['last_name']}, Created: {user['created_at']}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print(f"Error type: {type(e).__name__}")
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    check_tables()

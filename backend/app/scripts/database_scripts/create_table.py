#!/usr/bin/env python3
"""
Script to create the users table
"""
import psycopg2
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

def create_users_table():
    """Create the users table"""
    conn = None
    try:
        print("Connecting to PostgreSQL database...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Read the SQL file
        sql_file_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "database", "01_create_users_table.sql")
        
        if not os.path.exists(sql_file_path):
            print(f"❌ SQL file not found: {sql_file_path}")
            return False
            
        with open(sql_file_path, 'r') as file:
            sql_content = file.read()
        
        print("Creating users table...")
        cursor.execute(sql_content)
        conn.commit()
        
        print("✅ Users table created successfully!")
        
        # Verify table was created
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'users';
        """)
        result = cursor.fetchone()
        
        if result:
            print("✅ Table 'users' confirmed in database")
            
            # Show table structure
            cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'users' 
                ORDER BY ordinal_position;
            """)
            columns = cursor.fetchall()
            
            print("\n📋 Table structure:")
            for col in columns:
                print(f"  - {col[0]} ({col[1]}) {'NULL' if col[2] == 'YES' else 'NOT NULL'}")
                
        return True
        
    except Exception as e:
        print(f"❌ Error creating table: {str(e)}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    success = create_users_table()
    if success:
        print("\n🎉 Database setup complete! You can now test user signup.")
    else:
        print("\n💥 Database setup failed!")
        sys.exit(1)

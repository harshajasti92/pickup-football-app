#!/usr/bin/env python3
"""
Script to create the user_preferences table
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

def create_user_preferences_table():
    """Create the user_preferences table"""
    conn = None
    try:
        print("🔗 Connecting to PostgreSQL database...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Check if users table exists (dependency)
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'users';
        """)
        users_exists = cursor.fetchone()
        
        if not users_exists:
            print("❌ Users table must exist first!")
            print("💡 Users table should have been created in the initial setup")
            return False
        
        # Read the SQL file
        sql_file_path = os.path.join(os.path.dirname(__file__), "..", "..", "database", "04_create_user_preferences_table.sql")
        
        if not os.path.exists(sql_file_path):
            print(f"❌ SQL file not found: {sql_file_path}")
            return False
            
        with open(sql_file_path, 'r') as file:
            sql_content = file.read()
        
        print("🚀 Creating user_preferences table...")
        cursor.execute(sql_content)
        conn.commit()
        
        print("✅ User preferences table created successfully!")
        
        # Verify table was created
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'user_preferences';
        """)
        result = cursor.fetchone()
        
        if result:
            print("✅ Table 'user_preferences' confirmed in database")
            
            # Show table structure
            cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'user_preferences' 
                ORDER BY ordinal_position;
            """)
            columns = cursor.fetchall()
            
            print("\n📊 User preferences table structure:")
            for col in columns:
                nullable = "NULL" if col[2] == 'YES' else "NOT NULL"
                default = f" DEFAULT {col[3]}" if col[3] else ""
                print(f"  📌 {col[0]} ({col[1]}) {nullable}{default}")
                
            # Show indexes
            cursor.execute("""
                SELECT indexname FROM pg_indexes 
                WHERE tablename = 'user_preferences' AND schemaname = 'public'
                ORDER BY indexname;
            """)
            indexes = cursor.fetchall()
            
            print(f"\n🔍 Indexes created: {len(indexes)}")
            for idx in indexes:
                print(f"  🔗 {idx[0]}")
                
            # Check if trigger was created for auto-creating preferences
            cursor.execute("""
                SELECT trigger_name, event_manipulation, event_object_table
                FROM information_schema.triggers 
                WHERE trigger_name = 'create_user_preferences_on_signup';
            """)
            trigger = cursor.fetchone()
            
            if trigger:
                print(f"\n⚡ Auto-trigger created: {trigger[0]}")
                print("  📝 Will automatically create default preferences for new users")
                
            # Test with existing users (create preferences for them)
            cursor.execute("SELECT id, first_name, last_name FROM users;")
            existing_users = cursor.fetchall()
            
            if existing_users:
                print(f"\n👥 Creating default preferences for {len(existing_users)} existing users:")
                for user in existing_users:
                    try:
                        cursor.execute("""
                            INSERT INTO user_preferences (
                                user_id, preferred_days, preferred_times, 
                                max_travel_distance, notifications_enabled, auto_join_skill_range
                            ) VALUES (%s, %s, %s, %s, %s, %s)
                            ON CONFLICT (user_id) DO NOTHING;
                        """, (
                            user[0],
                            ['tuesday', 'thursday', 'saturday'],
                            ['evening'],
                            15,
                            True,
                            [-2, 2]
                        ))
                        print(f"  ✅ {user[1]} {user[2]} (ID: {user[0]})")
                    except Exception as e:
                        print(f"  ⚠️  {user[1]} {user[2]} - {str(e)}")
                
                conn.commit()
                
        return True
        
    except Exception as e:
        print(f"❌ Error creating user_preferences table: {str(e)}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    print("⚙️  Creating User Preferences Table")
    print("=" * 45)
    
    success = create_user_preferences_table()
    if success:
        print("\n🎉 User preferences table setup complete!")
        print("✅ Ready to store user game preferences")
        print("🔄 Future user signups will automatically get default preferences")
    else:
        print("\n💥 User preferences table setup failed!")
        sys.exit(1)

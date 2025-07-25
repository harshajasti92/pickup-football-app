#!/usr/bin/env python3
"""
Script to create the game_participants table
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

def create_game_participants_table():
    """Create the game_participants table"""
    conn = None
    try:
        print("🔗 Connecting to PostgreSQL database...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Check if games table exists (dependency)
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'games';
        """)
        games_exists = cursor.fetchone()
        
        if not games_exists:
            print("❌ Games table must be created first!")
            print("💡 Run: python create_games_table.py")
            return False
        
        # Read the SQL file
        sql_file_path = os.path.join(os.path.dirname(__file__), "..", "..", "database", "03_create_game_participants_table.sql")
        
        if not os.path.exists(sql_file_path):
            print(f"❌ SQL file not found: {sql_file_path}")
            return False
            
        with open(sql_file_path, 'r') as file:
            sql_content = file.read()
        
        print("🚀 Creating game_participants table...")
        cursor.execute(sql_content)
        conn.commit()
        
        print("✅ Game participants table created successfully!")
        
        # Verify table was created
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'game_participants';
        """)
        result = cursor.fetchone()
        
        if result:
            print("✅ Table 'game_participants' confirmed in database")
            
            # Show table structure
            cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'game_participants' 
                ORDER BY ordinal_position;
            """)
            columns = cursor.fetchall()
            
            print("\n📊 Game participants table structure:")
            for col in columns:
                nullable = "NULL" if col[2] == 'YES' else "NOT NULL"
                default = f" DEFAULT {col[3]}" if col[3] else ""
                print(f"  📌 {col[0]} ({col[1]}) {nullable}{default}")
                
            # Show indexes
            cursor.execute("""
                SELECT indexname FROM pg_indexes 
                WHERE tablename = 'game_participants' AND schemaname = 'public'
                ORDER BY indexname;
            """)
            indexes = cursor.fetchall()
            
            print(f"\n🔍 Indexes created: {len(indexes)}")
            for idx in indexes:
                print(f"  🔗 {idx[0]}")
                
            # Show foreign key relationships
            cursor.execute("""
                SELECT 
                    conname,
                    pg_get_constraintdef(oid) as definition
                FROM pg_constraint 
                WHERE conrelid = 'game_participants'::regclass
                AND contype = 'f'
                ORDER BY conname;
            """)
            foreign_keys = cursor.fetchall()
            
            print(f"\n🔗 Foreign Key Relationships: {len(foreign_keys)}")
            for fk in foreign_keys:
                print(f"  🔑 {fk[0]}")
                
        return True
        
    except Exception as e:
        print(f"❌ Error creating game_participants table: {str(e)}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    print("👥 Creating Game Participants Table")
    print("=" * 45)
    
    success = create_game_participants_table()
    if success:
        print("\n🎉 Game participants table setup complete!")
        print("✅ Ready to track user participation in games")
    else:
        print("\n💥 Game participants table setup failed!")
        sys.exit(1)

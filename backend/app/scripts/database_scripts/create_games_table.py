#!/usr/bin/env python3
"""
Script to create the games table
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

def create_games_table():
    """Create the games table"""
    conn = None
    try:
        print("🔗 Connecting to PostgreSQL database...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Read the SQL file
        sql_file_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "database", "02_create_games_table.sql")
        
        if not os.path.exists(sql_file_path):
            print(f"❌ SQL file not found: {sql_file_path}")
            return False
            
        with open(sql_file_path, 'r') as file:
            sql_content = file.read()
        
        # Remove empty lines and split by statements
        sql_statements = []
        current_statement = ""
        in_do_block = False
        
        for line in sql_content.split('\n'):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('--'):
                continue
                
            # Check for DO block start/end
            if line.startswith('DO $$'):
                in_do_block = True
                current_statement += line + '\n'
            elif line == '$$;' and in_do_block:
                current_statement += line
                sql_statements.append(current_statement.strip())
                current_statement = ""
                in_do_block = False
            elif in_do_block:
                current_statement += line + '\n'
            else:
                current_statement += line + ' '
                
                # End of statement (semicolon not in DO block)
                if line.endswith(';'):
                    sql_statements.append(current_statement.strip())
                    current_statement = ""
        
        # Add any remaining statement
        if current_statement.strip():
            sql_statements.append(current_statement.strip())
        
        print("🚀 Creating games table...")
        
        # Execute each statement separately
        for i, statement in enumerate(sql_statements, 1):
            if statement:
                try:
                    print(f"  📝 Executing statement {i}...")
                    cursor.execute(statement)
                    conn.commit()
                except Exception as e:
                    print(f"  ❌ Error in statement {i}: {e}")
                    print(f"  Statement: {statement[:100]}...")
                    raise
        
        print("✅ Games table created successfully!")
        
        # Verify table was created
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'games';
        """)
        result = cursor.fetchone()
        
        if result:
            print("✅ Table 'games' confirmed in database")
            
            # Show table structure
            cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'games' 
                ORDER BY ordinal_position;
            """)
            columns = cursor.fetchall()
            
            print("\n📊 Games table structure:")
            for col in columns:
                nullable = "NULL" if col[2] == 'YES' else "NOT NULL"
                default = f" DEFAULT {col[3]}" if col[3] else ""
                print(f"  📌 {col[0]} ({col[1]}) {nullable}{default}")
                
            # Show indexes
            cursor.execute("""
                SELECT indexname FROM pg_indexes 
                WHERE tablename = 'games' AND schemaname = 'public'
                ORDER BY indexname;
            """)
            indexes = cursor.fetchall()
            
            print(f"\n🔍 Indexes created: {len(indexes)}")
            for idx in indexes:
                print(f"  🔗 {idx[0]}")
                
            # Show constraints
            cursor.execute("""
                SELECT conname, pg_get_constraintdef(oid) as definition
                FROM pg_constraint 
                WHERE conrelid = 'games'::regclass
                ORDER BY conname;
            """)
            constraints = cursor.fetchall()
            
            print(f"\n🛡️  Constraints: {len(constraints)}")
            for constraint in constraints:
                print(f"  🔒 {constraint[0]}")
                
        return True
        
    except Exception as e:
        print(f"❌ Error creating games table: {str(e)}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    print("🏈 Creating Games Table")
    print("=" * 40)
    
    success = create_games_table()
    if success:
        print("\n🎉 Games table setup complete!")
        print("✅ Ready to store game information")
    else:
        print("\n💥 Games table setup failed!")
        sys.exit(1)

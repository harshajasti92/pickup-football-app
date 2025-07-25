#!/usr/bin/env python3
"""
Script to add sample users data for testing
"""
import psycopg2
import sys
import os
from datetime import datetime, timezone

# Database connection configuration
DB_CONFIG = {
    "host": "127.0.0.1",
    "database": "pickup_football",
    "user": "postgres", 
    "password": "kingdoms",
    "port": 5432
}

def add_sample_users():
    """Add sample users to the users table"""
    conn = None
    try:
        print("🔗 Connecting to PostgreSQL database...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Sample users data
        sample_users = [
            {
                'username': 'john_striker',
                'password_hash': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/cVV8YyLee',  # password: "test123"
                'first_name': 'John',
                'last_name': 'Smith',
                'phone': '+1-555-0101',
                'age_range': '26-35',
                'bio': 'Passionate football player with 10+ years experience. Love playing striker position.',
                'skill_level': 8,
                'preferred_position': 'Forward',
                'playing_style': 'Aggressive',
                'is_active': True,
                'is_verified': True
            },
            {
                'username': 'sarah_keeper',
                'password_hash': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/cVV8YyLee',  # password: "test123"
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'phone': '+1-555-0102',
                'age_range': '18-25',
                'bio': 'Goalkeeper with great reflexes. Been playing since high school.',
                'skill_level': 7,
                'preferred_position': 'Goalkeeper',
                'playing_style': 'Technical',
                'is_active': True,
                'is_verified': True
            },
            {
                'username': 'mike_midfield',
                'password_hash': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/cVV8YyLee',  # password: "test123"
                'first_name': 'Mike',
                'last_name': 'Rodriguez',
                'phone': '+1-555-0103',
                'age_range': '26-35',
                'bio': 'Central midfielder who loves creating plays and assisting teammates.',
                'skill_level': 6,
                'preferred_position': 'Midfielder',
                'playing_style': 'Creative',
                'is_active': True,
                'is_verified': False
            },
            {
                'username': 'alex_defender',
                'password_hash': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/cVV8YyLee',  # password: "test123"
                'first_name': 'Alex',
                'last_name': 'Chen',
                'phone': '+1-555-0104',
                'age_range': '36-45',
                'bio': 'Solid defender with good positioning. Captain of my local team.',
                'skill_level': 9,
                'preferred_position': 'Defender',
                'playing_style': 'Physical',
                'is_active': True,
                'is_verified': True
            },
            {
                'username': 'emma_versatile',
                'password_hash': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/cVV8YyLee',  # password: "test123"
                'first_name': 'Emma',
                'last_name': 'Williams',
                'phone': '+1-555-0105',
                'age_range': '18-25',
                'bio': 'Flexible player who can adapt to any position. Just moved to the city.',
                'skill_level': 5,
                'preferred_position': 'Any',
                'playing_style': 'Balanced',
                'is_active': True,
                'is_verified': False
            },
            {
                'username': 'david_beginner',
                'password_hash': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/cVV8YyLee',  # password: "test123"
                'first_name': 'David',
                'last_name': 'Brown',
                'phone': '+1-555-0106',
                'age_range': '26-35',
                'bio': 'New to football but eager to learn and improve my skills.',
                'skill_level': 3,
                'preferred_position': 'Any',
                'playing_style': 'Balanced',
                'is_active': True,
                'is_verified': True
            }
        ]
        
        print("🚀 Adding sample users...")
        users_added = 0
        
        for user_data in sample_users:
            try:
                # Check if user already exists
                cursor.execute("SELECT id FROM users WHERE username = %s", (user_data['username'],))
                existing_user = cursor.fetchone()
                
                if existing_user:
                    print(f"  ⚠️  User '{user_data['username']}' already exists, skipping...")
                    continue
                
                # Insert new user
                cursor.execute("""
                    INSERT INTO users (
                        username, password_hash, first_name, last_name, phone, age_range,
                        bio, skill_level, preferred_position, playing_style, is_active, is_verified,
                        created_at, updated_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                """, (
                    user_data['username'],
                    user_data['password_hash'],
                    user_data['first_name'],
                    user_data['last_name'],
                    user_data['phone'],
                    user_data['age_range'],
                    user_data['bio'],
                    user_data['skill_level'],
                    user_data['preferred_position'],
                    user_data['playing_style'],
                    user_data['is_active'],
                    user_data['is_verified'],
                    datetime.now(timezone.utc),
                    datetime.now(timezone.utc)
                ))
                
                user_id = cursor.fetchone()[0]
                users_added += 1
                
                verified_status = "✅" if user_data['is_verified'] else "⏳"
                print(f"  {verified_status} Added: {user_data['first_name']} {user_data['last_name']} (@{user_data['username']}) - Skill: {user_data['skill_level']}/10")
                
            except Exception as e:
                print(f"  ❌ Error adding user '{user_data['username']}': {str(e)}")
                continue
        
        conn.commit()
        print(f"\n✅ Successfully added {users_added} sample users!")
        
        # Show current users in database
        cursor.execute("""
            SELECT id, username, first_name, last_name, skill_level, preferred_position, is_verified
            FROM users 
            ORDER BY id;
        """)
        all_users = cursor.fetchall()
        
        print(f"\n👥 Total users in database: {len(all_users)}")
        print("📋 Current users:")
        for user in all_users:
            verified_icon = "✅" if user[6] else "⏳"
            print(f"  {verified_icon} ID:{user[0]} - @{user[1]} ({user[2]} {user[3]}) - {user[4]}/10 - {user[5]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error adding sample users: {str(e)}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    print("👥 Adding Sample Users for Testing")
    print("=" * 40)
    
    success = add_sample_users()
    if success:
        print("\n🎉 Sample users setup complete!")
        print("🔐 All users have password: 'test123'")
        print("📱 You can now test login and game creation features")
    else:
        print("\n💥 Sample users setup failed!")
        sys.exit(1)

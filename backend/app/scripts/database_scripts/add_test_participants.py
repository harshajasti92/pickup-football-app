#!/usr/bin/env python3
"""
Script to add test participants to a specific game for waitlist testing
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

def add_test_participants():
    """Add participants to the reduced capacity game for waitlist testing"""
    conn = None
    try:
        print("🔗 Connecting to PostgreSQL database...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Find the game with reduced capacity (max_players = 3)
        cursor.execute("""
            SELECT id, title, max_players 
            FROM games 
            WHERE max_players = 3 AND title = 'Friday Evening Football'
            ORDER BY id ASC 
            LIMIT 1;
        """)
        target_game = cursor.fetchone()
        
        if not target_game:
            print("❌ No game found with 3 max players")
            return False
        
        game_id = target_game[0]
        print(f"✅ Found target game: {target_game[1]} (ID: {game_id}) - Max Players: {target_game[2]}")
        
        # Get available users
        cursor.execute("SELECT id, first_name, last_name FROM users ORDER BY id LIMIT 10;")
        users = cursor.fetchall()
        
        if len(users) < 6:
            print("❌ Need at least 6 users to test waitlist feature")
            return False
        
        print(f"✅ Found {len(users)} users available")
        
        # Clear any existing participants for this game
        cursor.execute("DELETE FROM game_participants WHERE game_id = %s", (game_id,))
        deleted_count = cursor.rowcount
        if deleted_count > 0:
            print(f"🧹 Cleared {deleted_count} existing participants")
        
        # Add participants - first 3 will be confirmed, rest will be waitlisted
        print("🚀 Adding test participants...")
        
        # Use unique users only (no duplicates)
        unique_participants = []
        used_users = set()
        
        for i, user in enumerate(users):
            if len(unique_participants) >= 6:  # 3 confirmed + 3 waitlisted
                break
                
            user_id = user[0]
            if user_id not in used_users:
                status = 'confirmed' if len(unique_participants) < 3 else 'waitlisted'
                positions = ['Midfielder', 'Goalkeeper', 'Forward', 'Defender', 'Any']
                position = positions[len(unique_participants) % len(positions)]
                
                unique_participants.append((game_id, user_id, status, position))
                used_users.add(user_id)
        
        # Insert participants
        participants_added = 0
        for participant_data in unique_participants:
            try:
                cursor.execute("""
                    INSERT INTO game_participants (game_id, user_id, status, position_preference, joined_at)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    participant_data[0],  # game_id
                    participant_data[1],  # user_id
                    participant_data[2],  # status
                    participant_data[3],  # position_preference
                    datetime.now(timezone.utc)
                ))
                
                participants_added += 1
                
                # Get user name
                user = next(u for u in users if u[0] == participant_data[1])
                user_name = f"{user[1]} {user[2]}"
                status_icon = "✅" if participant_data[2] == 'confirmed' else "⏰"
                
                print(f"  {status_icon} Added: {user_name} - {participant_data[2]} - {participant_data[3]}")
                
            except Exception as e:
                print(f"  ❌ Error adding participant: {str(e)}")
                continue
        
        conn.commit()
        print(f"\n✅ Successfully added {participants_added} participants!")
        
        # Show summary
        cursor.execute("""
            SELECT 
                gp.status,
                COUNT(*) as count,
                string_agg(u.first_name || ' ' || u.last_name, ', ' ORDER BY gp.joined_at) as names
            FROM game_participants gp
            JOIN users u ON gp.user_id = u.id
            WHERE gp.game_id = %s
            GROUP BY gp.status
            ORDER BY gp.status;
        """, (game_id,))
        
        status_summary = cursor.fetchall()
        
        print(f"\n📊 Game Participation Summary for '{target_game[1]}':")
        print(f"   Max Players: {target_game[2]}")
        
        for status_info in status_summary:
            status, count, names = status_info
            status_icon = "✅" if status == 'confirmed' else "⏰"
            print(f"   {status_icon} {status.title()}: {count} players")
            print(f"      {names}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error adding test participants: {str(e)}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    print("👥 Adding Test Participants for Waitlist Testing")
    print("=" * 50)
    
    success = add_test_participants()
    if success:
        print("\n🎉 Test participants setup complete!")
        print("🧪 You can now test the waitlist feature:")
        print("   • Try joining the 'Friday Evening Football' game")
        print("   • First 3 users should be confirmed")
        print("   • Additional users should be waitlisted")
        print("   • When someone leaves, waitlisted users should be promoted")
    else:
        print("\n💥 Test participants setup failed!")
        sys.exit(1)

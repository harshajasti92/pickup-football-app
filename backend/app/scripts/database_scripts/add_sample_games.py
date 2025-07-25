#!/usr/bin/env python3
"""
Script to add sample games data for testing
"""
import psycopg2
import sys
import os
from datetime import datetime, timezone, timedelta

# Database connection configuration
DB_CONFIG = {
    "host": "127.0.0.1",
    "database": "pickup_football",
    "user": "postgres", 
    "password": "kingdoms",
    "port": 5432
}

def add_sample_games():
    """Add sample games to the games table"""
    conn = None
    try:
        print("🔗 Connecting to PostgreSQL database...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Check if users exist (we need user IDs for created_by)
        cursor.execute("SELECT id, first_name, last_name FROM users ORDER BY id LIMIT 6;")
        users = cursor.fetchall()
        
        if not users:
            print("❌ No users found! Please create users first.")
            return False
        
        print(f"✅ Found {len(users)} users for game creation")
        
        # Generate sample games with various scenarios
        base_date = datetime.now(timezone.utc)
        
        sample_games = [
            {
                'title': 'Friday Evening Football',
                'description': 'Casual game for intermediate players. Good vibes and friendly competition!',
                'location': 'Central Park Field A',
                'date_time': base_date + timedelta(days=1, hours=18),
                'duration_minutes': 90,
                'max_players': 20,
                'skill_level_min': 5,
                'skill_level_max': 8,
                'created_by': users[0][0],  # John (skill 8)
                'status': 'open'
            },
            {
                'title': 'Sunday Morning Match',
                'description': 'Competitive game for skilled players. High intensity, great workout!',
                'location': 'Riverside Courts',
                'date_time': base_date + timedelta(days=3, hours=10),
                'duration_minutes': 90,
                'max_players': 16,
                'skill_level_min': 7,
                'skill_level_max': 10,
                'created_by': users[3][0],  # Alex (skill 9)
                'status': 'open'
            },
            {
                'title': 'Wednesday Pickup',
                'description': 'All skill levels welcome! Perfect for beginners and pros alike.',
                'location': 'Downtown Sports Complex',
                'date_time': base_date + timedelta(days=5, hours=19),
                'duration_minutes': 90,
                'max_players': 18,
                'skill_level_min': 1,
                'skill_level_max': 10,
                'created_by': users[4][0],  # Emma (skill 5)
                'status': 'open'
            },
            {
                'title': 'Saturday Morning Kickabout',
                'description': 'Relaxed game to start the weekend. Coffee and pastries after!',
                'location': 'Westside Park',
                'date_time': base_date + timedelta(days=2, hours=9),
                'duration_minutes': 75,
                'max_players': 14,
                'skill_level_min': 3,
                'skill_level_max': 7,
                'created_by': users[2][0],  # Mike (skill 6)
                'status': 'open'
            },
            {
                'title': 'Thursday Night Lights',
                'description': 'Under the floodlights! Fast-paced game for intermediate+ players.',
                'location': 'Municipal Stadium',
                'date_time': base_date + timedelta(days=6, hours=20),
                'duration_minutes': 60,
                'max_players': 22,
                'skill_level_min': 6,
                'skill_level_max': 9,
                'created_by': users[1][0],  # Sarah (skill 7)
                'status': 'open'
            },
            {
                'title': 'Beginners Welcome Game',
                'description': 'New to football? This is your game! Patient players and helpful tips.',
                'location': 'Community Center Field',
                'date_time': base_date + timedelta(days=4, hours=16),
                'duration_minutes': 90,
                'max_players': 16,
                'skill_level_min': 1,
                'skill_level_max': 5,
                'created_by': users[5][0],  # David (skill 3)
                'status': 'open'
            },
            {
                'title': 'Lunch Break Quick Game',
                'description': 'Short and sweet! Perfect for lunch break warriors.',
                'location': 'Office Park Field',
                'date_time': base_date + timedelta(days=1, hours=12),
                'duration_minutes': 45,
                'max_players': 12,
                'skill_level_min': 4,
                'skill_level_max': 8,
                'created_by': users[0][0],  # John
                'status': 'open'
            },
            {
                'title': 'Weekend Tournament Prep',
                'description': 'Practice match for upcoming tournament. Serious players only!',
                'location': 'Elite Training Ground',
                'date_time': base_date + timedelta(days=2, hours=15),
                'duration_minutes': 120,
                'max_players': 18,
                'skill_level_min': 8,
                'skill_level_max': 10,
                'created_by': users[3][0],  # Alex
                'status': 'open'
            },
            {
                'title': 'Mixed Skill Social Game',
                'description': 'Fun social game with mixed teams. BBQ afterwards!',
                'location': 'Lakeside Fields',
                'date_time': base_date + timedelta(days=7, hours=14),
                'duration_minutes': 90,
                'max_players': 20,
                'skill_level_min': 3,
                'skill_level_max': 9,
                'created_by': users[4][0],  # Emma
                'status': 'open'
            },
            {
                'title': 'Early Bird Special',
                'description': 'Early morning game for the dedicated! Coffee provided.',
                'location': 'Sunrise Park',
                'date_time': base_date + timedelta(days=1, hours=7),
                'duration_minutes': 75,
                'max_players': 14,
                'skill_level_min': 4,
                'skill_level_max': 8,
                'created_by': users[2][0],  # Mike
                'status': 'open'
            }
        ]
        
        print("🚀 Adding sample games...")
        games_added = 0
        
        for game_data in sample_games:
            try:
                # Check if game with same title and date already exists
                cursor.execute("""
                    SELECT id FROM games 
                    WHERE title = %s AND date_time = %s
                """, (game_data['title'], game_data['date_time']))
                existing_game = cursor.fetchone()
                
                if existing_game:
                    print(f"  ⚠️  Game '{game_data['title']}' already exists, skipping...")
                    continue
                
                # Insert new game
                cursor.execute("""
                    INSERT INTO games (
                        title, description, location, date_time, duration_minutes,
                        max_players, skill_level_min, skill_level_max, created_by, status,
                        created_at, updated_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                """, (
                    game_data['title'],
                    game_data['description'],
                    game_data['location'],
                    game_data['date_time'],
                    game_data['duration_minutes'],
                    game_data['max_players'],
                    game_data['skill_level_min'],
                    game_data['skill_level_max'],
                    game_data['created_by'],
                    game_data['status'],
                    datetime.now(timezone.utc),
                    datetime.now(timezone.utc)
                ))
                
                game_id = cursor.fetchone()[0]
                games_added += 1
                
                # Get creator name
                creator = next(u for u in users if u[0] == game_data['created_by'])
                creator_name = f"{creator[1]} {creator[2]}"
                
                # Format date for display
                game_date = game_data['date_time'].strftime("%m/%d %H:%M")
                skill_range = f"{game_data['skill_level_min']}-{game_data['skill_level_max']}"
                
                print(f"  ⚽ Added: '{game_data['title']}' - {game_date} - Skills:{skill_range} - by {creator_name}")
                
            except Exception as e:
                print(f"  ❌ Error adding game '{game_data['title']}': {str(e)}")
                continue
        
        conn.commit()
        print(f"\n✅ Successfully added {games_added} sample games!")
        
        # Show current games in database
        cursor.execute("""
            SELECT g.id, g.title, g.location, g.date_time, g.max_players, 
                   g.skill_level_min, g.skill_level_max, g.status,
                   u.first_name, u.last_name
            FROM games g
            JOIN users u ON g.created_by = u.id
            ORDER BY g.date_time;
        """)
        all_games = cursor.fetchall()
        
        print(f"\n🎮 Total games in database: {len(all_games)}")
        print("📋 Upcoming games:")
        for game in all_games:
            game_date = game[3].strftime("%m/%d %H:%M")
            skill_range = f"{game[5]}-{game[6]}"
            creator = f"{game[8]} {game[9]}"
            status_icon = "🟢" if game[7] == 'open' else "🔴"
            print(f"  {status_icon} ID:{game[0]} - {game[1]} @ {game[2]} - {game_date} - Skills:{skill_range} - by {creator}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error adding sample games: {str(e)}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    print("⚽ Adding Sample Games for Testing")
    print("=" * 40)
    
    success = add_sample_games()
    if success:
        print("\n🎉 Sample games setup complete!")
        print("🎮 You can now test game joining, team creation, and scheduling features")
        print("🗓️  Games span the next week with various skill levels and times")
    else:
        print("\n💥 Sample games setup failed!")
        sys.exit(1)

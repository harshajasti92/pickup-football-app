"""
Game-related business logic and database operations
"""
from fastapi import HTTPException
from datetime import datetime
from typing import Optional, List

from ..core import DatabaseManager
from ..models import (
    CreateGameRequest, JoinGameRequest, GameResponse, 
    ParticipantResponse, GameParticipantsResponse
)

class GameService:
    """Service class for game-related operations"""
    
    @staticmethod
    def create_game(game_data: CreateGameRequest, created_by: int) -> GameResponse:
        """Create a new game"""
        with DatabaseManager() as (cursor, conn):
            try:
                # Verify the creator exists and is active
                cursor.execute("""
                    SELECT id, first_name, last_name FROM users 
                    WHERE id = %s AND is_active = true
                """, (created_by,))
                creator = cursor.fetchone()
                
                if not creator:
                    raise HTTPException(status_code=404, detail="Creator user not found or inactive")
                
                # Validate skill level range
                if game_data.skill_level_min > game_data.skill_level_max:
                    raise HTTPException(status_code=400, detail="Minimum skill level cannot be higher than maximum")
                
                # Parse and validate datetime
                try:
                    datetime.fromisoformat(game_data.date_time.replace('Z', '+00:00'))
                except ValueError:
                    raise HTTPException(status_code=400, detail="Invalid datetime format. Use ISO format (e.g., 2024-01-01T18:00:00Z)")
                
                # Insert the new game
                cursor.execute("""
                    INSERT INTO games (
                        title, description, location, date_time, duration_minutes,
                        max_players, skill_level_min, skill_level_max, created_by
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id, title, description, location, date_time, duration_minutes,
                             max_players, skill_level_min, skill_level_max, status,
                             created_by, created_at, updated_at
                """, (
                    game_data.title, game_data.description, game_data.location,
                    game_data.date_time, game_data.duration_minutes, game_data.max_players,
                    game_data.skill_level_min, game_data.skill_level_max, created_by
                ))
                
                new_game = cursor.fetchone()
                
                return GameResponse(
                    id=new_game['id'],
                    title=new_game['title'],
                    description=new_game['description'],
                    location=new_game['location'],
                    date_time=str(new_game['date_time']),
                    duration_minutes=new_game['duration_minutes'],
                    max_players=new_game['max_players'],
                    skill_level_min=new_game['skill_level_min'],
                    skill_level_max=new_game['skill_level_max'],
                    status=new_game['status'],
                    created_by=new_game['created_by'],
                    creator_name=f"{creator['first_name']} {creator['last_name']}",
                    created_at=str(new_game['created_at']),
                    updated_at=str(new_game['updated_at']),
                    confirmed_players=0,
                    waitlisted_players=0,
                    user_status=None,
                    user_waitlist_position=None
                )
                
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to create game: {str(e)}")

    @staticmethod
    def get_games(
        status: Optional[str] = "open",
        skill_min: Optional[int] = None,
        skill_max: Optional[int] = None,
        limit: Optional[int] = 20,
        user_id: Optional[int] = None
    ) -> List[GameResponse]:
        """Get list of available games"""
        with DatabaseManager() as (cursor, conn):
            try:
                # Build query with optional filters
                query = """
                    SELECT g.id, g.title, g.description, g.location, g.date_time,
                           g.duration_minutes, g.max_players, g.skill_level_min, g.skill_level_max,
                           g.status, g.created_by, g.created_at, g.updated_at,
                           u.first_name, u.last_name,
                           (SELECT COUNT(*) FROM game_participants WHERE game_id = g.id AND status = 'confirmed') as confirmed_players,
                           (SELECT COUNT(*) FROM game_participants WHERE game_id = g.id AND status = 'waitlisted') as waitlisted_players
                    FROM games g
                    JOIN users u ON g.created_by = u.id
                """
                
                conditions = []
                params = []
                
                if status:
                    conditions.append("g.status = %s")
                    params.append(status)
                
                if skill_min is not None:
                    conditions.append("g.skill_level_max >= %s")
                    params.append(skill_min)
                    
                if skill_max is not None:
                    conditions.append("g.skill_level_min <= %s")
                    params.append(skill_max)
                
                if conditions:
                    query += " WHERE " + " AND ".join(conditions)
                
                query += " ORDER BY g.date_time ASC"
                
                if limit:
                    query += f" LIMIT {limit}"
                
                cursor.execute(query, params)
                games = cursor.fetchall()
                
                result = []
                for game in games:
                    # Check user's participation status if user_id provided
                    user_status = None
                    user_waitlist_position = None
                    
                    if user_id:
                        cursor.execute("""
                            SELECT status, joined_at FROM game_participants 
                            WHERE game_id = %s AND user_id = %s
                        """, (game['id'], user_id))
                        participation = cursor.fetchone()
                        
                        if participation:
                            user_status = participation['status']
                            
                            # Get waitlist position if waitlisted
                            if user_status == 'waitlisted':
                                cursor.execute("""
                                    SELECT COUNT(*) + 1 as position
                                    FROM game_participants 
                                    WHERE game_id = %s AND status = 'waitlisted' AND joined_at < %s
                                """, (game['id'], participation['joined_at']))
                                position_result = cursor.fetchone()
                                user_waitlist_position = position_result['position'] if position_result else None
                    
                    result.append(GameResponse(
                        id=game['id'],
                        title=game['title'],
                        description=game['description'],
                        location=game['location'],
                        date_time=str(game['date_time']),
                        duration_minutes=game['duration_minutes'],
                        max_players=game['max_players'],
                        skill_level_min=game['skill_level_min'],
                        skill_level_max=game['skill_level_max'],
                        status=game['status'],
                        created_by=game['created_by'],
                        creator_name=f"{game['first_name']} {game['last_name']}",
                        created_at=str(game['created_at']),
                        updated_at=str(game['updated_at']),
                        confirmed_players=game['confirmed_players'],
                        waitlisted_players=game['waitlisted_players'],
                        user_status=user_status,
                        user_waitlist_position=user_waitlist_position
                    ))
                
                return result
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to fetch games: {str(e)}")

    @staticmethod
    def join_game(game_id: int, request: JoinGameRequest, user_id: int) -> dict:
        """Join a game (confirmed or waitlisted based on availability)"""
        with DatabaseManager() as (cursor, conn):
            try:
                # Check if game exists and is open
                cursor.execute("""
                    SELECT id, title, max_players, status, skill_level_min, skill_level_max
                    FROM games WHERE id = %s
                """, (game_id,))
                game = cursor.fetchone()
                
                if not game:
                    raise HTTPException(status_code=404, detail="Game not found")
                
                if game['status'] != 'open':
                    raise HTTPException(status_code=400, detail="Game is not open for registration")
                
                # Check if user exists and get their skill level
                cursor.execute("""
                    SELECT id, skill_level FROM users WHERE id = %s AND is_active = true
                """, (user_id,))
                user = cursor.fetchone()
                
                if not user:
                    raise HTTPException(status_code=404, detail="User not found")
                
                # Check skill level compatibility
                if not (game['skill_level_min'] <= user['skill_level'] <= game['skill_level_max']):
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Your skill level ({user['skill_level']}) doesn't match game requirements ({game['skill_level_min']}-{game['skill_level_max']})"
                    )
                
                # Check if user is already in this game
                cursor.execute("""
                    SELECT status FROM game_participants 
                    WHERE game_id = %s AND user_id = %s
                """, (game_id, user_id))
                existing = cursor.fetchone()
                
                if existing:
                    raise HTTPException(status_code=400, detail=f"You are already {existing['status']} for this game")
                
                # Count confirmed players
                cursor.execute("""
                    SELECT COUNT(*) as confirmed_count 
                    FROM game_participants 
                    WHERE game_id = %s AND status = 'confirmed'
                """, (game_id,))
                confirmed_count = cursor.fetchone()['confirmed_count']
                
                # Determine status (confirmed or waitlisted)
                status = 'confirmed' if confirmed_count < game['max_players'] else 'waitlisted'
                
                # Insert participant
                cursor.execute("""
                    INSERT INTO game_participants (game_id, user_id, status, position_preference)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id, status, joined_at
                """, (game_id, user_id, status, request.position_preference))
                
                participant = cursor.fetchone()
                
                # Get waitlist position if waitlisted
                waitlist_position = None
                if status == 'waitlisted':
                    cursor.execute("""
                        SELECT COUNT(*) + 1 as position
                        FROM game_participants 
                        WHERE game_id = %s AND status = 'waitlisted' AND joined_at < %s
                    """, (game_id, participant['joined_at']))
                    waitlist_position = cursor.fetchone()['position']
                
                return {
                    "message": f"Successfully {'joined' if status == 'confirmed' else 'added to waitlist for'} {game['title']}",
                    "status": status,
                    "waitlist_position": waitlist_position,
                    "game_id": game_id,
                    "participant_id": participant['id']
                }
                
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to join game: {str(e)}")

    @staticmethod
    def leave_game(game_id: int, user_id: int) -> dict:
        """Leave a game"""
        with DatabaseManager() as (cursor, conn):
            try:
                # Check if user is in this game
                cursor.execute("""
                    SELECT gp.id, gp.status, g.title
                    FROM game_participants gp
                    JOIN games g ON gp.game_id = g.id
                    WHERE gp.game_id = %s AND gp.user_id = %s
                """, (game_id, user_id))
                
                participation = cursor.fetchone()
                if not participation:
                    raise HTTPException(status_code=404, detail="You are not registered for this game")
                
                # Delete the participation (trigger will handle waitlist promotion)
                cursor.execute("""
                    DELETE FROM game_participants 
                    WHERE game_id = %s AND user_id = %s
                """, (game_id, user_id))
                
                return {
                    "message": f"Successfully left {participation['title']}",
                    "game_id": game_id,
                    "previous_status": participation['status']
                }
                
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to leave game: {str(e)}")

    @staticmethod
    def get_game_participants(game_id: int) -> GameParticipantsResponse:
        """Get all participants for a game"""
        with DatabaseManager() as (cursor, conn):
            try:
                # Check if game exists
                cursor.execute("SELECT id FROM games WHERE id = %s", (game_id,))
                if not cursor.fetchone():
                    raise HTTPException(status_code=404, detail="Game not found")
                
                # Get all participants with user details
                cursor.execute("""
                    SELECT gp.id, gp.user_id, gp.status, gp.position_preference, gp.joined_at,
                           u.username, u.first_name, u.last_name, u.skill_level
                    FROM game_participants gp
                    JOIN users u ON gp.user_id = u.id
                    WHERE gp.game_id = %s
                    ORDER BY 
                        CASE WHEN gp.status = 'confirmed' THEN 1 
                             WHEN gp.status = 'waitlisted' THEN 2 
                             ELSE 3 END,
                        gp.joined_at ASC
                """, (game_id,))
                
                participants = cursor.fetchall()
                
                confirmed = []
                waitlisted = []
                
                for p in participants:
                    participant_data = ParticipantResponse(
                        id=p['id'],
                        user_id=p['user_id'],
                        username=p['username'],
                        first_name=p['first_name'],
                        last_name=p['last_name'],
                        skill_level=p['skill_level'],
                        status=p['status'],
                        position_preference=p['position_preference'],
                        joined_at=str(p['joined_at'])
                    )
                    
                    if p['status'] == 'confirmed':
                        confirmed.append(participant_data)
                    elif p['status'] == 'waitlisted':
                        waitlisted.append(participant_data)
                
                return GameParticipantsResponse(
                    game_id=game_id,
                    confirmed=confirmed,
                    waitlisted=waitlisted,
                    total_confirmed=len(confirmed),
                    total_waitlisted=len(waitlisted)
                )
                
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to fetch participants: {str(e)}")

    @staticmethod
    def get_user_games(user_id: int, status: Optional[str] = None) -> List[dict]:
        """Get games for a specific user"""
        with DatabaseManager() as (cursor, conn):
            try:
                # Check if user exists
                cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
                if not cursor.fetchone():
                    raise HTTPException(status_code=404, detail="User not found")
                
                # Build query
                query = """
                    SELECT g.id, g.title, g.description, g.location, g.date_time, g.duration_minutes,
                           g.max_players, g.skill_level_min, g.skill_level_max, g.status,
                           g.created_by, g.created_at, g.updated_at,
                           u.first_name, u.last_name,
                           gp.status as user_status, gp.position_preference, gp.joined_at
                    FROM games g
                    JOIN users u ON g.created_by = u.id
                    JOIN game_participants gp ON g.id = gp.game_id
                    WHERE gp.user_id = %s
                """
                
                params = [user_id]
                
                if status:
                    query += " AND gp.status = %s"
                    params.append(status)
                
                query += " ORDER BY g.date_time ASC"
                
                cursor.execute(query, params)
                user_games = cursor.fetchall()
                
                return [
                    {
                        "game": GameResponse(
                            id=game['id'],
                            title=game['title'],
                            description=game['description'],
                            location=game['location'],
                            date_time=str(game['date_time']),
                            duration_minutes=game['duration_minutes'],
                            max_players=game['max_players'],
                            skill_level_min=game['skill_level_min'],
                            skill_level_max=game['skill_level_max'],
                            status=game['status'],
                            created_by=game['created_by'],
                            creator_name=f"{game['first_name']} {game['last_name']}",
                            created_at=str(game['created_at']),
                            updated_at=str(game['updated_at'])
                        ),
                        "participation": {
                            "status": game['user_status'],
                            "position_preference": game['position_preference'],
                            "joined_at": str(game['joined_at'])
                        }
                    }
                    for game in user_games
                ]
                
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to fetch user games: {str(e)}")

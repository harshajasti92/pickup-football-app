from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
import psycopg2
from psycopg2.extras import RealDictCursor
import bcrypt
from typing import Optional, List
import os
import getpass

# Initialize FastAPI app
app = FastAPI(title="Pickup Football API", version="1.0.0")

# Add CORS middleware to allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection configuration
def get_db_password():
    """Get database password from environment or prompt user"""
    password = os.getenv("POSTGRES_PASSWORD")
    if not password:
        # For development, we'll use the actual password
        password = "kingdoms"  # Use the actual password for testing
    return password

DB_CONFIG = {
    "host": "127.0.0.1",  # Use IPv4 explicitly
    "database": os.getenv("POSTGRES_DATABASE", "pickup_football"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": get_db_password(),
    "port": int(os.getenv("POSTGRES_PORT", "5432"))
}

def get_db_connection():
    """Get database connection"""
    try:
        print(f"Attempting to connect with config: {DB_CONFIG}")  # Debug logging
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {str(e)}")  # Debug logging
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

# Pydantic models for request/response
class UserSignup(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    age_range: Optional[str] = None
    bio: Optional[str] = None
    skill_level: int = 5
    preferred_position: Optional[str] = None
    playing_style: Optional[str] = None

    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        if ' ' in v:
            raise ValueError('Username cannot contain spaces')
        return v

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

    @validator('skill_level')
    def validate_skill_level(cls, v):
        if v < 1 or v > 10:
            raise ValueError('Skill level must be between 1 and 10')
        return v

    @validator('age_range')
    def validate_age_range(cls, v):
        if v and v not in ['18-25', '26-35', '36-45', '46+']:
            raise ValueError('Invalid age range')
        return v

    @validator('preferred_position')
    def validate_preferred_position(cls, v):
        if v and v not in ['Goalkeeper', 'Defender', 'Midfielder', 'Forward', 'Any']:
            raise ValueError('Invalid preferred position')
        return v

    @validator('playing_style')
    def validate_playing_style(cls, v):
        if v and v not in ['Aggressive', 'Technical', 'Physical', 'Balanced', 'Creative', 'Defensive']:
            raise ValueError('Invalid playing style')
        return v

class UserLogin(BaseModel):
    username: str
    password: str

    @validator('username')
    def validate_username(cls, v):
        if not v.strip():
            raise ValueError('Username is required')
        return v.strip()

    @validator('password')
    def validate_password(cls, v):
        if not v:
            raise ValueError('Password is required')
        return v

class UserResponse(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    age_range: Optional[str]
    bio: Optional[str]
    skill_level: int
    preferred_position: Optional[str]
    playing_style: Optional[str]
    is_active: bool
    is_verified: bool
    created_at: str

class GameResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    location: str
    date_time: str
    duration_minutes: int
    max_players: int
    skill_level_min: int
    skill_level_max: int
    status: str
    created_by: int
    creator_name: str
    created_at: str
    updated_at: str
    # Enhanced fields for participant info
    confirmed_players: int = 0
    waitlisted_players: int = 0
    user_status: Optional[str] = None  # confirmed, waitlisted, declined, or None if not joined
    user_waitlist_position: Optional[int] = None

class ParticipantResponse(BaseModel):
    id: int
    user_id: int
    username: str
    first_name: str
    last_name: str
    skill_level: int
    status: str  # confirmed, waitlisted, declined
    position_preference: Optional[str]
    joined_at: str

class JoinGameRequest(BaseModel):
    position_preference: Optional[str] = None
    
    @validator('position_preference')
    def validate_position_preference(cls, v):
        if v and v not in ['Goalkeeper', 'Defender', 'Midfielder', 'Forward', 'Any']:
            raise ValueError('Invalid position preference')
        return v

class CreateGameRequest(BaseModel):
    title: str
    description: Optional[str] = None
    location: str
    date_time: str  # ISO format datetime string
    duration_minutes: int = 90
    max_players: int = 22
    skill_level_min: int = 1
    skill_level_max: int = 10
    
    @validator('title')
    def validate_title(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('Title must be at least 3 characters long')
        if len(v.strip()) > 100:
            raise ValueError('Title must be less than 100 characters')
        return v.strip()
    
    @validator('location')
    def validate_location(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('Location must be at least 3 characters long')
        if len(v.strip()) > 200:
            raise ValueError('Location must be less than 200 characters')
        return v.strip()
    
    @validator('duration_minutes')
    def validate_duration(cls, v):
        if v < 30 or v > 180:
            raise ValueError('Duration must be between 30 and 180 minutes')
        return v
    
    @validator('max_players')
    def validate_max_players(cls, v):
        if v < 4 or v > 30:
            raise ValueError('Max players must be between 4 and 30')
        return v
    
    @validator('skill_level_min', 'skill_level_max')
    def validate_skill_levels(cls, v):
        if v < 1 or v > 10:
            raise ValueError('Skill level must be between 1 and 10')
        return v

class GameParticipantsResponse(BaseModel):
    game_id: int
    confirmed: List[ParticipantResponse]
    waitlisted: List[ParticipantResponse]
    total_confirmed: int
    total_waitlisted: int

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Pickup Football API is running!", "version": "1.0.0"}

@app.post("/api/users/login", response_model=UserResponse)
async def login_user(login_data: UserLogin):
    """Authenticate user login"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get user by username
        cursor.execute("""
            SELECT id, username, password_hash, first_name, last_name, 
                   age_range, bio, skill_level, preferred_position, playing_style, 
                   is_active, is_verified, created_at
            FROM users 
            WHERE username = %s AND is_active = true
        """, (login_data.username,))
        
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Verify password
        if not verify_password(login_data.password, user['password_hash']):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Update last login timestamp
        cursor.execute("""
            UPDATE users 
            SET last_login = CURRENT_TIMESTAMP 
            WHERE id = %s
        """, (user['id'],))
        conn.commit()
        
        return UserResponse(
            id=user['id'],
            username=user['username'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            age_range=user['age_range'],
            bio=user['bio'],
            skill_level=user['skill_level'],
            preferred_position=user['preferred_position'],
            playing_style=user['playing_style'],
            is_active=user['is_active'],
            is_verified=user['is_verified'],
            created_at=str(user['created_at'])
        )
        
    except HTTPException:
        # Re-raise HTTPExceptions (401 errors)
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@app.post("/api/users/signup", response_model=UserResponse)
async def signup_user(user_data: UserSignup):
    """Create a new user account"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if username already exists
        cursor.execute("SELECT id FROM users WHERE username = %s", (user_data.username,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Username already exists")
        
        # Hash the password
        hashed_password = hash_password(user_data.password)
        
        # Insert new user
        insert_query = """
            INSERT INTO users (
                username, password_hash, first_name, last_name, 
                age_range, bio, skill_level, preferred_position, playing_style
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s
            ) RETURNING id, username, first_name, last_name, age_range, 
                       bio, skill_level, preferred_position, playing_style, 
                       is_active, is_verified, created_at
        """
        
        cursor.execute(insert_query, (
            user_data.username,
            hashed_password,
            user_data.first_name,
            user_data.last_name,
            user_data.age_range,
            user_data.bio,
            user_data.skill_level,
            user_data.preferred_position,
            user_data.playing_style
        ))
        
        new_user = cursor.fetchone()
        conn.commit()
        
        return UserResponse(
            id=new_user['id'],
            username=new_user['username'],
            first_name=new_user['first_name'],
            last_name=new_user['last_name'],
            age_range=new_user['age_range'],
            bio=new_user['bio'],
            skill_level=new_user['skill_level'],
            preferred_position=new_user['preferred_position'],
            playing_style=new_user['playing_style'],
            is_active=new_user['is_active'],
            is_verified=new_user['is_verified'],
            created_at=str(new_user['created_at'])
        )
        
    except psycopg2.IntegrityError as e:
        conn.rollback()
        if "username" in str(e):
            raise HTTPException(status_code=400, detail="Username already exists")
        else:
            raise HTTPException(status_code=400, detail="Data integrity error")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@app.get("/api/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Get user by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id, username, first_name, last_name, age_range, 
                   bio, skill_level, preferred_position, playing_style, 
                   is_active, is_verified, created_at
            FROM users WHERE id = %s AND is_active = true
        """, (user_id,))
        
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserResponse(
            id=user['id'],
            username=user['username'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            age_range=user['age_range'],
            bio=user['bio'],
            skill_level=user['skill_level'],
            preferred_position=user['preferred_position'],
            playing_style=user['playing_style'],
            is_active=user['is_active'],
            is_verified=user['is_verified'],
            created_at=str(user['created_at'])
        )
        
    finally:
        cursor.close()
        conn.close()

@app.post("/api/games", response_model=GameResponse)
async def create_game(game_data: CreateGameRequest, created_by: int):
    """Create a new game"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
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
        from datetime import datetime
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
        conn.commit()
        
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
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create game: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@app.get("/api/games", response_model=List[GameResponse])
async def get_games(
    status: Optional[str] = "open",
    skill_min: Optional[int] = None,
    skill_max: Optional[int] = None,
    limit: Optional[int] = 20,
    user_id: Optional[int] = None  # Add user_id to check participation status
):
    """Get list of available games"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
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
    finally:
        cursor.close()
        conn.close()

@app.post("/api/games/{game_id}/join")
async def join_game(game_id: int, request: JoinGameRequest, user_id: int):
    """Join a game (confirmed or waitlisted based on availability)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
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
        conn.commit()
        
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
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to join game: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@app.delete("/api/games/{game_id}/leave")
async def leave_game(game_id: int, user_id: int):
    """Leave a game"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
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
        
        conn.commit()
        
        return {
            "message": f"Successfully left {participation['title']}",
            "game_id": game_id,
            "previous_status": participation['status']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to leave game: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@app.get("/api/games/{game_id}/participants", response_model=GameParticipantsResponse)
async def get_game_participants(game_id: int):
    """Get all participants for a game"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
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
    finally:
        cursor.close()
        conn.close()

@app.get("/api/users/{user_id}/games")
async def get_user_games(user_id: int, status: Optional[str] = None):
    """Get games for a specific user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
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
    finally:
        cursor.close()
        conn.close()

@app.get("/api/health/db")
async def check_database():
    """Check database connection health"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        result = cursor.fetchone()
        user_count = result['count']  # Use column name instead of index when using RealDictCursor
        cursor.close()
        conn.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "total_users": user_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database health check failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

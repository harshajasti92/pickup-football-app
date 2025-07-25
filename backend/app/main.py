from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
import psycopg2
from psycopg2.extras import RealDictCursor
import bcrypt
from typing import Optional
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
    "database": os.getenv("POSTGRES_DATABASE", "postgres"),
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

@app.get("/api/health/db")
async def check_database():
    """Check database connection health"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
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

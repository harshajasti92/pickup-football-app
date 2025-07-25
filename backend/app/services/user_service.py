"""
User-related business logic and database operations
"""
from fastapi import HTTPException
import bcrypt
import psycopg2
from typing import Optional

from ..core import DatabaseManager
from ..models import UserSignup, UserLogin, UserResponse

class UserService:
    """Service class for user-related operations"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    @staticmethod
    def create_user(user_data: UserSignup) -> UserResponse:
        """Create a new user account"""
        with DatabaseManager() as (cursor, conn):
            try:
                # Check if username already exists
                cursor.execute("SELECT id FROM users WHERE username = %s", (user_data.username,))
                if cursor.fetchone():
                    raise HTTPException(status_code=400, detail="Username already exists")
                
                # Hash the password
                hashed_password = UserService.hash_password(user_data.password)
                
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
                if "username" in str(e):
                    raise HTTPException(status_code=400, detail="Username already exists")
                else:
                    raise HTTPException(status_code=400, detail="Data integrity error")
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")

    @staticmethod
    def authenticate_user(login_data: UserLogin) -> UserResponse:
        """Authenticate user login"""
        with DatabaseManager() as (cursor, conn):
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
                if not UserService.verify_password(login_data.password, user['password_hash']):
                    raise HTTPException(status_code=401, detail="Invalid credentials")
                
                # Update last login timestamp
                cursor.execute("""
                    UPDATE users 
                    SET last_login = CURRENT_TIMESTAMP 
                    WHERE id = %s
                """, (user['id'],))
                
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
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

    @staticmethod
    def get_user_by_id(user_id: int) -> UserResponse:
        """Get user by ID"""
        with DatabaseManager() as (cursor, conn):
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
                
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to fetch user: {str(e)}")

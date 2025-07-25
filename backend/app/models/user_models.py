"""
User-related Pydantic models for request/response validation
"""
from pydantic import BaseModel, validator
from typing import Optional

class UserSignup(BaseModel):
    """Model for user registration request"""
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
    """Model for user login request"""
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
    """Model for user data response"""
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

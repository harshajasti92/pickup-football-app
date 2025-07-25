"""
Game-related Pydantic models for request/response validation
"""
from pydantic import BaseModel, validator
from typing import Optional, List

class CreateGameRequest(BaseModel):
    """Model for game creation request"""
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

class JoinGameRequest(BaseModel):
    """Model for joining a game request"""
    position_preference: Optional[str] = None
    
    @validator('position_preference')
    def validate_position_preference(cls, v):
        if v and v not in ['Goalkeeper', 'Defender', 'Midfielder', 'Forward', 'Any']:
            raise ValueError('Invalid position preference')
        return v

class GameResponse(BaseModel):
    """Model for game data response"""
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
    """Model for game participant response"""
    id: int
    user_id: int
    username: str
    first_name: str
    last_name: str
    skill_level: int
    status: str  # confirmed, waitlisted, declined
    position_preference: Optional[str]
    joined_at: str

class GameParticipantsResponse(BaseModel):
    """Model for game participants list response"""
    game_id: int
    confirmed: List[ParticipantResponse]
    waitlisted: List[ParticipantResponse]
    total_confirmed: int
    total_waitlisted: int

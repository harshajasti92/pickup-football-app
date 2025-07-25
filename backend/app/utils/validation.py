"""
Validation utilities for data validation and formatting
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
import re

def validate_iso_datetime(date_string: str) -> bool:
    """Validate ISO format datetime string"""
    try:
        datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False

def validate_phone_number(phone: Optional[str]) -> bool:
    """Validate phone number format"""
    if not phone:
        return True
    
    # Basic phone validation pattern
    pattern = r'^\+?1?-?\(?[0-9]{3}\)?-?[0-9]{3}-?[0-9]{4}$'
    return bool(re.match(pattern, phone))

def validate_skill_level_range(min_level: int, max_level: int) -> bool:
    """Validate skill level range"""
    return (
        1 <= min_level <= 10 and
        1 <= max_level <= 10 and
        min_level <= max_level
    )

def sanitize_string(text: Optional[str], max_length: Optional[int] = None) -> Optional[str]:
    """Sanitize and clean string input"""
    if not text:
        return None
    
    # Remove extra whitespace
    cleaned = text.strip()
    
    # Truncate if necessary
    if max_length and len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    
    return cleaned if cleaned else None

def format_user_display_name(first_name: str, last_name: str) -> str:
    """Format user display name"""
    return f"{first_name} {last_name}".strip()

def calculate_age_range_from_birthdate(birthdate: datetime) -> str:
    """Calculate age range from birthdate"""
    today = datetime.now()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    
    if 18 <= age <= 25:
        return '18-25'
    elif 26 <= age <= 35:
        return '26-35'
    elif 36 <= age <= 45:
        return '36-45'
    else:
        return '46+'

class ValidationError(Exception):
    """Custom validation error"""
    pass

def validate_game_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate game creation data"""
    errors = []
    
    # Validate required fields
    if not data.get('title', '').strip():
        errors.append("Title is required")
    
    if not data.get('location', '').strip():
        errors.append("Location is required")
    
    if not data.get('date_time'):
        errors.append("Date and time are required")
    elif not validate_iso_datetime(data['date_time']):
        errors.append("Invalid date format")
    
    # Validate numeric fields
    duration = data.get('duration_minutes', 90)
    if not isinstance(duration, int) or duration < 30 or duration > 180:
        errors.append("Duration must be between 30 and 180 minutes")
    
    max_players = data.get('max_players', 22)
    if not isinstance(max_players, int) or max_players < 4 or max_players > 30:
        errors.append("Max players must be between 4 and 30")
    
    skill_min = data.get('skill_level_min', 1)
    skill_max = data.get('skill_level_max', 10)
    if not validate_skill_level_range(skill_min, skill_max):
        errors.append("Invalid skill level range")
    
    if errors:
        raise ValidationError("; ".join(errors))
    
    return data

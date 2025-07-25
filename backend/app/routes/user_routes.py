"""
User-related API endpoints
"""
from fastapi import APIRouter
from typing import Optional

from ..models import UserSignup, UserLogin, UserResponse
from ..services import UserService

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/signup", response_model=UserResponse)
async def signup_user(user_data: UserSignup):
    """Create a new user account"""
    return UserService.create_user(user_data)

@router.post("/login", response_model=UserResponse)
async def login_user(login_data: UserLogin):
    """Authenticate user login"""
    return UserService.authenticate_user(login_data)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Get user by ID"""
    return UserService.get_user_by_id(user_id)

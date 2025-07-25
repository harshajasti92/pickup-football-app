"""
Game-related API endpoints
"""
from fastapi import APIRouter, Query
from typing import Optional, List

from ..models import (
    CreateGameRequest, JoinGameRequest, GameResponse, 
    GameParticipantsResponse
)
from ..services import GameService

router = APIRouter(prefix="/api/games", tags=["games"])

@router.post("", response_model=GameResponse)
async def create_game(game_data: CreateGameRequest, created_by: int):
    """Create a new game"""
    return GameService.create_game(game_data, created_by)

@router.get("", response_model=List[GameResponse])
async def get_games(
    status: Optional[str] = Query("open", description="Filter by game status"),
    skill_min: Optional[int] = Query(None, description="Minimum skill level compatibility"),
    skill_max: Optional[int] = Query(None, description="Maximum skill level compatibility"),
    limit: Optional[int] = Query(20, description="Maximum number of results"),
    user_id: Optional[int] = Query(None, description="User ID to check participation status")
):
    """Get list of available games"""
    return GameService.get_games(status, skill_min, skill_max, limit, user_id)

@router.post("/{game_id}/join")
async def join_game(game_id: int, request: JoinGameRequest, user_id: int):
    """Join a game (confirmed or waitlisted based on availability)"""
    return GameService.join_game(game_id, request, user_id)

@router.delete("/{game_id}/leave")
async def leave_game(game_id: int, user_id: int):
    """Leave a game"""
    return GameService.leave_game(game_id, user_id)

@router.get("/{game_id}/participants", response_model=GameParticipantsResponse)
async def get_game_participants(game_id: int):
    """Get all participants for a game"""
    return GameService.get_game_participants(game_id)

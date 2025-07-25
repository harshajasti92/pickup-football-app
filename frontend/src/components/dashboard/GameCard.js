import React from 'react';
import './GameCard.css';

const GameCard = ({ game, onJoinGame, onLeaveGame, currentUser }) => {
  const formatDateTime = (dateTimeStr) => {
    const date = new Date(dateTimeStr);
    return {
      date: date.toLocaleDateString('en-US', { 
        weekday: 'short', 
        month: 'short', 
        day: 'numeric' 
      }),
      time: date.toLocaleTimeString('en-US', { 
        hour: 'numeric', 
        minute: '2-digit',
        hour12: true 
      })
    };
  };

  const getSkillLevelColor = (min, max) => {
    const avg = (min + max) / 2;
    if (avg <= 3) return '#4CAF50'; // Green for beginner
    if (avg <= 6) return '#FF9800'; // Orange for intermediate  
    return '#F44336'; // Red for advanced
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'open': return '🟢';
      case 'full': return '🔴';
      case 'cancelled': return '❌';
      case 'completed': return '✅';
      default: return '⚪';
    }
  };

  const canJoinGame = () => {
    if (game.status !== 'open') return false;
    if (game.created_by === currentUser?.id) return false;
    
    // Check if user's skill level fits the game requirements
    const userSkill = currentUser?.skill_level || 5;
    return userSkill >= game.skill_level_min && userSkill <= game.skill_level_max;
  };

  const { date, time } = formatDateTime(game.date_time);
  const skillColor = getSkillLevelColor(game.skill_level_min, game.skill_level_max);

  return (
    <div className="game-card">
      <div className="game-header">
        <div className="game-status">
          {getStatusIcon(game.status)}
          <span className="status-text">{game.status.toUpperCase()}</span>
        </div>
        <div className="game-skill-level" style={{ backgroundColor: skillColor }}>
          Skills: {game.skill_level_min}-{game.skill_level_max}
        </div>
      </div>

      <div className="game-main">
        <h3 className="game-title">{game.title}</h3>
        <p className="game-description">{game.description}</p>
        
        <div className="game-details">
          <div className="detail-item">
            <span className="detail-icon">📍</span>
            <span className="detail-text">{game.location}</span>
          </div>
          
          <div className="detail-item">
            <span className="detail-icon">📅</span>
            <span className="detail-text">{date}</span>
          </div>
          
          <div className="detail-item">
            <span className="detail-icon">⏰</span>
            <span className="detail-text">{time}</span>
          </div>
          
          <div className="detail-item">
            <span className="detail-icon">⏱️</span>
            <span className="detail-text">{game.duration_minutes} min</span>
          </div>
          
          <div className="detail-item">
            <span className="detail-icon">👥</span>
            <span className="detail-text">
              {game.confirmed_players || 0}/{game.max_players} players
              {game.waitlisted_players > 0 && ` (+${game.waitlisted_players} waitlisted)`}
            </span>
          </div>
          
          <div className="detail-item">
            <span className="detail-icon">👤</span>
            <span className="detail-text">Created by {game.creator_name}</span>
          </div>

          {/* Show user's participation status */}
          {game.user_status && (
            <div className="detail-item">
              <span className="detail-icon">
                {game.user_status === 'confirmed' ? '✅' : 
                 game.user_status === 'waitlisted' ? '⏳' : '❌'}
              </span>
              <span className="detail-text">
                You are {game.user_status}
                {game.user_status === 'waitlisted' && game.user_waitlist_position && 
                  ` (#${game.user_waitlist_position} in queue)`}
              </span>
            </div>
          )}
        </div>
      </div>

      <div className="game-actions">
        {game.created_by === currentUser?.id ? (
          <button className="game-btn owner-btn" disabled>
            Your Game
          </button>
        ) : game.user_status ? (
          // User is already participating - show leave button
          <button 
            className="game-btn leave-btn"
            onClick={() => onLeaveGame && onLeaveGame(game)}
            style={{ backgroundColor: '#ff6b6b', color: 'white' }}
          >
            Leave Game ({game.user_status}) 🚪
          </button>
        ) : canJoinGame() ? (
          <button 
            className="game-btn join-btn"
            onClick={() => onJoinGame(game)}
          >
            Join Game ⚽
          </button>
        ) : (
          <button className="game-btn disabled-btn" disabled>
            {game.status !== 'open' ? 'Game Closed' : 'Skill Level Mismatch'}
          </button>
        )}
      </div>
    </div>
  );
};

export default GameCard;

import React, { useState } from 'react';
import './CreateGameForm.css';

const CreateGameForm = ({ onClose, onGameCreated, currentUser }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    location: '',
    date: '',
    time: '',
    duration_minutes: 90,
    max_players: 22,
    skill_level_min: 1,
    skill_level_max: 10
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? parseInt(value) || 0 : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Validate required fields
      if (!formData.title.trim() || !formData.location.trim() || !formData.date || !formData.time) {
        throw new Error('Please fill in all required fields');
      }

      // Validate skill level range
      if (formData.skill_level_min > formData.skill_level_max) {
        throw new Error('Minimum skill level cannot be higher than maximum skill level');
      }

      // Combine date and time into ISO format
      const dateTime = `${formData.date}T${formData.time}:00Z`;

      // Validate datetime is in the future
      const gameDateTime = new Date(dateTime);
      if (gameDateTime <= new Date()) {
        throw new Error('Game date and time must be in the future');
      }

      const gameData = {
        title: formData.title.trim(),
        description: formData.description.trim() || null,
        location: formData.location.trim(),
        date_time: dateTime,
        duration_minutes: formData.duration_minutes,
        max_players: formData.max_players,
        skill_level_min: formData.skill_level_min,
        skill_level_max: formData.skill_level_max
      };

      const response = await fetch(
        `http://localhost:8000/api/games?created_by=${currentUser.id}`, 
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(gameData)
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to create game');
      }

      const newGame = await response.json();
      
      // Success! Call parent callback and close form
      onGameCreated(newGame);
      onClose();
      
    } catch (err) {
      console.error('Error creating game:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getTomorrowDate = () => {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    return tomorrow.toISOString().split('T')[0];
  };

  return (
    <div className="create-game-overlay">
      <div className="create-game-modal">
        <div className="create-game-header">
          <h2>⚽ Create New Game</h2>
          <button className="close-btn" onClick={onClose}>✖️</button>
        </div>

        <form onSubmit={handleSubmit} className="create-game-form">
          {/* Game Title */}
          <div className="form-group">
            <label htmlFor="title">Game Title *</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              placeholder="e.g., Friday Evening Football"
              maxLength="100"
              required
            />
          </div>

          {/* Description */}
          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Brief description of the game (optional)"
              rows="3"
              maxLength="500"
            />
          </div>

          {/* Location */}
          <div className="form-group">
            <label htmlFor="location">Location *</label>
            <input
              type="text"
              id="location"
              name="location"
              value={formData.location}
              onChange={handleChange}
              placeholder="e.g., Central Park Field A"
              maxLength="200"
              required
            />
          </div>

          {/* Date and Time */}
          <div className="form-group-row">
            <div className="form-group">
              <label htmlFor="date">Date *</label>
              <input
                type="date"
                id="date"
                name="date"
                value={formData.date}
                onChange={handleChange}
                min={getTomorrowDate()}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="time">Time *</label>
              <input
                type="time"
                id="time"
                name="time"
                value={formData.time}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          {/* Duration and Max Players */}
          <div className="form-group-row">
            <div className="form-group">
              <label htmlFor="duration_minutes">Duration (min)</label>
              <select
                id="duration_minutes"
                name="duration_minutes"
                value={formData.duration_minutes}
                onChange={handleChange}
              >
                <option value={60}>60 minutes</option>
                <option value={90}>90 minutes</option>
                <option value={120}>120 minutes</option>
              </select>
            </div>
            <div className="form-group">
              <label htmlFor="max_players">Max Players</label>
              <select
                id="max_players"
                name="max_players"
                value={formData.max_players}
                onChange={handleChange}
              >
                <option value={10}>10 players</option>
                <option value={14}>14 players</option>
                <option value={18}>18 players</option>
                <option value={22}>22 players</option>
                <option value={26}>26 players</option>
                <option value={30}>30 players</option>
              </select>
            </div>
          </div>

          {/* Skill Level Range */}
          <div className="form-group">
            <label>Skill Level Range</label>
            <div className="skill-range-container">
              <div className="skill-input">
                <label htmlFor="skill_level_min">Min</label>
                <select
                  id="skill_level_min"
                  name="skill_level_min"
                  value={formData.skill_level_min}
                  onChange={handleChange}
                >
                  {[1,2,3,4,5,6,7,8,9,10].map(level => (
                    <option key={level} value={level}>{level}</option>
                  ))}
                </select>
              </div>
              <span className="skill-divider">to</span>
              <div className="skill-input">
                <label htmlFor="skill_level_max">Max</label>
                <select
                  id="skill_level_max"
                  name="skill_level_max"
                  value={formData.skill_level_max}
                  onChange={handleChange}
                >
                  {[1,2,3,4,5,6,7,8,9,10].map(level => (
                    <option key={level} value={level}>{level}</option>
                  ))}
                </select>
              </div>
            </div>
            <small>Players with skill levels between {formData.skill_level_min} and {formData.skill_level_max} can join</small>
          </div>

          {/* Error Display */}
          {error && (
            <div className="error-message">
              <span className="error-icon">❌</span>
              {error}
            </div>
          )}

          {/* Form Actions */}
          <div className="form-actions">
            <button 
              type="button" 
              className="cancel-btn" 
              onClick={onClose}
              disabled={loading}
            >
              Cancel
            </button>
            <button 
              type="submit" 
              className="create-btn" 
              disabled={loading}
            >
              {loading ? 'Creating...' : 'Create Game'} ⚽
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateGameForm;

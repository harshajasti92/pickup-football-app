import React, { useState, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { getUserDisplayName } from '../../utils/auth';
import GameCard from './GameCard';
import CreateGameForm from './CreateGameForm';
import './Dashboard.css';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showCreateForm, setShowCreateForm] = useState(false);

  useEffect(() => {
    fetchGames();
  }, [user]); // Re-fetch when user changes // eslint-disable-line react-hooks/exhaustive-deps

  const fetchGames = async () => {
    try {
      setLoading(true);
      
      // Include user_id in the request to get participation status
      const url = user?.id 
        ? `http://localhost:8000/api/games?user_id=${user.id}`
        : 'http://localhost:8000/api/games';
      
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error('Failed to fetch games');
      }
      
      const gamesData = await response.json();
      setGames(gamesData);
      setError(null);
    } catch (err) {
      console.error('Error fetching games:', err);
      setError('Failed to load games. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const handleLeaveGame = async (game) => {
    if (!user?.id) {
      alert('Please log in to leave games');
      return;
    }

    if (!window.confirm(`Are you sure you want to leave "${game.title}"?`)) {
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/api/games/${game.id}/leave?user_id=${user.id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to leave game');
      }

      const result = await response.json();
      alert(result.message);
      
      // Refresh games list to show updated participant counts
      fetchGames();
      
    } catch (error) {
      console.error('Error leaving game:', error);
      alert(`Failed to leave game: ${error.message}`);
    }
  };

  const handleJoinGame = async (game) => {
    if (!user?.id) {
      alert('Please log in to join games');
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/api/games/${game.id}/join?user_id=${user.id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          position_preference: null // Could be enhanced with a position selector
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to join game');
      }

      const result = await response.json();
      
      // Show success message
      let message = result.message;
      if (result.status === 'waitlisted' && result.waitlist_position) {
        message += `\nYou are #${result.waitlist_position} on the waitlist.`;
      }
      
      alert(message);
      
      // Refresh games list to show updated participant counts
      fetchGames();
      
    } catch (error) {
      console.error('Error joining game:', error);
      alert(`Failed to join game: ${error.message}`);
    }
  };

  const handleLogout = () => {
    logout();
  };

  const handleCreateGame = () => {
    setShowCreateForm(true);
  };

  const handleCloseCreateForm = () => {
    setShowCreateForm(false);
  };

  const handleGameCreated = (newGame) => {
    // Add the new game to the beginning of the games list
    setGames(prevGames => [newGame, ...prevGames]);
    alert(`Game "${newGame.title}" created successfully!`);
  };

  return (
    <div className="dashboard">
      {/* Header Section - Placeholder */}
      <header className="dashboard-header">
        <div className="header-content">
          <div className="welcome-section">
            <h1>Welcome back, {user?.first_name || 'User'}! ⚽</h1>
            <p>Ready for your next game?</p>
          </div>
          <div className="header-actions">
            <button onClick={handleLogout} className="logout-btn">
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Main Dashboard Content */}
      <main className="dashboard-main">
        <div className="dashboard-container">
          
          {/* Quick Profile Summary Card - Placeholder */}
          <section className="profile-section">
            <div className="profile-card">
              <h2>👤 Your Player Profile</h2>
              <div className="profile-info">
                <p><strong>Name:</strong> {getUserDisplayName(user)}</p>
                <p><strong>Username:</strong> @{user?.username}</p>
                <p><strong>Skill Level:</strong> {user?.skill_level}/10</p>
                <p><strong>Position:</strong> {user?.preferred_position || 'Not set'}</p>
                <p><strong>Playing Style:</strong> {user?.playing_style || 'Not set'}</p>
                {user?.age_range && <p><strong>Age Range:</strong> {user.age_range}</p>}
              </div>
            </div>
          </section>

          {/* Upcoming Games Section */}
          <section className="games-section">
            <div className="games-card">
              <div className="games-header">
                <h2>⚽ Available Games</h2>
                <div className="games-header-actions">
                  <button className="create-game-btn-header" onClick={handleCreateGame}>
                    + Create Game
                  </button>
                  <button className="refresh-btn" onClick={fetchGames}>
                    🔄 Refresh
                  </button>
                </div>
              </div>
              
              {loading && (
                <div className="loading-state">
                  <div className="loading-spinner"></div>
                  <p>Loading games...</p>
                </div>
              )}
              
              {error && (
                <div className="error-state">
                  <div className="error-icon">❌</div>
                  <h3>Error Loading Games</h3>
                  <p>{error}</p>
                  <button className="retry-btn" onClick={fetchGames}>
                    Try Again
                  </button>
                </div>
              )}
              
              {!loading && !error && games.length === 0 && (
                <div className="empty-state">
                  <div className="empty-icon">🏈</div>
                  <h3>No games available</h3>
                  <p>Be the first to create a game!</p>
                  <button className="create-game-btn" onClick={handleCreateGame}>
                    + Create New Game
                  </button>
                </div>
              )}
              
              {!loading && !error && games.length > 0 && (
                <div className="games-list">
                  <div className="games-count">
                    <span>{games.length} games available</span>
                  </div>
                  {games.map(game => (
                    <GameCard
                      key={game.id}
                      game={game}
                      currentUser={user}
                      onJoinGame={handleJoinGame}
                      onLeaveGame={handleLeaveGame}
                    />
                  ))}
                </div>
              )}
            </div>
          </section>

        </div>
      </main>

      {/* Create Game Form Modal */}
      {showCreateForm && (
        <CreateGameForm
          onClose={handleCloseCreateForm}
          onGameCreated={handleGameCreated}
          currentUser={user}
        />
      )}
    </div>
  );
};

export default Dashboard;

import React, { useState, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { getUserDisplayName } from '../../utils/auth';
import GameCard from './GameCard';
import './Dashboard.css';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchGames();
  }, []);

  const fetchGames = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/api/games');
      
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

  const handleJoinGame = async (game) => {
    // TODO: Implement join game functionality
    alert(`Joining game: ${game.title}\nThis feature will be implemented next!`);
  };

  const handleLogout = () => {
    logout();
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
                <button className="refresh-btn" onClick={fetchGames}>
                  🔄 Refresh
                </button>
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
                  <button className="create-game-btn">
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
                    />
                  ))}
                </div>
              )}
            </div>
          </section>

        </div>
      </main>
    </div>
  );
};

export default Dashboard;

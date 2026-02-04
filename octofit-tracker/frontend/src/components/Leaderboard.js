import React, { useState, useEffect } from 'react';

const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboard/`;

  useEffect(() => {
    console.log('Leaderboard component - Fetching from API:', API_URL);
    
    fetch(API_URL)
      .then(response => {
        console.log('Leaderboard - Response status:', response.status);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Leaderboard - Raw data received:', data);
        // Handle both paginated (.results) and plain array responses
        const leaderboardData = data.results || data;
        console.log('Leaderboard - Processed data:', leaderboardData);
        setLeaderboard(Array.isArray(leaderboardData) ? leaderboardData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Leaderboard - Error fetching data:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [API_URL]);

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="loading-spinner">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3">Loading leaderboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-4">
        <div className="alert alert-danger" role="alert">
          <h4 className="alert-heading">Error!</h4>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="page-header">
        <h2>🏆 Leaderboard</h2>
        <p className="mb-0">See who's leading the fitness challenge</p>
      </div>

      <div className="table-responsive">
        <table className="table table-striped table-hover">
          <thead className="table-dark">
            <tr>
              <th style={{width: '10%'}}>Rank</th>
              <th style={{width: '25%'}}>Hero Name</th>
              <th style={{width: '20%'}}>Team</th>
              <th style={{width: '20%'}}>Total Calories</th>
              <th style={{width: '15%'}}>Activities</th>
              <th style={{width: '10%'}}>Points</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.length > 0 ? (
              leaderboard
                .filter(entry => entry.leaderboard_type === 'individual')
                .map((entry, index) => (
                <tr key={entry._id || index} className={entry.rank <= 3 ? 'table-warning' : ''}>
                  <td>
                    <h5 className="mb-0">
                      {entry.rank === 1 && '🥇'}
                      {entry.rank === 2 && '🥈'}
                      {entry.rank === 3 && '🥉'}
                      {entry.rank > 3 && `#${entry.rank}`}
                    </h5>
                  </td>
                  <td>
                    <strong>{entry.hero_name || entry.user_name || 'Unknown'}</strong>
                  </td>
                  <td>
                    {entry.team_name_display || entry.team_name || 'No Team'}
                  </td>
                  <td>
                    <span className="badge bg-danger">{entry.total_calories || 0} kcal</span>
                  </td>
                  <td>
                    <span className="badge bg-primary">{entry.activity_count || 0}</span>
                  </td>
                  <td>
                    <span className="badge bg-success">{entry.total_points || 0}</span>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="6" className="text-center text-muted py-4">
                  <p className="mb-0">No leaderboard data available</p>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Leaderboard;

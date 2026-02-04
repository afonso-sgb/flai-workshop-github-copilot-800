import React, { useState, useEffect } from 'react';

const Teams = () => {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/teams/`;

  useEffect(() => {
    console.log('Teams component - Fetching from API:', API_URL);
    
    fetch(API_URL)
      .then(response => {
        console.log('Teams - Response status:', response.status);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Teams - Raw data received:', data);
        // Handle both paginated (.results) and plain array responses
        const teamsData = data.results || data;
        console.log('Teams - Processed data:', teamsData);
        setTeams(Array.isArray(teamsData) ? teamsData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Teams - Error fetching data:', error);
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
          <p className="mt-3">Loading teams...</p>
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
        <h2>👥 Teams</h2>
        <p className="mb-0">Browse all fitness teams and their members</p>
      </div>

      <div className="row">
        {teams.length > 0 ? (
          teams.map((team, index) => (
            <div key={team._id || index} className="col-md-6 col-lg-4 mb-4">
              <div className="card h-100">
                <div className="card-header">
                  <h5 className="mb-0">{team.name}</h5>
                </div>
                <div className="card-body">
                  <p className="card-text">{team.description || 'No description available'}</p>
                  <hr />
                  <h6 className="mb-3">
                    <strong>Team Members ({team.members?.length || 0}):</strong>
                  </h6>
                  {team.members && team.members.length > 0 ? (
                    <ul className="list-group list-group-flush">
                      {team.members.map((member, idx) => (
                        <li key={idx} className="list-group-item px-0">
                          <span className="badge bg-primary me-2">👤</span>
                          <strong>{member.hero_name}</strong>
                          <br />
                          <small className="text-muted">{member.name}</small>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="text-muted text-center py-3">No members yet</p>
                  )}
                </div>
                <div className="card-footer">
                  <small className="text-muted">
                    📅 Created: {team.created_at ? new Date(team.created_at).toLocaleDateString('en-US', { 
                      year: 'numeric', 
                      month: 'short', 
                      day: 'numeric' 
                    }) : 'N/A'}
                  </small>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col-12">
            <div className="alert alert-info text-center" role="alert">
              <h5>No teams found</h5>
              <p className="mb-0">Create your first team to get started!</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Teams;

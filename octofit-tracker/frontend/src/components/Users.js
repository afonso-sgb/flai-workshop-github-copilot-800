import React, { useState, useEffect } from 'react';

const Users = () => {
  const [users, setUsers] = useState([]);
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingUser, setEditingUser] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    hero_name: '',
    team_id: ''
  });
  const [saving, setSaving] = useState(false);
  const [saveError, setSaveError] = useState(null);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/users/`;
  const TEAMS_API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/teams/`;

  useEffect(() => {
    console.log('Users component - Fetching from API:', API_URL);
    
    // Fetch users and teams
    Promise.all([
      fetch(API_URL).then(response => {
        console.log('Users - Response status:', response.status);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      }),
      fetch(TEAMS_API_URL).then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
    ])
      .then(([usersData, teamsData]) => {
        console.log('Users - Raw data received:', usersData);
        console.log('Teams - Raw data received:', teamsData);
        
        // Handle both paginated (.results) and plain array responses
        const usersArray = usersData.results || usersData;
        const teamsArray = teamsData.results || teamsData;
        
        console.log('Users - Processed data:', usersArray);
        console.log('Teams - Processed data:', teamsArray);
        
        setUsers(Array.isArray(usersArray) ? usersArray : []);
        setTeams(Array.isArray(teamsArray) ? teamsArray : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Users - Error fetching data:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [API_URL, TEAMS_API_URL]);

  const handleEdit = (user) => {
    setEditingUser(user._id);
    setFormData({
      name: user.name,
      email: user.email,
      hero_name: user.hero_name,
      team_id: user.team_id || ''
    });
    setSaveError(null);
  };

  const handleCancel = () => {
    setEditingUser(null);
    setFormData({
      name: '',
      email: '',
      hero_name: '',
      team_id: ''
    });
    setSaveError(null);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSave = async (userId) => {
    setSaving(true);
    setSaveError(null);

    try {
      const response = await fetch(`${API_URL}${userId}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to update user');
      }

      const updatedUser = await response.json();
      
      // Update the users list with the updated user
      setUsers(prevUsers => 
        prevUsers.map(user => 
          user._id === userId ? updatedUser : user
        )
      );

      setEditingUser(null);
      setFormData({
        name: '',
        email: '',
        hero_name: '',
        team_id: ''
      });
    } catch (error) {
      console.error('Error updating user:', error);
      setSaveError(error.message);
    } finally {
      setSaving(false);
    }
  };

  const getTeamName = (teamId) => {
    const team = teams.find(t => t._id === teamId);
    return team ? team.name : teamId;
  };

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="loading-spinner">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3">Loading users...</p>
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
        <h2>👥 Users</h2>
        <p className="mb-0">View and edit user profiles</p>
      </div>

      {saveError && (
        <div className="alert alert-danger alert-dismissible fade show" role="alert">
          <strong>Error:</strong> {saveError}
          <button 
            type="button" 
            className="btn-close" 
            onClick={() => setSaveError(null)}
            aria-label="Close"
          ></button>
        </div>
      )}

      <div className="table-responsive">
        <table className="table table-striped table-hover">
          <thead className="table-dark">
            <tr>
              <th>Name</th>
              <th>Hero Name</th>
              <th>Email</th>
              <th>Team</th>
              <th>Total Points</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.length > 0 ? (
              users.map((user, index) => (
                <tr key={user._id || index}>
                  {editingUser === user._id ? (
                    // Edit mode
                    <>
                      <td>
                        <input
                          type="text"
                          className="form-control form-control-sm"
                          name="name"
                          value={formData.name}
                          onChange={handleChange}
                          placeholder="Name"
                          disabled={saving}
                        />
                      </td>
                      <td>
                        <input
                          type="text"
                          className="form-control form-control-sm"
                          name="hero_name"
                          value={formData.hero_name}
                          onChange={handleChange}
                          placeholder="Hero Name"
                          disabled={saving}
                        />
                      </td>
                      <td>
                        <input
                          type="email"
                          className="form-control form-control-sm"
                          name="email"
                          value={formData.email}
                          onChange={handleChange}
                          placeholder="Email"
                          disabled={saving}
                        />
                      </td>
                      <td>
                        <select
                          className="form-select form-select-sm"
                          name="team_id"
                          value={formData.team_id}
                          onChange={handleChange}
                          disabled={saving}
                        >
                          <option value="">No Team</option>
                          {teams.map(team => (
                            <option key={team._id} value={team._id}>
                              {team.name}
                            </option>
                          ))}
                        </select>
                      </td>
                      <td>
                        <span className="badge bg-success">
                          {user.total_points || 0}
                        </span>
                      </td>
                      <td>
                        <button
                          className="btn btn-success btn-sm me-1"
                          onClick={() => handleSave(user._id)}
                          disabled={saving}
                        >
                          {saving ? 'Saving...' : '💾 Save'}
                        </button>
                        <button
                          className="btn btn-secondary btn-sm"
                          onClick={handleCancel}
                          disabled={saving}
                        >
                          ❌ Cancel
                        </button>
                      </td>
                    </>
                  ) : (
                    // View mode
                    <>
                      <td>
                        <strong>{user.name}</strong>
                      </td>
                      <td>{user.hero_name}</td>
                      <td>
                        <a href={`mailto:${user.email}`} className="text-decoration-none">
                          {user.email}
                        </a>
                      </td>
                      <td>
                        {user.team_id ? (
                          <span className="badge bg-primary">
                            {getTeamName(user.team_id)}
                          </span>
                        ) : (
                          <span className="badge bg-secondary">No Team</span>
                        )}
                      </td>
                      <td>
                        <span className="badge bg-success">
                          {user.total_points || 0}
                        </span>
                      </td>
                      <td>
                        <button
                          className="btn btn-primary btn-sm"
                          onClick={() => handleEdit(user)}
                          disabled={editingUser !== null}
                        >
                          ✏️ Edit
                        </button>
                      </td>
                    </>
                  )}
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="6" className="text-center text-muted py-4">
                  <p className="mb-0">No users found</p>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Users;

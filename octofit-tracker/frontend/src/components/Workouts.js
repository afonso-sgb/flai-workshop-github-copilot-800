import React, { useState, useEffect } from 'react';

const Workouts = () => {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;

  useEffect(() => {
    console.log('Workouts component - Fetching from API:', API_URL);
    
    fetch(API_URL)
      .then(response => {
        console.log('Workouts - Response status:', response.status);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Workouts - Raw data received:', data);
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        console.log('Workouts - Processed data:', workoutsData);
        setWorkouts(Array.isArray(workoutsData) ? workoutsData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Workouts - Error fetching data:', error);
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
          <p className="mt-3">Loading workouts...</p>
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
        <h2>💪 Workout Suggestions</h2>
        <p className="mb-0">Personalized workout recommendations to help you reach your goals</p>
      </div>

      <div className="row">
        {workouts.length > 0 ? (
          workouts.map((workout, index) => (
            <div key={workout._id || index} className="col-md-6 col-lg-4 mb-4">
              <div className="card h-100">
                <div className="card-header">
                  <h5 className="mb-0">{workout.name}</h5>
                  <small className="text-white-50">
                    {workout.type}
                  </small>
                </div>
                <div className="card-body">
                  <p className="card-text">{workout.description || 'No description available'}</p>
                  <hr />
                  <div className="d-flex justify-content-between align-items-center mb-2">
                    <span><strong>⏱️ Duration:</strong></span>
                    <span className="badge bg-info">{workout.duration_minutes || 0} min</span>
                  </div>
                  <div className="d-flex justify-content-between align-items-center mb-2">
                    <span><strong>📊 Difficulty:</strong></span>
                    <span className={`badge ${
                      workout.difficulty === 'easy' ? 'bg-success' :
                      workout.difficulty === 'medium' ? 'bg-warning text-dark' :
                      'bg-danger'
                    }`}>
                      {workout.difficulty ? workout.difficulty.toUpperCase() : 'N/A'}
                    </span>
                  </div>
                  <div className="d-flex justify-content-between align-items-center">
                    <span><strong>🔥 Calories:</strong></span>
                    <span className="badge bg-danger">{workout.calories_per_session || 0} kcal</span>
                  </div>
                </div>
                <div className="card-footer">
                  <small className="text-muted">
                    💪 {workout.type || 'General'} Workout
                  </small>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col-12">
            <div className="alert alert-info text-center" role="alert">
              <h5>No workout suggestions available</h5>
              <p className="mb-0">Check back soon for personalized recommendations!</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Workouts;

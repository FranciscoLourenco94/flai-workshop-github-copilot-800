import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;
    console.log('Workouts API URL:', apiUrl);
    
    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Workouts fetched data:', data);
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        setWorkouts(Array.isArray(workoutsData) ? workoutsData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching workouts:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="container mt-5">
        <div className="loading-container">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="container mt-5">
        <div className="alert alert-danger" role="alert">
          <h4 className="alert-heading">Error!</h4>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-5">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1 className="page-header">Personalized Workouts</h1>
          <p className="lead text-muted">Tailored fitness routines just for you</p>
        </div>
        <button className="btn btn-primary" disabled>
          <i className="bi bi-plus-lg"></i> Create Workout
        </button>
      </div>
      
      <div className="row">
        {workouts.length > 0 ? (
          workouts.map(workout => (
            <div key={workout.id} className="col-lg-6 col-md-12 mb-4">
              <div className="card h-100 border-0 shadow">
                <div className="card-header bg-primary text-white">
                  <h5 className="mb-0">{workout.name}</h5>
                </div>
                <div className="card-body">
                  <p className="card-text">{workout.description}</p>
                  <hr />
                  <div className="row g-3">
                    <div className="col-6">
                      <div className="d-flex align-items-center">
                        <i className="bi bi-clock me-2 text-primary"></i>
                        <div>
                          <small className="text-muted d-block">Duration</small>
                          <strong>{workout.duration} min</strong>
                        </div>
                      </div>
                    </div>
                    <div className="col-6">
                      <div className="d-flex align-items-center">
                        <i className="bi bi-speedometer2 me-2 text-primary"></i>
                        <div>
                          <small className="text-muted d-block">Difficulty</small>
                          <span className={`badge ${
                            workout.difficulty === 'Easy' ? 'bg-success' : 
                            workout.difficulty === 'Medium' ? 'bg-warning text-dark' : 
                            'bg-danger'
                          }`}>
                            {workout.difficulty}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="col-6">
                      <div className="d-flex align-items-center">
                        <i className="bi bi-tag me-2 text-primary"></i>
                        <div>
                          <small className="text-muted d-block">Category</small>
                          <strong>{workout.category}</strong>
                        </div>
                      </div>
                    </div>
                    {workout.user && (
                      <div className="col-6">
                        <div className="d-flex align-items-center">
                          <i className="bi bi-person me-2 text-primary"></i>
                          <div>
                            <small className="text-muted d-block">Assigned to</small>
                            <span className="badge bg-secondary">{workout.user}</span>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
                <div className="card-footer bg-light">
                  <div className="d-flex justify-content-between align-items-center">
                    <small className="text-muted">
                      Created: {new Date(workout.created_at).toLocaleDateString()}
                    </small>
                    <button className="btn btn-sm btn-outline-primary" disabled>
                      Start Workout
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col-12">
            <div className="alert alert-info" role="alert">
              <p className="mb-0 text-center">No workouts found. Create your personalized workout plan!</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Workouts;

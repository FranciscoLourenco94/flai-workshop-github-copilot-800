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

  if (loading) return <div className="container mt-4"><p>Loading workouts...</p></div>;
  if (error) return <div className="container mt-4"><p className="text-danger">Error: {error}</p></div>;

  return (
    <div className="container mt-4">
      <h2>Personalized Workouts</h2>
      <div className="row">
        {workouts.length > 0 ? (
          workouts.map(workout => (
            <div key={workout.id} className="col-md-6 mb-4">
              <div className="card h-100">
                <div className="card-header bg-primary text-white">
                  <h5 className="mb-0">{workout.name}</h5>
                </div>
                <div className="card-body">
                  <p className="card-text"><strong>Description:</strong> {workout.description}</p>
                  <p className="card-text"><strong>Duration:</strong> {workout.duration} minutes</p>
                  <p className="card-text"><strong>Difficulty:</strong> 
                    <span className={`badge ms-2 ${
                      workout.difficulty === 'Easy' ? 'bg-success' : 
                      workout.difficulty === 'Medium' ? 'bg-warning' : 
                      'bg-danger'
                    }`}>
                      {workout.difficulty}
                    </span>
                  </p>
                  <p className="card-text"><strong>Category:</strong> {workout.category}</p>
                  {workout.user && (
                    <p className="card-text">
                      <small className="text-muted">Assigned to: {workout.user}</small>
                    </p>
                  )}
                </div>
                <div className="card-footer">
                  <small className="text-muted">
                    Created: {new Date(workout.created_at).toLocaleDateString()}
                  </small>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col-12">
            <p className="text-center">No workouts found</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Workouts;

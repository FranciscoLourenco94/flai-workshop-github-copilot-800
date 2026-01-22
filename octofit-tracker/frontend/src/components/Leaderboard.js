import React, { useState, useEffect } from 'react';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboard/`;
    console.log('Leaderboard API URL:', apiUrl);
    
    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Leaderboard fetched data:', data);
        // Handle both paginated (.results) and plain array responses
        const leaderboardData = data.results || data;
        setLeaderboard(Array.isArray(leaderboardData) ? leaderboardData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching leaderboard:', error);
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
      <div className="mb-4">
        <h1 className="page-header">🏆 Leaderboard</h1>
        <p className="lead text-muted">Top performers by total points</p>
      </div>
      
      <div className="table-responsive">
        <table className="table table-striped table-hover align-middle">
          <thead className="table-dark">
            <tr>
              <th scope="col" className="text-center">Rank</th>
              <th scope="col">User</th>
              <th scope="col">Team</th>
              <th scope="col" className="text-center">Total Points</th>
              <th scope="col" className="text-center">Activities</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.length > 0 ? (
              leaderboard.map((entry, index) => {
                const rankBadge = index === 0 ? 'bg-warning text-dark' : 
                                 index === 1 ? 'bg-secondary' : 
                                 index === 2 ? 'bg-danger' : 'bg-light text-dark';
                return (
                  <tr key={entry.id}>
                    <td className="text-center">
                      <span className={`badge ${rankBadge} fs-6`}>
                        {index + 1}
                      </span>
                    </td>
                    <td>
                      <strong>{entry.user}</strong>
                    </td>
                    <td>
                      {entry.team ? (
                        <span className="badge bg-primary">{entry.team}</span>
                      ) : (
                        <span className="text-muted">N/A</span>
                      )}
                    </td>
                    <td className="text-center">
                      <span className="badge bg-success fs-6">{entry.total_points}</span>
                    </td>
                    <td className="text-center">
                      <span className="badge bg-info text-dark">{entry.activity_count}</span>
                    </td>
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan="5" className="text-center py-4">
                  <p className="text-muted mb-0">No leaderboard data available</p>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Leaderboard;

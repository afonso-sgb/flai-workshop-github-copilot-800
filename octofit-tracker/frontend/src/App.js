import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Teams from './components/Teams';
import Users from './components/Users';
import Workouts from './components/Workouts';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
          <div className="container-fluid">
            <Link className="navbar-brand" to="/">
              <img src="/octofitapp-small.png" alt="OctoFit Logo" />
              <strong>OctoFit Tracker</strong>
            </Link>
            <button
              className="navbar-toggler"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#navbarNav"
              aria-controls="navbarNav"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav ms-auto">
                <li className="nav-item">
                  <Link className="nav-link" to="/users">Users</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/activities">Activities</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/teams">Teams</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/leaderboard">Leaderboard</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/workouts">Workouts</Link>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        <main>
          <Routes>
            <Route path="/" element={
              <div className="container mt-5">
                <div className="welcome-section">
                  <h1 className="display-3 mb-4">Welcome to OctoFit Tracker 🏋️</h1>
                  <p className="lead">
                    Track your fitness activities, compete with your team, and achieve your goals!
                  </p>
                  <hr className="my-4" />
                  <div className="row mt-5">
                    <div className="col-md-4 mb-4">
                      <Link to="/users" className="text-decoration-none">
                        <div className="card text-center h-100 card-hover">
                          <div className="card-body">
                            <h2 className="display-1">👥</h2>
                            <h5 className="card-title">Users</h5>
                            <p className="card-text">View all registered users and their profiles</p>
                          </div>
                        </div>
                      </Link>
                    </div>
                    <div className="col-md-4 mb-4">
                      <Link to="/activities" className="text-decoration-none">
                        <div className="card text-center h-100 card-hover">
                          <div className="card-body">
                            <h2 className="display-1">🏃</h2>
                            <h5 className="card-title">Activities</h5>
                            <p className="card-text">Log your workouts and monitor your progress</p>
                          </div>
                        </div>
                      </Link>
                    </div>
                    <div className="col-md-4 mb-4">
                      <Link to="/leaderboard" className="text-decoration-none">
                        <div className="card text-center h-100 card-hover">
                          <div className="card-body">
                            <h2 className="display-1">🏆</h2>
                            <h5 className="card-title">Leaderboard</h5>
                            <p className="card-text">Challenge your friends on the leaderboard</p>
                          </div>
                        </div>
                      </Link>
                    </div>
                  </div>
                  <div className="row">
                    <div className="col-md-6 mb-4">
                      <Link to="/teams" className="text-decoration-none">
                        <div className="card text-center h-100 card-hover">
                          <div className="card-body">
                            <h2 className="display-1">👥</h2>
                            <h5 className="card-title">Teams</h5>
                            <p className="card-text">Browse all fitness teams and their members</p>
                          </div>
                        </div>
                      </Link>
                    </div>
                    <div className="col-md-6 mb-4">
                      <Link to="/workouts" className="text-decoration-none">
                        <div className="card text-center h-100 card-hover">
                          <div className="card-body">
                            <h2 className="display-1">💪</h2>
                            <h5 className="card-title">Workouts</h5>
                            <p className="card-text">Follow personalized workout suggestions</p>
                          </div>
                        </div>
                      </Link>
                    </div>
                  </div>
                </div>
              </div>
            } />
            <Route path="/users" element={<Users />} />
            <Route path="/activities" element={<Activities />} />
            <Route path="/teams" element={<Teams />} />
            <Route path="/leaderboard" element={<Leaderboard />} />
            <Route path="/workouts" element={<Workouts />} />
          </Routes>
        </main>

        <footer className="mt-5 py-3 bg-light text-center">
          <div className="container">
            <p className="text-muted mb-0">© 2026 OctoFit Tracker - Stay Fit, Stay Active!</p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;

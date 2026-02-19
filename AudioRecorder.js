import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Navbar.css';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          <span className="brand-icon">🐦</span>
          <span className="brand-text">Bird Recognition</span>
        </Link>

        <div className="navbar-links">
          {user ? (
            <>
              <Link to="/" className="nav-link">Identify</Link>
              <Link to="/history" className="nav-link">History</Link>
              <div className="nav-user">
                <span className="user-name">{user.username}</span>
                <button onClick={handleLogout} className="nav-logout">
                  Sign Out
                </button>
              </div>
            </>
          ) : (
            <>
              <Link to="/login" className="nav-link">Sign In</Link>
              <Link to="/register" className="nav-button">Sign Up</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;


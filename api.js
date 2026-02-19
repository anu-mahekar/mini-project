import React, { useState, useEffect } from 'react';
import { getHistory } from '../services/api';
import './History.css';

const History = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      setLoading(true);
      const data = await getHistory();
      setHistory(data.results || []);
    } catch (err) {
      setError(err.message || 'Failed to load history');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return (
      <div className="history-container">
        <div className="history-loading">
          <div className="spinner"></div>
          <p>Loading history...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="history-container">
        <div className="history-error">
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="history-container">
      <div className="history-header">
        <h1>Prediction History</h1>
        <p>{history.length} {history.length === 1 ? 'prediction' : 'predictions'}</p>
      </div>

      {history.length === 0 ? (
        <div className="history-empty">
          <div className="empty-icon">📭</div>
          <h2>No predictions yet</h2>
          <p>Your prediction history will appear here</p>
        </div>
      ) : (
        <div className="history-list">
          {history.map((item) => (
            <div key={item.id} className="history-item">
              <div className="history-item-header">
                <div className="history-item-title">
                  <h3>{item.predicted_label || 'Unknown'}</h3>
                  {item.bird?.english_cname && (
                    <span className="history-item-subtitle">{item.bird.english_cname}</span>
                  )}
                </div>
                <div className="history-item-meta">
                  <span className="history-date">{formatDate(item.created_at)}</span>
                  <span className="history-confidence">
                    {(item.confidence * 100).toFixed(1)}%
                  </span>
                </div>
              </div>

              {item.bird && (
                <div className="history-item-details">
                  <div className="history-detail-row">
                    <span className="detail-label">Scientific Name:</span>
                    <span className="detail-value">{item.bird.binomial}</span>
                  </div>
                  {item.bird.habitat && (
                    <div className="history-detail-row">
                      <span className="detail-label">Habitat:</span>
                      <span className="detail-value">{item.bird.habitat}</span>
                    </div>
                  )}
                </div>
              )}

              <div className="history-item-footer">
                <span className="history-filename">{item.filename}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default History;


import React, { useState } from 'react';
import './ResultDisplay.css';

const ResultDisplay = ({ result, onReset }) => {
  // result structure: { prediction: {...}, bird: {...}, ambiguous: false }
  const prediction = result?.prediction;
  const bird = result?.bird;
  const ambiguous = result?.ambiguous;
  
  const speciesName = prediction?.label || 'Unknown';
  const confidence = prediction?.confidence ? (prediction.confidence * 100).toFixed(1) : 'N/A';
  const votes = prediction?.votes || {};
  const [selectedImage, setSelectedImage] = useState(null);

  // Collect all images with credits
  const images = [];
  if (bird) {
    if (bird.image_url_1) images.push({ url: bird.image_url_1, credit: bird.image_credit_1 || 'Unknown' });
    if (bird.image_url_2) images.push({ url: bird.image_url_2, credit: bird.image_credit_2 || 'Unknown' });
    if (bird.image_url_3) images.push({ url: bird.image_url_3, credit: bird.image_credit_3 || 'Unknown' });
  }

  return (
    <div className="result-display">
      {/* Hero Section */}
      <div className="result-hero">
        <div className="hero-content">
          <div className="success-badge">
            <span className="success-icon">✓</span>
            <span>Identification Complete</span>
          </div>
          <h1 className="hero-title">
            {bird?.english_cname || speciesName}
          </h1>
          <p className="hero-subtitle">{bird?.binomial || speciesName}</p>
          <div className="confidence-badge">
            <span className="confidence-label">Confidence</span>
            <span className="confidence-value">{confidence}%</span>
          </div>
          {ambiguous && (
            <div className="warning-badge">
              <span>⚠️</span>
              <span>Species name may be ambiguous</span>
            </div>
          )}
        </div>
      </div>

      {/* Prediction Stats */}
      {prediction && (
        <div className="stats-card">
          <div className="stat-item">
            <div className="stat-value">{prediction.windows || 0}</div>
            <div className="stat-label">Audio Windows</div>
          </div>
          <div className="stat-divider"></div>
          <div className="stat-item">
            <div className="stat-value">{confidence}%</div>
            <div className="stat-label">Confidence</div>
          </div>
          {Object.keys(votes).length > 0 && (
            <>
              <div className="stat-divider"></div>
              <div className="stat-item">
                <div className="stat-value">{Object.keys(votes).length}</div>
                <div className="stat-label">Top Predictions</div>
              </div>
            </>
          )}
        </div>
      )}

      {/* Top Predictions */}
      {Object.keys(votes).length > 0 && (
        <div className="predictions-card">
          <h3 className="card-title">
            <span className="card-icon">🎯</span>
            Top Predictions
          </h3>
          <div className="predictions-list">
            {Object.entries(votes).slice(0, 5).map(([species, count], index) => (
              <div key={species} className={`prediction-item ${index === 0 ? 'top-prediction' : ''}`}>
                <div className="prediction-rank">#{index + 1}</div>
                <div className="prediction-info">
                  <div className="prediction-species">{species}</div>
                  <div className="prediction-votes">{count} {count === 1 ? 'vote' : 'votes'}</div>
                </div>
                {index === 0 && <div className="top-badge">Top</div>}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Bird Information */}
      {bird ? (
        <div className="bird-info-section">
          {/* Images Gallery */}
          {images.length > 0 && (
            <div className="images-card">
              <h3 className="card-title">
                <span className="card-icon">🖼️</span>
                Gallery
              </h3>
              <div className="image-gallery">
                {images.map((img, index) => (
                  <div 
                    key={index} 
                    className="image-card"
                    onClick={() => setSelectedImage(img)}
                  >
                    <div className="image-wrapper">
                      <img 
                        src={img.url} 
                        alt={bird.binomial || speciesName}
                        className="gallery-image"
                        loading="lazy"
                      />
                      <div className="image-overlay">
                        <span className="view-icon">👁️</span>
                      </div>
                    </div>
                    {img.credit && (
                      <div className="image-credit">
                        <span className="credit-icon">📷</span>
                        <span className="credit-text">{img.credit}</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Information Cards */}
          <div className="info-cards-grid">
            {/* Basic Info */}
            <div className="info-card">
              <div className="card-header">
                <span className="card-icon">📋</span>
                <h3>Basic Information</h3>
              </div>
              <div className="card-content">
                <div className="info-row">
                  <span className="info-label">Scientific Name</span>
                  <span className="info-value">{bird.binomial || 'N/A'}</span>
                </div>
                {bird.genus && (
                  <div className="info-row">
                    <span className="info-label">Genus</span>
                    <span className="info-value">{bird.genus}</span>
                  </div>
                )}
                {bird.species && (
                  <div className="info-row">
                    <span className="info-label">Species</span>
                    <span className="info-value">{bird.species}</span>
                  </div>
                )}
                {bird.english_cname && (
                  <div className="info-row">
                    <span className="info-label">Common Name</span>
                    <span className="info-value">{bird.english_cname}</span>
                  </div>
                )}
                {bird.wikipedia_url && (
                  <div className="info-row">
                    <span className="info-label">Learn More</span>
                    <a 
                      href={bird.wikipedia_url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="wikipedia-link"
                    >
                      <span>Wikipedia</span>
                      <span className="external-icon">↗</span>
                    </a>
                  </div>
                )}
              </div>
            </div>

            {/* Habitat */}
            {bird.habitat && (
              <div className="info-card habitat-card">
                <div className="card-header">
                  <span className="card-icon">🌳</span>
                  <h3>Habitat</h3>
                </div>
                <div className="card-content">
                  <p className="info-text">{bird.habitat}</p>
                </div>
              </div>
            )}

            {/* Diet */}
            {bird.diet && (
              <div className="info-card diet-card">
                <div className="card-header">
                  <span className="card-icon">🍽️</span>
                  <h3>Diet</h3>
                </div>
                <div className="card-content">
                  <p className="info-text">{bird.diet}</p>
                </div>
              </div>
            )}

            {/* Notes/Description */}
            {bird.notes && (
              <div className="info-card notes-card full-width">
                <div className="card-header">
                  <span className="card-icon">📝</span>
                  <h3>About</h3>
                </div>
                <div className="card-content">
                  <p className="info-text">{bird.notes}</p>
                </div>
              </div>
            )}
          </div>
        </div>
      ) : (
        <div className="no-details-card">
          <div className="no-details-icon">🔍</div>
          <h3>No Bird Details Found</h3>
          <p>
            {prediction ? 
              'The prediction was successful, but no matching bird was found in the database.' : 
              'Prediction result is not available.'}
          </p>
        </div>
      )}

      {/* Image Modal */}
      {selectedImage && (
        <div className="image-modal" onClick={() => setSelectedImage(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setSelectedImage(null)}>×</button>
            <img src={selectedImage.url} alt={bird?.binomial || speciesName} className="modal-image" />
            {selectedImage.credit && (
              <div className="modal-credit">
                <span className="credit-icon">📷</span>
                <span>{selectedImage.credit}</span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Action Button */}
      <div className="result-actions">
        <button className="reset-button" onClick={onReset}>
          <span className="button-icon">🔄</span>
          <span>Analyze Another Audio</span>
        </button>
      </div>
    </div>
  );
};

export default ResultDisplay;

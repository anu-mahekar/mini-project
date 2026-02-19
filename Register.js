import React, { useState, useRef } from 'react';
import './FileUpload.css';

const FileUpload = ({ onAudioSubmit, loading }) => {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (file) => {
    // Check if file is an audio file
    if (!file.type.startsWith('audio/')) {
      alert('Please select an audio file');
      return;
    }

    setSelectedFile(file);
    
    // Create preview URL
    const url = URL.createObjectURL(file);
    setAudioUrl(url);
  };

  const handleSubmit = () => {
    if (selectedFile) {
      // Convert File to Blob if needed
      const blob = selectedFile instanceof Blob 
        ? selectedFile 
        : new Blob([selectedFile], { type: selectedFile.type });
      onAudioSubmit(blob, selectedFile.name);
    }
  };

  const handleReset = () => {
    if (audioUrl) {
      URL.revokeObjectURL(audioUrl);
    }
    setSelectedFile(null);
    setAudioUrl(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="file-upload">
      {!selectedFile ? (
        <div
          className={`upload-area ${dragActive ? 'drag-active' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={handleClick}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept="audio/*"
            onChange={handleFileInput}
            style={{ display: 'none' }}
          />
          <div className="upload-content">
            <div className="upload-icon">📁</div>
            <h3>Drop audio file here or click to browse</h3>
            <p>Supports: MP3, WAV, FLAC, M4A, OGG, and other audio formats</p>
          </div>
        </div>
      ) : (
        <div className="file-preview">
          <div className="file-info">
            <div className="file-icon">🎵</div>
            <div className="file-details">
              <h3>{selectedFile.name}</h3>
              <p>{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
            </div>
          </div>
          
          {audioUrl && (
            <div className="audio-player">
              <audio src={audioUrl} controls />
            </div>
          )}

          <div className="preview-actions">
            <button
              className="submit-button"
              onClick={handleSubmit}
              disabled={loading}
            >
              {loading ? 'Processing...' : 'Submit for Analysis'}
            </button>
            <button
              className="reset-button"
              onClick={handleReset}
              disabled={loading}
            >
              Choose Different File
            </button>
          </div>
        </div>
      )}

      {loading && (
        <div className="loading-overlay">
          <div className="spinner"></div>
          <p>Analyzing audio...</p>
        </div>
      )}
    </div>
  );
};

export default FileUpload;


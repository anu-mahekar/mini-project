import React, { useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Navbar from './components/Navbar';
import Login from './components/Login';
import Register from './components/Register';
import History from './components/History';
import AudioRecorder from './components/AudioRecorder';
import FileUpload from './components/FileUpload';
import ResultDisplay from './components/ResultDisplay';
import { uploadAudio } from './services/api';
import './App.css';

function MainApp() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('record');

  const handleAudioSubmit = async (audioBlob, fileName) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const predictionResult = await uploadAudio(audioBlob, fileName);
      setResult(predictionResult);
    } catch (err) {
      setError(err.message || 'Failed to process audio. Please try again.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  return (
    <div className="App">
      <Navbar />
      <div className="app-content">
        <div className="container">
          <header className="app-header">
            <h1>Bird Sound Recognition</h1>
            <p>Record or upload bird audio to identify the species</p>
          </header>

          {!result ? (
            <div className="main-content">
              <div className="tab-selector">
                <button
                  className={`tab-button ${activeTab === 'record' ? 'active' : ''}`}
                  onClick={() => setActiveTab('record')}
                >
                  Record Audio
                </button>
                <button
                  className={`tab-button ${activeTab === 'upload' ? 'active' : ''}`}
                  onClick={() => setActiveTab('upload')}
                >
                  Upload File
                </button>
              </div>

              <div className="tab-content">
                {activeTab === 'record' ? (
                  <AudioRecorder
                    onAudioSubmit={handleAudioSubmit}
                    loading={loading}
                  />
                ) : (
                  <FileUpload
                    onAudioSubmit={handleAudioSubmit}
                    loading={loading}
                  />
                )}
              </div>

              {error && (
                <div className="error-message">
                  <p>{error}</p>
                </div>
              )}
            </div>
          ) : (
            <ResultDisplay
              result={result}
              onReset={handleReset}
            />
          )}
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <MainApp />
            </ProtectedRoute>
          }
        />
        <Route
          path="/history"
          element={
            <ProtectedRoute>
              <History />
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AuthProvider>
  );
}

export default App;

# Test Cases Documentation

## Table of Contents
1. [Overview](#overview)
2. [Backend Test Cases](#backend-test-cases)
3. [Frontend Test Cases](#frontend-test-cases)
4. [Integration Test Cases](#integration-test-cases)
5. [API Test Cases](#api-test-cases)
6. [Audio Processing Test Cases](#audio-processing-test-cases)
7. [ML Model Test Cases](#ml-model-test-cases)
8. [Authentication Test Cases](#authentication-test-cases)
9. [Data Enrichment Test Cases](#data-enrichment-test-cases)
10. [Performance Test Cases](#performance-test-cases)

---

## Overview

### Test Coverage
This document provides comprehensive test cases for the Bird Sound Recognition System, covering:
- **Backend**: Django REST Framework API endpoints
- **Frontend**: React components and user interactions
- **Integration**: End-to-end workflows
- **API**: REST API endpoints
- **Audio Processing**: Audio conversion and feature extraction
- **ML Model**: Prediction accuracy and performance
- **Authentication**: User authentication and authorization
- **Data Enrichment**: Wikipedia/Wikidata integration
- **Performance**: System performance and scalability

### Test Types
- **Unit Tests**: Individual component testing
- **Integration Tests**: Component interaction testing
- **End-to-End Tests**: Complete workflow testing
- **Performance Tests**: Load and performance testing
- **Security Tests**: Authentication and authorization testing

---

## 1. Backend Test Cases

### 1.1 User Registration Tests

#### Test Case: TC-BE-001 - Successful User Registration
**Description**: Test successful user registration with valid credentials
**Preconditions**: No existing user with the same username/email
**Test Steps**:
1. Send POST request to `/api/register/` with valid username, email, and password
2. Verify response status code is 201 (Created)
3. Verify response contains `token` and `user` fields
4. Verify user is created in database
5. Verify token is created in database

**Expected Results**:
- Status code: 201
- Response contains `token` and `user` fields
- User is created in database
- Token is created in database

**Test Data**:
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "testpass123"
}
```

#### Test Case: TC-BE-002 - Registration with Missing Fields
**Description**: Test user registration with missing required fields
**Preconditions**: None
**Test Steps**:
1. Send POST request to `/api/register/` with missing username
2. Verify response status code is 400 (Bad Request)
3. Verify response contains error message

**Expected Results**:
- Status code: 400
- Error message: "Username, email, and password are required."

#### Test Case: TC-BE-003 - Registration with Duplicate Username
**Description**: Test user registration with existing username
**Preconditions**: User with username "testuser" exists
**Test Steps**:
1. Send POST request to `/api/register/` with existing username
2. Verify response status code is 400 (Bad Request)
3. Verify response contains error message

**Expected Results**:
- Status code: 400
- Error message: "Username already exists."

#### Test Case: TC-BE-004 - Registration with Duplicate Email
**Description**: Test user registration with existing email
**Preconditions**: User with email "test@example.com" exists
**Test Steps**:
1. Send POST request to `/api/register/` with existing email
2. Verify response status code is 400 (Bad Request)
3. Verify response contains error message

**Expected Results**:
- Status code: 400
- Error message: "Email already registered."

#### Test Case: TC-BE-005 - Registration with Invalid Email Format
**Description**: Test user registration with invalid email format
**Preconditions**: None
**Test Steps**:
1. Send POST request to `/api/register/` with invalid email format
2. Verify response status code is 400 (Bad Request)
3. Verify response contains error message

**Expected Results**:
- Status code: 400
- Error message: "Invalid email format."

### 1.2 User Login Tests

#### Test Case: TC-BE-006 - Successful User Login
**Description**: Test successful user login with valid credentials
**Preconditions**: User exists in database
**Test Steps**:
1. Send POST request to `/api/login/` with valid username and password
2. Verify response status code is 200 (OK)
3. Verify response contains `token` and `user` fields
4. Verify token is valid

**Expected Results**:
- Status code: 200
- Response contains `token` and `user` fields
- Token is valid

**Test Data**:
```json
{
  "username": "testuser",
  "password": "testpass123"
}
```

#### Test Case: TC-BE-007 - Login with Invalid Credentials
**Description**: Test user login with invalid credentials
**Preconditions**: User exists in database
**Test Steps**:
1. Send POST request to `/api/login/` with invalid password
2. Verify response status code is 401 (Unauthorized)
3. Verify response contains error message

**Expected Results**:
- Status code: 401
- Error message: "Invalid credentials."

#### Test Case: TC-BE-008 - Login with Missing Fields
**Description**: Test user login with missing required fields
**Preconditions**: None
**Test Steps**:
1. Send POST request to `/api/login/` with missing username
2. Verify response status code is 400 (Bad Request)
3. Verify response contains error message

**Expected Results**:
- Status code: 400
- Error message: "Username and password are required."

### 1.3 User Logout Tests

#### Test Case: TC-BE-009 - Successful User Logout
**Description**: Test successful user logout
**Preconditions**: User is authenticated
**Test Steps**:
1. Send POST request to `/api/logout/` with valid token
2. Verify response status code is 200 (OK)
3. Verify token is deleted from database
4. Verify subsequent requests with same token fail

**Expected Results**:
- Status code: 200
- Token is deleted from database
- Subsequent requests with same token return 401

#### Test Case: TC-BE-010 - Logout without Authentication
**Description**: Test user logout without authentication
**Preconditions**: None
**Test Steps**:
1. Send POST request to `/api/logout/` without token
2. Verify response status code is 401 (Unauthorized)
3. Verify response contains error message

**Expected Results**:
- Status code: 401
- Error message: "Authentication credentials were not provided."

### 1.4 User Information Tests

#### Test Case: TC-BE-011 - Get User Information
**Description**: Test retrieving user information
**Preconditions**: User is authenticated
**Test Steps**:
1. Send GET request to `/api/user/` with valid token
2. Verify response status code is 200 (OK)
3. Verify response contains user information

**Expected Results**:
- Status code: 200
- Response contains user information (id, username, email)

#### Test Case: TC-BE-012 - Get User Information without Authentication
**Description**: Test retrieving user information without authentication
**Preconditions**: None
**Test Steps**:
1. Send GET request to `/api/user/` without token
2. Verify response status code is 401 (Unauthorized)
3. Verify response contains error message

**Expected Results**:
- Status code: 401
- Error message: "Authentication credentials were not provided."

### 1.5 Prediction Tests

#### Test Case: TC-BE-013 - Successful Audio Prediction
**Description**: Test successful audio prediction
**Preconditions**: User is authenticated, model files exist
**Test Steps**:
1. Send POST request to `/api/predict/` with valid audio file
2. Verify response status code is 200 (OK)
3. Verify response contains `prediction`, `bird`, and `ambiguous` fields
4. Verify prediction log is created in database

**Expected Results**:
- Status code: 200
- Response contains `prediction`, `bird`, and `ambiguous` fields
- Prediction log is created in database

**Test Data**:
- Audio file: Valid bird audio file (WAV/FLAC/MP3)

#### Test Case: TC-BE-014 - Prediction without Audio File
**Description**: Test prediction without audio file
**Preconditions**: User is authenticated
**Test Steps**:
1. Send POST request to `/api/predict/` without audio file
2. Verify response status code is 400 (Bad Request)
3. Verify response contains error message

**Expected Results**:
- Status code: 400
- Error message: "No 'audio' file provided."

#### Test Case: TC-BE-015 - Prediction without Authentication
**Description**: Test prediction without authentication
**Preconditions**: None
**Test Steps**:
1. Send POST request to `/api/predict/` without token
2. Verify response status code is 401 (Unauthorized)
3. Verify response contains error message

**Expected Results**:
- Status code: 401
- Error message: "Authentication credentials were not provided."

#### Test Case: TC-BE-016 - Prediction with Invalid Audio Format
**Description**: Test prediction with invalid audio format
**Preconditions**: User is authenticated
**Test Steps**:
1. Send POST request to `/api/predict/` with invalid audio format
2. Verify response status code is 400 (Bad Request) or 500 (Internal Server Error)
3. Verify response contains error message

**Expected Results**:
- Status code: 400 or 500
- Error message: "Could not convert audio file" or similar

#### Test Case: TC-BE-017 - Prediction with Short Audio
**Description**: Test prediction with audio that is too short
**Preconditions**: User is authenticated, model files exist
**Test Steps**:
1. Send POST request to `/api/predict/` with very short audio file (< 0.279 seconds)
2. Verify response status code is 200 (OK)
3. Verify response contains `prediction` with `label: null`
4. Verify response contains message about audio being too short

**Expected Results**:
- Status code: 200
- Response contains `prediction` with `label: null`
- Message: "Audio too short after masking to make a prediction."

#### Test Case: TC-BE-018 - Prediction with Missing Model Files
**Description**: Test prediction when model files are missing
**Preconditions**: User is authenticated, model files do not exist
**Test Steps**:
1. Send POST request to `/api/predict/` with valid audio file
2. Verify response status code is 500 (Internal Server Error)
3. Verify response contains error message about missing model files

**Expected Results**:
- Status code: 500
- Error message: "Model file not found" or similar

### 1.6 History Tests

#### Test Case: TC-BE-019 - Get Prediction History
**Description**: Test retrieving prediction history
**Preconditions**: User is authenticated, has prediction history
**Test Steps**:
1. Send GET request to `/api/history/` with valid token
2. Verify response status code is 200 (OK)
3. Verify response contains `count` and `results` fields
4. Verify results are ordered by `created_at` DESC
5. Verify results are limited to 50 records

**Expected Results**:
- Status code: 200
- Response contains `count` and `results` fields
- Results are ordered by `created_at` DESC
- Results are limited to 50 records

#### Test Case: TC-BE-020 - Get History without Authentication
**Description**: Test retrieving prediction history without authentication
**Preconditions**: None
**Test Steps**:
1. Send GET request to `/api/history/` without token
2. Verify response status code is 401 (Unauthorized)
3. Verify response contains error message

**Expected Results**:
- Status code: 401
- Error message: "Authentication credentials were not provided."

#### Test Case: TC-BE-021 - Get History with Empty Results
**Description**: Test retrieving prediction history with no predictions
**Preconditions**: User is authenticated, has no prediction history
**Test Steps**:
1. Send GET request to `/api/history/` with valid token
2. Verify response status code is 200 (OK)
3. Verify response contains `count: 0` and `results: []`

**Expected Results**:
- Status code: 200
- Response contains `count: 0` and `results: []`

---

## 2. Frontend Test Cases

### 2.1 Authentication Tests

#### Test Case: TC-FE-001 - Successful User Registration
**Description**: Test successful user registration from frontend
**Preconditions**: None
**Test Steps**:
1. Navigate to registration page
2. Fill in registration form with valid data
3. Submit form
4. Verify user is redirected to home page
5. Verify user is logged in
6. Verify token is stored in localStorage

**Expected Results**:
- User is redirected to home page
- User is logged in
- Token is stored in localStorage

#### Test Case: TC-FE-002 - Registration with Validation Errors
**Description**: Test user registration with validation errors
**Preconditions**: None
**Test Steps**:
1. Navigate to registration page
2. Fill in registration form with invalid data (missing fields, invalid email)
3. Submit form
4. Verify validation errors are displayed
5. Verify user is not registered

**Expected Results**:
- Validation errors are displayed
- User is not registered

#### Test Case: TC-FE-003 - Successful User Login
**Description**: Test successful user login from frontend
**Preconditions**: User exists in database
**Test Steps**:
1. Navigate to login page
2. Fill in login form with valid credentials
3. Submit form
4. Verify user is redirected to home page
5. Verify user is logged in
6. Verify token is stored in localStorage

**Expected Results**:
- User is redirected to home page
- User is logged in
- Token is stored in localStorage

#### Test Case: TC-FE-004 - Login with Invalid Credentials
**Description**: Test user login with invalid credentials
**Preconditions**: User exists in database
**Test Steps**:
1. Navigate to login page
2. Fill in login form with invalid credentials
3. Submit form
4. Verify error message is displayed
5. Verify user is not logged in

**Expected Results**:
- Error message is displayed
- User is not logged in

#### Test Case: TC-FE-005 - User Logout
**Description**: Test user logout from frontend
**Preconditions**: User is logged in
**Test Steps**:
1. Click logout button
2. Verify user is redirected to login page
3. Verify token is removed from localStorage
4. Verify user is logged out

**Expected Results**:
- User is redirected to login page
- Token is removed from localStorage
- User is logged out

### 2.2 Audio Recording Tests

#### Test Case: TC-FE-006 - Start Audio Recording
**Description**: Test starting audio recording
**Preconditions**: User is logged in, microphone permission granted
**Test Steps**:
1. Navigate to home page
2. Click "Record Audio" tab
3. Click "Start Recording" button
4. Verify recording starts
5. Verify recording timer starts
6. Verify "Stop Recording" button is enabled

**Expected Results**:
- Recording starts
- Recording timer starts
- "Stop Recording" button is enabled

#### Test Case: TC-FE-007 - Stop Audio Recording
**Description**: Test stopping audio recording
**Preconditions**: User is logged in, recording is in progress
**Test Steps**:
1. Click "Stop Recording" button
2. Verify recording stops
3. Verify recording timer stops
4. Verify audio playback is available
5. Verify "Submit" button is enabled

**Expected Results**:
- Recording stops
- Recording timer stops
- Audio playback is available
- "Submit" button is enabled

#### Test Case: TC-FE-008 - Audio Recording without Microphone Permission
**Description**: Test audio recording without microphone permission
**Preconditions**: User is logged in, microphone permission denied
**Test Steps**:
1. Navigate to home page
2. Click "Record Audio" tab
3. Click "Start Recording" button
4. Verify error message is displayed
5. Verify recording does not start

**Expected Results**:
- Error message is displayed
- Recording does not start

### 2.3 File Upload Tests

#### Test Case: TC-FE-009 - Upload Audio File
**Description**: Test uploading audio file
**Preconditions**: User is logged in
**Test Steps**:
1. Navigate to home page
2. Click "Upload File" tab
3. Select audio file
4. Verify file is selected
5. Verify "Submit" button is enabled
6. Click "Submit" button
7. Verify file is uploaded

**Expected Results**:
- File is selected
- "Submit" button is enabled
- File is uploaded

#### Test Case: TC-FE-010 - Upload Invalid File Type
**Description**: Test uploading invalid file type
**Preconditions**: User is logged in
**Test Steps**:
1. Navigate to home page
2. Click "Upload File" tab
3. Select non-audio file (e.g., image, text file)
4. Verify error message is displayed
5. Verify file is not selected

**Expected Results**:
- Error message is displayed
- File is not selected

#### Test Case: TC-FE-011 - Upload Large File
**Description**: Test uploading large audio file
**Preconditions**: User is logged in
**Test Steps**:
1. Navigate to home page
2. Click "Upload File" tab
3. Select large audio file (> 10 MB)
4. Verify file upload handling (may fail or take long time)
5. Verify appropriate error message or loading state

**Expected Results**:
- File upload handling works correctly
- Appropriate error message or loading state is displayed

### 2.4 Prediction Results Tests

#### Test Case: TC-FE-012 - Display Prediction Results
**Description**: Test displaying prediction results
**Preconditions**: User is logged in, prediction is completed
**Test Steps**:
1. Submit audio file for prediction
2. Wait for prediction to complete
3. Verify prediction results are displayed
4. Verify bird information is displayed
5. Verify images are displayed (if available)
6. Verify confidence score is displayed

**Expected Results**:
- Prediction results are displayed
- Bird information is displayed
- Images are displayed (if available)
- Confidence score is displayed

#### Test Case: TC-FE-013 - Display Ambiguous Prediction
**Description**: Test displaying ambiguous prediction
**Preconditions**: User is logged in, prediction is ambiguous
**Test Steps**:
1. Submit audio file for prediction
2. Wait for prediction to complete
3. Verify ambiguous prediction is displayed
4. Verify warning message is displayed
5. Verify bird information is not displayed (or partial)

**Expected Results**:
- Ambiguous prediction is displayed
- Warning message is displayed
- Bird information is not displayed (or partial)

#### Test Case: TC-FE-014 - Display Prediction Error
**Description**: Test displaying prediction error
**Preconditions**: User is logged in, prediction fails
**Test Steps**:
1. Submit audio file for prediction
2. Wait for prediction to fail
3. Verify error message is displayed
4. Verify user can retry prediction

**Expected Results**:
- Error message is displayed
- User can retry prediction

### 2.5 History Tests

#### Test Case: TC-FE-015 - View Prediction History
**Description**: Test viewing prediction history
**Preconditions**: User is logged in, has prediction history
**Test Steps**:
1. Navigate to history page
2. Verify prediction history is displayed
3. Verify predictions are ordered by date (newest first)
4. Verify prediction details are displayed
5. Verify bird information is displayed (if available)

**Expected Results**:
- Prediction history is displayed
- Predictions are ordered by date (newest first)
- Prediction details are displayed
- Bird information is displayed (if available)

#### Test Case: TC-FE-016 - View Empty History
**Description**: Test viewing empty prediction history
**Preconditions**: User is logged in, has no prediction history
**Test Steps**:
1. Navigate to history page
2. Verify empty history message is displayed
3. Verify user can navigate back to home page

**Expected Results**:
- Empty history message is displayed
- User can navigate back to home page

### 2.6 Navigation Tests

#### Test Case: TC-FE-017 - Navigate to Protected Route
**Description**: Test navigating to protected route without authentication
**Preconditions**: User is not logged in
**Test Steps**:
1. Navigate to home page
2. Verify user is redirected to login page
3. Verify login page is displayed

**Expected Results**:
- User is redirected to login page
- Login page is displayed

#### Test Case: TC-FE-018 - Navigate to History Page
**Description**: Test navigating to history page
**Preconditions**: User is logged in
**Test Steps**:
1. Click "History" link in navbar
2. Verify history page is displayed
3. Verify prediction history is loaded

**Expected Results**:
- History page is displayed
- Prediction history is loaded

---

## 3. Integration Test Cases

### 3.1 Complete Workflow Tests

#### Test Case: TC-INT-001 - Complete Prediction Workflow
**Description**: Test complete prediction workflow from registration to prediction
**Preconditions**: None
**Test Steps**:
1. Register new user
2. Login with credentials
3. Record audio or upload audio file
4. Submit audio for prediction
5. Verify prediction results are displayed
6. Verify prediction is saved to history
7. View prediction history
8. Verify prediction appears in history

**Expected Results**:
- User is registered and logged in
- Audio is recorded/uploaded
- Prediction results are displayed
- Prediction is saved to history
- Prediction appears in history

#### Test Case: TC-INT-002 - Multiple Predictions Workflow
**Description**: Test multiple predictions workflow
**Preconditions**: User is logged in
**Test Steps**:
1. Submit first audio file for prediction
2. Verify first prediction results are displayed
3. Reset and submit second audio file for prediction
4. Verify second prediction results are displayed
5. View prediction history
6. Verify both predictions appear in history

**Expected Results**:
- Both predictions are displayed
- Both predictions appear in history

#### Test Case: TC-INT-003 - Authentication Workflow
**Description**: Test complete authentication workflow
**Preconditions**: None
**Test Steps**:
1. Register new user
2. Login with credentials
3. Access protected routes
4. Logout
5. Verify user cannot access protected routes
6. Login again with credentials
7. Verify user can access protected routes

**Expected Results**:
- User can register and login
- User can access protected routes when logged in
- User cannot access protected routes when logged out
- User can login again and access protected routes

---

## 4. API Test Cases

### 4.1 API Endpoint Tests

#### Test Case: TC-API-001 - API Endpoint Availability
**Description**: Test API endpoint availability
**Preconditions**: Backend server is running
**Test Steps**:
1. Send GET request to `/api/` endpoint
2. Verify response status code is 200 or 404 (expected)
3. Verify API is accessible

**Expected Results**:
- API is accessible
- Response status code is 200 or 404 (expected)

#### Test Case: TC-API-002 - CORS Configuration
**Description**: Test CORS configuration
**Preconditions**: Backend server is running
**Test Steps**:
1. Send OPTIONS request to `/api/predict/` from frontend origin
2. Verify CORS headers are present
3. Verify CORS headers allow frontend origin

**Expected Results**:
- CORS headers are present
- CORS headers allow frontend origin

#### Test Case: TC-API-003 - API Response Format
**Description**: Test API response format
**Preconditions**: Backend server is running, user is authenticated
**Test Steps**:
1. Send GET request to `/api/user/` with valid token
2. Verify response is JSON format
3. Verify response contains expected fields
4. Verify response structure is correct

**Expected Results**:
- Response is JSON format
- Response contains expected fields
- Response structure is correct

### 4.2 API Error Handling Tests

#### Test Case: TC-API-004 - API Error Responses
**Description**: Test API error responses
**Preconditions**: Backend server is running
**Test Steps**:
1. Send invalid request to API endpoint
2. Verify error response is returned
3. Verify error response contains `detail` field
4. Verify error response status code is appropriate

**Expected Results**:
- Error response is returned
- Error response contains `detail` field
- Error response status code is appropriate

#### Test Case: TC-API-005 - API Rate Limiting
**Description**: Test API rate limiting (if implemented)
**Preconditions**: Backend server is running
**Test Steps**:
1. Send multiple requests to API endpoint in short time
2. Verify rate limiting is applied (if implemented)
3. Verify appropriate error response is returned

**Expected Results**:
- Rate limiting is applied (if implemented)
- Appropriate error response is returned

---

## 5. Audio Processing Test Cases

### 5.1 Audio Conversion Tests

#### Test Case: TC-AUDIO-001 - Convert WebM to WAV
**Description**: Test converting WebM audio to WAV format
**Preconditions**: WebM audio file exists, ffmpeg is installed
**Test Steps**:
1. Provide WebM audio file
2. Convert to WAV format
3. Verify WAV file is created
4. Verify WAV file is valid
5. Verify WAV file has correct sample rate (22,050 Hz)
6. Verify WAV file is mono

**Expected Results**:
- WAV file is created
- WAV file is valid
- WAV file has correct sample rate (22,050 Hz)
- WAV file is mono

#### Test Case: TC-AUDIO-002 - Convert MP3 to WAV
**Description**: Test converting MP3 audio to WAV format
**Preconditions**: MP3 audio file exists, ffmpeg is installed
**Test Steps**:
1. Provide MP3 audio file
2. Convert to WAV format
3. Verify WAV file is created
4. Verify WAV file is valid
5. Verify WAV file has correct sample rate (22,050 Hz)
6. Verify WAV file is mono

**Expected Results**:
- WAV file is created
- WAV file is valid
- WAV file has correct sample rate (22,050 Hz)
- WAV file is mono

#### Test Case: TC-AUDIO-003 - Convert FLAC to WAV
**Description**: Test converting FLAC audio to WAV format (should be direct processing)
**Preconditions**: FLAC audio file exists
**Test Steps**:
1. Provide FLAC audio file
2. Process audio (should not convert, direct processing)
3. Verify audio is processed directly
4. Verify audio has correct sample rate (22,050 Hz)
5. Verify audio is mono

**Expected Results**:
- Audio is processed directly (no conversion)
- Audio has correct sample rate (22,050 Hz)
- Audio is mono

#### Test Case: TC-AUDIO-004 - Convert Invalid Audio Format
**Description**: Test converting invalid audio format
**Preconditions**: Invalid audio file exists
**Test Steps**:
1. Provide invalid audio file
2. Attempt to convert to WAV format
3. Verify error is returned
4. Verify error message is appropriate

**Expected Results**:
- Error is returned
- Error message is appropriate

### 5.2 Audio Loading Tests

#### Test Case: TC-AUDIO-005 - Load Audio File
**Description**: Test loading audio file
**Preconditions**: Valid audio file exists
**Test Steps**:
1. Load audio file using librosa
2. Verify audio is loaded successfully
3. Verify audio has correct sample rate (22,050 Hz)
4. Verify audio is mono
5. Verify audio is numpy array

**Expected Results**:
- Audio is loaded successfully
- Audio has correct sample rate (22,050 Hz)
- Audio is mono
- Audio is numpy array

#### Test Case: TC-AUDIO-006 - Load Empty Audio File
**Description**: Test loading empty audio file
**Preconditions**: Empty audio file exists
**Test Steps**:
1. Load empty audio file using librosa
2. Verify audio is loaded (may be empty array)
3. Verify appropriate handling of empty audio

**Expected Results**:
- Audio is loaded (may be empty array)
- Appropriate handling of empty audio

### 5.3 Audio Masking Tests

#### Test Case: TC-AUDIO-007 - Apply Audio Masking
**Description**: Test applying audio masking to remove silence
**Preconditions**: Valid audio file exists
**Test Steps**:
1. Load audio file
2. Apply audio masking
3. Verify masked audio is created
4. Verify masked audio has reduced length (silence removed)
5. Verify masked audio contains only active portions

**Expected Results**:
- Masked audio is created
- Masked audio has reduced length (silence removed)
- Masked audio contains only active portions

#### Test Case: TC-AUDIO-008 - Audio Masking with All Silence
**Description**: Test audio masking with audio that is all silence
**Preconditions**: Audio file with all silence exists
**Test Steps**:
1. Load audio file with all silence
2. Apply audio masking
3. Verify masked audio handling (may return original or empty)
4. Verify appropriate handling of all-silence audio

**Expected Results**:
- Masked audio handling works correctly
- Appropriate handling of all-silence audio

### 5.4 Audio Windowing Tests

#### Test Case: TC-AUDIO-009 - Create Audio Windows
**Description**: Test creating audio windows
**Preconditions**: Valid audio file exists
**Test Steps**:
1. Load audio file
2. Apply audio masking
3. Create audio windows (6,144 samples each)
4. Verify windows are created
5. Verify windows have correct size (6,144 samples)
6. Verify windows are non-overlapping

**Expected Results**:
- Windows are created
- Windows have correct size (6,144 samples)
- Windows are non-overlapping

#### Test Case: TC-AUDIO-010 - Create Windows with Short Audio
**Description**: Test creating windows with audio that is too short
**Preconditions**: Short audio file exists (< 6,144 samples)
**Test Steps**:
1. Load short audio file
2. Apply audio masking
3. Attempt to create audio windows
4. Verify no windows are created (or empty list)
5. Verify appropriate handling of short audio

**Expected Results**:
- No windows are created (or empty list)
- Appropriate handling of short audio

### 5.5 Feature Extraction Tests

#### Test Case: TC-AUDIO-011 - Extract Features from Window
**Description**: Test extracting features from audio window
**Preconditions**: Valid audio window exists
**Test Steps**:
1. Provide audio window (6,144 samples)
2. Extract features (spectral centroid, chroma)
3. Verify features are extracted
4. Verify features have correct count (29 features)
5. Verify features are numeric (float)

**Expected Results**:
- Features are extracted
- Features have correct count (29 features)
- Features are numeric (float)

#### Test Case: TC-AUDIO-012 - Extract Features from Multiple Windows
**Description**: Test extracting features from multiple audio windows
**Preconditions**: Multiple audio windows exist
**Test Steps**:
1. Provide multiple audio windows
2. Extract features from each window
3. Verify features are extracted from all windows
4. Verify features have correct shape (n_windows × 29 features)
5. Verify features are in correct order

**Expected Results**:
- Features are extracted from all windows
- Features have correct shape (n_windows × 29 features)
- Features are in correct order

---

## 6. ML Model Test Cases

### 6.1 Model Loading Tests

#### Test Case: TC-ML-001 - Load ML Model
**Description**: Test loading ML model
**Preconditions**: Model file (svm.sav) exists
**Test Steps**:
1. Load model file using pickle
2. Verify model is loaded successfully
3. Verify model is SVM classifier
4. Verify model has correct structure

**Expected Results**:
- Model is loaded successfully
- Model is SVM classifier
- Model has correct structure

#### Test Case: TC-ML-002 - Load Model with Missing File
**Description**: Test loading model with missing file
**Preconditions**: Model file (svm.sav) does not exist
**Test Steps**:
1. Attempt to load model file
2. Verify error is returned
3. Verify error message is appropriate

**Expected Results**:
- Error is returned
- Error message is appropriate

#### Test Case: TC-ML-003 - Load Training Data
**Description**: Test loading training data
**Preconditions**: Training CSV (train.csv) exists
**Test Steps**:
1. Load training CSV using pandas
2. Verify training data is loaded successfully
3. Verify feature columns are extracted
4. Verify feature columns have correct count (29 features)

**Expected Results**:
- Training data is loaded successfully
- Feature columns are extracted
- Feature columns have correct count (29 features)

### 6.2 Model Prediction Tests

#### Test Case: TC-ML-004 - Predict with Valid Features
**Description**: Test prediction with valid features
**Preconditions**: Model is loaded, valid features exist
**Test Steps**:
1. Provide valid features (29 features)
2. Normalize features using StandardScaler
3. Predict species using model
4. Verify prediction is returned
5. Verify prediction is string (species name)
6. Verify prediction is valid species

**Expected Results**:
- Prediction is returned
- Prediction is string (species name)
- Prediction is valid species

#### Test Case: TC-ML-005 - Predict with Multiple Windows
**Description**: Test prediction with multiple windows
**Preconditions**: Model is loaded, multiple windows exist
**Test Steps**:
1. Provide features from multiple windows
2. Predict species for each window
3. Aggregate predictions using voting
4. Verify top prediction is returned
5. Verify confidence score is calculated
6. Verify vote counts are returned

**Expected Results**:
- Top prediction is returned
- Confidence score is calculated
- Vote counts are returned

#### Test Case: TC-ML-006 - Predict with Invalid Features
**Description**: Test prediction with invalid features
**Preconditions**: Model is loaded
**Test Steps**:
1. Provide invalid features (wrong count, NaN, Inf)
2. Attempt to predict species
3. Verify error is returned or handled appropriately
4. Verify error message is appropriate

**Expected Results**:
- Error is returned or handled appropriately
- Error message is appropriate

### 6.3 Model Performance Tests

#### Test Case: TC-ML-007 - Model Prediction Accuracy
**Description**: Test model prediction accuracy
**Preconditions**: Model is loaded, test dataset exists
**Test Steps**:
1. Load test dataset
2. Predict species for test samples
3. Calculate accuracy score
4. Verify accuracy is above threshold (e.g., 70%)
5. Verify predictions are reasonable

**Expected Results**:
- Accuracy is above threshold (e.g., 70%)
- Predictions are reasonable

#### Test Case: TC-ML-008 - Model Prediction Speed
**Description**: Test model prediction speed
**Preconditions**: Model is loaded, test samples exist
**Test Steps**:
1. Provide test samples
2. Measure prediction time
3. Verify prediction time is acceptable (< 1 second per sample)
4. Verify prediction speed is consistent

**Expected Results**:
- Prediction time is acceptable (< 1 second per sample)
- Prediction speed is consistent

---

## 7. Authentication Test Cases

### 7.1 Token Authentication Tests

#### Test Case: TC-AUTH-001 - Token Generation
**Description**: Test token generation
**Preconditions**: User exists in database
**Test Steps**:
1. Register or login user
2. Verify token is generated
3. Verify token is stored in database
4. Verify token is returned to client

**Expected Results**:
- Token is generated
- Token is stored in database
- Token is returned to client

#### Test Case: TC-AUTH-002 - Token Validation
**Description**: Test token validation
**Preconditions**: User is authenticated, token exists
**Test Steps**:
1. Send request with valid token
2. Verify token is validated
3. Verify user is authenticated
4. Verify request is processed

**Expected Results**:
- Token is validated
- User is authenticated
- Request is processed

#### Test Case: TC-AUTH-003 - Token Expiration
**Description**: Test token expiration (if implemented)
**Preconditions**: User is authenticated, token exists
**Test Steps**:
1. Wait for token to expire (if expiration is implemented)
2. Send request with expired token
3. Verify token is rejected
4. Verify user is not authenticated
5. Verify appropriate error is returned

**Expected Results**:
- Token is rejected
- User is not authenticated
- Appropriate error is returned

#### Test Case: TC-AUTH-004 - Token Deletion
**Description**: Test token deletion on logout
**Preconditions**: User is authenticated, token exists
**Test Steps**:
1. Logout user
2. Verify token is deleted from database
3. Verify subsequent requests with same token fail
4. Verify user is not authenticated

**Expected Results**:
- Token is deleted from database
- Subsequent requests with same token fail
- User is not authenticated

### 7.2 Session Authentication Tests

#### Test Case: TC-AUTH-005 - Session Creation
**Description**: Test session creation
**Preconditions**: User exists in database
**Test Steps**:
1. Login user
2. Verify session is created
3. Verify session is stored
4. Verify session ID is returned to client

**Expected Results**:
- Session is created
- Session is stored
- Session ID is returned to client

#### Test Case: TC-AUTH-006 - Session Validation
**Description**: Test session validation
**Preconditions**: User is authenticated, session exists
**Test Steps**:
1. Send request with valid session
2. Verify session is validated
3. Verify user is authenticated
4. Verify request is processed

**Expected Results**:
- Session is validated
- User is authenticated
- Request is processed

---

## 8. Data Enrichment Test Cases

### 8.1 Wikipedia Enrichment Tests

#### Test Case: TC-ENRICH-001 - Fetch Wikipedia Summary
**Description**: Test fetching Wikipedia summary
**Preconditions**: Bird exists in database, Wikipedia API is accessible
**Test Steps**:
1. Run enrichment command for bird
2. Verify Wikipedia summary is fetched
3. Verify summary is stored in database
4. Verify Wikipedia URL is stored

**Expected Results**:
- Wikipedia summary is fetched
- Summary is stored in database
- Wikipedia URL is stored

#### Test Case: TC-ENRICH-002 - Fetch Wikipedia Images
**Description**: Test fetching Wikipedia images
**Preconditions**: Bird exists in database, Wikipedia API is accessible
**Test Steps**:
1. Run enrichment command for bird
2. Verify Wikipedia images are fetched
3. Verify images are stored in database
4. Verify image URLs are valid

**Expected Results**:
- Wikipedia images are fetched
- Images are stored in database
- Image URLs are valid

#### Test Case: TC-ENRICH-003 - Wikipedia API Error Handling
**Description**: Test Wikipedia API error handling
**Preconditions**: Bird exists in database, Wikipedia API is inaccessible or bird not found
**Test Steps**:
1. Run enrichment command for bird not in Wikipedia
2. Verify error is handled gracefully
3. Verify bird is not updated with invalid data
4. Verify appropriate error message is logged

**Expected Results**:
- Error is handled gracefully
- Bird is not updated with invalid data
- Appropriate error message is logged

### 8.2 Wikidata Enrichment Tests

#### Test Case: TC-ENRICH-004 - Fetch Wikidata QID
**Description**: Test fetching Wikidata QID
**Preconditions**: Bird exists in database, Wikidata API is accessible
**Test Steps**:
1. Run enrichment command for bird
2. Verify Wikidata QID is fetched
3. Verify QID is stored in database
4. Verify QID is valid format

**Expected Results**:
- Wikidata QID is fetched
- QID is stored in database
- QID is valid format

#### Test Case: TC-ENRICH-005 - Fetch Wikidata Habitat
**Description**: Test fetching Wikidata habitat
**Preconditions**: Bird exists in database, Wikidata QID exists
**Test Steps**:
1. Run enrichment command for bird with QID
2. Verify habitat (P141) is fetched
3. Verify habitat is stored in database
4. Verify habitat is valid text

**Expected Results**:
- Habitat (P141) is fetched
- Habitat is stored in database
- Habitat is valid text

#### Test Case: TC-ENRICH-006 - Fetch Wikidata Diet
**Description**: Test fetching Wikidata diet
**Preconditions**: Bird exists in database, Wikidata QID exists
**Test Steps**:
1. Run enrichment command for bird with QID
2. Verify diet (P2078/P2079) is fetched
3. Verify diet is stored in database
4. Verify diet is valid text

**Expected Results**:
- Diet (P2078/P2079) is fetched
- Diet is stored in database
- Diet is valid text

#### Test Case: TC-ENRICH-007 - Wikidata API Error Handling
**Description**: Test Wikidata API error handling
**Preconditions**: Bird exists in database, Wikidata API is inaccessible
**Test Steps**:
1. Run enrichment command when Wikidata API is inaccessible
2. Verify error is handled gracefully
3. Verify bird is not updated with invalid data
4. Verify appropriate error message is logged

**Expected Results**:
- Error is handled gracefully
- Bird is not updated with invalid data
- Appropriate error message is logged

### 8.3 CSV Enrichment Tests

#### Test Case: TC-ENRICH-008 - Import CSV Data
**Description**: Test importing CSV data
**Preconditions**: CSV file exists with bird data
**Test Steps**:
1. Run enrichment command with CSV file
2. Verify CSV data is parsed
3. Verify bird records are created/updated
4. Verify data is stored in database

**Expected Results**:
- CSV data is parsed
- Bird records are created/updated
- Data is stored in database

#### Test Case: TC-ENRICH-009 - CSV Validation
**Description**: Test CSV validation
**Preconditions**: CSV file exists with invalid data
**Test Steps**:
1. Run enrichment command with invalid CSV file
2. Verify validation errors are handled
3. Verify invalid records are skipped
4. Verify valid records are processed

**Expected Results**:
- Validation errors are handled
- Invalid records are skipped
- Valid records are processed

---

## 9. Performance Test Cases

### 9.1 API Performance Tests

#### Test Case: TC-PERF-001 - API Response Time
**Description**: Test API response time
**Preconditions**: Backend server is running, user is authenticated
**Test Steps**:
1. Send request to API endpoint
2. Measure response time
3. Verify response time is acceptable (< 1 second for simple endpoints)
4. Verify response time is consistent

**Expected Results**:
- Response time is acceptable (< 1 second for simple endpoints)
- Response time is consistent

#### Test Case: TC-PERF-002 - Prediction Response Time
**Description**: Test prediction response time
**Preconditions**: Backend server is running, user is authenticated, model is loaded
**Test Steps**:
1. Send prediction request with audio file
2. Measure response time
3. Verify response time is acceptable (< 5 seconds for prediction)
4. Verify response time is consistent

**Expected Results**:
- Response time is acceptable (< 5 seconds for prediction)
- Response time is consistent

#### Test Case: TC-PERF-003 - Concurrent Request Handling
**Description**: Test concurrent request handling
**Preconditions**: Backend server is running, multiple users are authenticated
**Test Steps**:
1. Send multiple concurrent requests to API endpoint
2. Verify all requests are processed
3. Verify response times are acceptable
4. Verify no requests are dropped

**Expected Results**:
- All requests are processed
- Response times are acceptable
- No requests are dropped

### 9.2 Database Performance Tests

#### Test Case: TC-PERF-004 - Database Query Performance
**Description**: Test database query performance
**Preconditions**: Database contains bird records and prediction logs
**Test Steps**:
1. Execute database queries (bird lookup, prediction history)
2. Measure query execution time
3. Verify query execution time is acceptable (< 100ms for simple queries)
4. Verify queries are optimized (use indexes)

**Expected Results**:
- Query execution time is acceptable (< 100ms for simple queries)
- Queries are optimized (use indexes)

#### Test Case: TC-PERF-005 - Database Write Performance
**Description**: Test database write performance
**Preconditions**: Database is accessible
**Test Steps**:
1. Execute database writes (create prediction log, update bird)
2. Measure write execution time
3. Verify write execution time is acceptable (< 50ms for simple writes)
4. Verify writes are atomic (transaction handling)

**Expected Results**:
- Write execution time is acceptable (< 50ms for simple writes)
- Writes are atomic (transaction handling)

### 9.3 Frontend Performance Tests

#### Test Case: TC-PERF-006 - Page Load Time
**Description**: Test page load time
**Preconditions**: Frontend server is running
**Test Steps**:
1. Navigate to frontend page
2. Measure page load time
3. Verify page load time is acceptable (< 2 seconds)
4. Verify page is responsive

**Expected Results**:
- Page load time is acceptable (< 2 seconds)
- Page is responsive

#### Test Case: TC-PERF-007 - Component Render Time
**Description**: Test component render time
**Preconditions**: Frontend server is running, user is logged in
**Test Steps**:
1. Navigate to page with components
2. Measure component render time
3. Verify component render time is acceptable (< 500ms)
4. Verify components are optimized

**Expected Results**:
- Component render time is acceptable (< 500ms)
- Components are optimized

---

## Test Execution Summary

### Test Categories
- **Backend Tests**: 21 test cases
- **Frontend Tests**: 18 test cases
- **Integration Tests**: 3 test cases
- **API Tests**: 5 test cases
- **Audio Processing Tests**: 12 test cases
- **ML Model Tests**: 8 test cases
- **Authentication Tests**: 6 test cases
- **Data Enrichment Tests**: 9 test cases
- **Performance Tests**: 7 test cases

### Total Test Cases
**89 test cases** covering all aspects of the Bird Sound Recognition System.

### Test Priority
- **High Priority**: Critical functionality (authentication, prediction, API endpoints)
- **Medium Priority**: Important functionality (audio processing, ML model, data enrichment)
- **Low Priority**: Nice-to-have functionality (performance, edge cases)

### Test Execution
- **Manual Testing**: Execute test cases manually during development
- **Automated Testing**: Implement automated tests for critical functionality
- **Continuous Testing**: Run tests continuously during development and deployment

---

This test cases documentation provides comprehensive coverage of all test scenarios for the Bird Sound Recognition System.


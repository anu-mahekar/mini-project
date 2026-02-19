# Data Flow Diagram Documentation

## Table of Contents
1. [Overview](#overview)
2. [Authentication Flow](#authentication-flow)
3. [Prediction Flow](#prediction-flow)
4. [History Flow](#history-flow)
5. [Enrichment Flow](#enrichment-flow)
6. [Error Flow](#error-flow)

---

## Overview

### Data Flow Architecture
The Bird Sound Recognition System uses a **client-server architecture** with RESTful API communication. Data flows from the React frontend through the Django backend to the database and ML model, then back to the frontend.

### Key Components
- **Frontend**: React application (client)
- **Backend**: Django REST Framework (server)
- **Database**: SQLite (data storage)
- **ML Model**: SVM model (prediction)
- **External APIs**: Wikipedia/Wikidata (enrichment)

---

## 1. Authentication Flow

### 1.1 Registration Flow

```
┌─────────┐
│  User   │
└────┬────┘
     │
     │ 1. Fill Registration Form
     │    (username, email, password)
     ▼
┌─────────────────────────────────┐
│   React Frontend                │
│   - Register Component          │
│   - Form Validation             │
└────┬────────────────────────────┘
     │
     │ 2. POST /api/register/
     │    {
     │      "username": "user",
     │      "email": "user@example.com",
     │      "password": "pass123"
     │    }
     ▼
┌─────────────────────────────────┐
│   Django Backend                │
│   - RegisterView                │
│   - Input Validation            │
│   - User Creation               │
│   - Token Generation            │
└────┬────────────────────────────┘
     │
     │ 3. Create User
     │    User.objects.create_user(...)
     ▼
┌─────────────────────────────────┐
│   Database (SQLite)             │
│   - User Table                  │
│   - Token Table                 │
└────┬────────────────────────────┘
     │
     │ 4. Return Response
     │    {
     │      "token": "abc123...",
     │      "user": {...}
     │    }
     ▼
┌─────────────────────────────────┐
│   React Frontend                │
│   - Store Token (localStorage)  │
│   - Store User (localStorage)   │
│   - Update AuthContext          │
│   - Navigate to Home            │
└─────────────────────────────────┘
```

### 1.2 Login Flow

```
┌─────────┐
│  User   │
└────┬────┘
     │
     │ 1. Fill Login Form
     │    (username, password)
     ▼
┌─────────────────────────────────┐
│   React Frontend                │
│   - Login Component             │
│   - Form Validation             │
└────┬────────────────────────────┘
     │
     │ 2. POST /api/login/
     │    {
     │      "username": "user",
     │      "password": "pass123"
     │    }
     ▼
┌─────────────────────────────────┐
│   Django Backend                │
│   - LoginView                   │
│   - User Authentication         │
│   - Token Generation/Retrieval  │
└────┬────────────────────────────┘
     │
     │ 3. Authenticate User
     │    authenticate(username, password)
     ▼
┌─────────────────────────────────┐
│   Database (SQLite)             │
│   - User Table                  │
│   - Password Verification       │
│   - Token Table                 │
└────┬────────────────────────────┘
     │
     │ 4. Return Response
     │    {
     │      "token": "abc123...",
     │      "user": {...}
     │    }
     ▼
┌─────────────────────────────────┐
│   React Frontend                │
│   - Store Token (localStorage)  │
│   - Store User (localStorage)   │
│   - Update AuthContext          │
│   - Navigate to Home            │
└─────────────────────────────────┘
```

### 1.3 Logout Flow

```
┌─────────┐
│  User   │
└────┬────┘
     │
     │ 1. Click Logout Button
     ▼
┌─────────────────────────────────┐
│   React Frontend                │
│   - Logout Handler              │
│   - API Call                    │
└────┬────────────────────────────┘
     │
     │ 2. POST /api/logout/
     │    Headers: Authorization: Token abc123...
     ▼
┌─────────────────────────────────┐
│   Django Backend                │
│   - LogoutView                  │
│   - Token Deletion              │
│   - Session Logout              │
└────┬────────────────────────────┘
     │
     │ 3. Delete Token
     │    request.user.auth_token.delete()
     ▼
┌─────────────────────────────────┐
│   Database (SQLite)             │
│   - Token Table                 │
│   - Token Deleted               │
└────┬────────────────────────────┘
     │
     │ 4. Return Response
     │    {"detail": "Successfully logged out."}
     ▼
┌─────────────────────────────────┐
│   React Frontend                │
│   - Clear Token (localStorage)  │
│   - Clear User (localStorage)   │
│   - Update AuthContext          │
│   - Navigate to Login           │
└─────────────────────────────────┘
```

---

## 2. Prediction Flow

### 2.1 Audio Upload Flow

```
┌─────────┐
│  User   │
└────┬────┘
     │
     │ 1. Record Audio or Upload File
     │    - AudioRecorder: Record audio (WebM)
     │    - FileUpload: Upload file (WAV/FLAC/MP3)
     ▼
┌─────────────────────────────────┐
│   React Frontend                │
│   - AudioRecorder/FileUpload    │
│   - Audio Blob Creation         │
│   - FormData Creation           │
└────┬────────────────────────────┘
     │
     │ 2. POST /api/predict/
     │    Headers: Authorization: Token abc123...
     │    Body: FormData { audio: Blob }
     ▼
┌─────────────────────────────────┐
│   Django Backend                │
│   - PredictView                 │
│   - Authentication Check        │
│   - File Validation             │
└────┬────────────────────────────┘
     │
     │ 3. Save Audio File
     │    media/predict_uploads/{uuid}_{filename}
     ▼
┌─────────────────────────────────┐
│   File System                   │
│   - Temporary File Storage      │
│   - Audio File (webm/wav/flac)  │
└────┬────────────────────────────┘
     │
     │ 4. Audio Processing
     │    predict_audio_file(temp_path)
     ▼
┌─────────────────────────────────┐
│   Audio Processing Service      │
│   - Audio Conversion (webm→wav) │
│   - Audio Loading (librosa)     │
│   - Audio Masking               │
│   - Windowing                   │
│   - Feature Extraction          │
└────┬────────────────────────────┘
     │
     │ 5. ML Prediction
     │    _MODEL.predict(X)
     ▼
┌─────────────────────────────────┐
│   ML Model (SVM)                │
│   - Feature Normalization       │
│   - Species Prediction          │
│   - Vote Aggregation            │
└────┬────────────────────────────┘
     │
     │ 6. Prediction Result
     │    {
     │      "pred_top": "Sylvia communis",
     │      "confidence": 0.85,
     │      "votes": {...},
     │      "windows": 10
     │    }
     ▼
┌─────────────────────────────────┐
│   Database Matching             │
│   - Bird.objects.filter(...)    │
│   - Species Matching            │
└────┬────────────────────────────┘
     │
     │ 7. Bird Information
     │    Bird record (if matched)
     ▼
┌─────────────────────────────────┐
│   Database (SQLite)             │
│   - Bird Table                  │
│   - PredictionLog Table         │
└────┬────────────────────────────┘
     │
     │ 8. Save Prediction
     │    PredictionLog.objects.create(...)
     ▼
┌─────────────────────────────────┐
│   Database (SQLite)             │
│   - PredictionLog Table         │
│   - Prediction Saved            │
└────┬────────────────────────────┘
     │
     │ 9. Return Response
     │    {
     │      "prediction": {...},
     │      "bird": {...},
     │      "ambiguous": false
     │    }
     ▼
┌─────────────────────────────────┐
│   React Frontend                │
│   - ResultDisplay Component     │
│   - Display Prediction          │
│   - Display Bird Information    │
│   - Display Images              │
└─────────────────────────────────┘
```

### 2.2 Detailed Prediction Flow

#### Step 1: Audio Conversion
```
WebM/MP3/M4A/OGG → ffmpeg/pydub → WAV (22,050 Hz, mono)
```

#### Step 2: Audio Loading
```
WAV File → librosa.load() → NumPy Array (float32)
```

#### Step 3: Audio Masking
```
Audio Signal → Melspectrogram → Energy Analysis → Mask Creation → Masked Audio
```

#### Step 4: Windowing
```
Masked Audio → Windows (6,144 samples) → List of Windows
```

#### Step 5: Feature Extraction
```
Window → Spectral Centroid → 5 Features
Window → Chroma STFT → 24 Features
Total: 29 Features per Window
```

#### Step 6: Feature Normalization
```
Features → StandardScaler → Normalized Features
```

#### Step 7: ML Prediction
```
Normalized Features → SVM Model → Species Prediction
```

#### Step 8: Vote Aggregation
```
Window Predictions → Counter → Top Prediction → Confidence
```

#### Step 9: Database Matching
```
Predicted Species → Bird.objects.filter() → Bird Record
```

#### Step 10: Prediction Logging
```
Prediction Result → PredictionLog.objects.create() → Database
```

---

## 3. History Flow

### 3.1 History Retrieval Flow

```
┌─────────┐
│  User   │
└────┬────┘
     │
     │ 1. Navigate to History Page
     ▼
┌─────────────────────────────────┐
│   React Frontend                │
│   - History Component           │
│   - API Call                    │
└────┬────────────────────────────┘
     │
     │ 2. GET /api/history/
     │    Headers: Authorization: Token abc123...
     ▼
┌─────────────────────────────────┐
│   Django Backend                │
│   - HistoryView                 │
│   - Authentication Check        │
│   - User Filtering              │
└────┬────────────────────────────┘
     │
     │ 3. Query Predictions
     │    PredictionLog.objects.filter(user=request.user)[:50]
     ▼
┌─────────────────────────────────┐
│   Database (SQLite)             │
│   - PredictionLog Table         │
│   - User Filtering              │
│   - Order by created_at DESC    │
└────┬────────────────────────────┘
     │
     │ 4. Serialize Predictions
     │    PredictionLogSerializer(predictions, many=True)
     ▼
┌─────────────────────────────────┐
│   Django Backend                │
│   - Serializer                  │
│   - Data Transformation         │
└────┬────────────────────────────┘
     │
     │ 5. Return Response
     │    {
     │      "count": 10,
     │      "results": [...]
     │    }
     ▼
┌─────────────────────────────────┐
│   React Frontend                │
│   - History Component           │
│   - Display Predictions         │
│   - Display Bird Information    │
└─────────────────────────────────┘
```

### 3.2 History Data Flow

#### Prediction Log Structure
```
PredictionLog
├── user (ForeignKey → User)
├── matched_bird (ForeignKey → Bird)
├── created_at (DateTime)
├── filename (String)
├── predicted_label (String)
├── confidence (Float)
└── top_votes_json (JSON)
```

#### Serialization Flow
```
PredictionLog → PredictionLogSerializer → JSON → React Frontend
```

---

## 4. Enrichment Flow

### 4.1 Wikipedia Enrichment Flow

```
┌─────────┐
│  Admin  │
└────┬────┘
     │
     │ 1. Run Enrichment Command
     │    python manage.py enrich_birds --from-wiki --limit 10
     ▼
┌─────────────────────────────────┐
│   Django Management Command     │
│   - enrich_birds.py             │
│   - Bird Query                  │
└────┬────────────────────────────┘
     │
     │ 2. Query Birds
     │    Bird.objects.all()[:10]
     ▼
┌─────────────────────────────────┐
│   Database (SQLite)             │
│   - Bird Table                  │
│   - Bird Records                │
└────┬────────────────────────────┘
     │
     │ 3. Fetch Wikipedia Data
     │    wiki_summary_for_title(bird.english_cname)
     ▼
┌─────────────────────────────────┐
│   Wikipedia API                 │
│   - REST API                    │
│   - Page Summary                │
│   - Images                      │
└────┬────────────────────────────┘
     │
     │ 4. Wikipedia Response
     │    {
     │      "title": "Common Whitethroat",
     │      "extract": "The common whitethroat...",
     │      "originalimage": {...}
     │    }
     ▼
┌─────────────────────────────────┐
│   Django Management Command     │
│   - Data Parsing                │
│   - Bird Update                 │
└────┬────────────────────────────┘
     │
     │ 5. Update Bird
     │    bird.notes = extract
     │    bird.wikipedia_url = url
     │    bird.image_url_1 = image
     │    bird.save()
     ▼
┌─────────────────────────────────┐
│   Database (SQLite)             │
│   - Bird Table                  │
│   - Bird Updated                │
└─────────────────────────────────┘
```

### 4.2 Wikidata Enrichment Flow

```
┌─────────┐
│  Admin  │
└────┬────┘
     │
     │ 1. Run Enrichment Command
     │    python manage.py enrich_birds --from-wiki --limit 10
     ▼
┌─────────────────────────────────┐
│   Django Management Command     │
│   - enrich_birds.py             │
│   - Bird Query                  │
└────┬────────────────────────────┘
     │
     │ 2. Search Wikidata QID
     │    wd_search_binomial(bird.binomial)
     ▼
┌─────────────────────────────────┐
│   Wikidata API                  │
│   - Entity Search               │
│   - QID Return                  │
└────┬────────────────────────────┘
     │
     │ 3. Wikidata QID
     │    "Q25251"
     ▼
┌─────────────────────────────────┐
│   Django Management Command     │
│   - QID Storage                 │
│   - Property Fetching           │
└────┬────────────────────────────┘
     │
     │ 4. Fetch Properties
     │    wd_get_property_labels(qid, ["P141", "P2078", "P18"])
     ▼
┌─────────────────────────────────┐
│   Wikidata API                  │
│   - Entity Data                 │
│   - Properties (P141, P2078, P18)│
└────┬────────────────────────────┘
     │
     │ 5. Resolve Item References
     │    Item ID → Label
     ▼
┌─────────────────────────────────┐
│   Wikidata API                  │
│   - Label Lookup                │
│   - English Labels              │
└────┬────────────────────────────┘
     │
     │ 6. Wikidata Response
     │    {
     │      "P141": "Shrubland",
     │      "P2078": "Insects",
     │      "P18": "File:Common_Whitethroat.jpg"
     │    }
     ▼
┌─────────────────────────────────┐
│   Django Management Command     │
│   - Data Parsing                │
│   - Bird Update                 │
└────┬────────────────────────────┘
     │
     │ 7. Update Bird
     │    bird.habitat = "Shrubland"
     │    bird.diet = "Insects"
     │    bird.image_url_1 = image_url
     │    bird.wikidata_qid = "Q25251"
     │    bird.save()
     ▼
┌─────────────────────────────────┐
│   Database (SQLite)             │
│   - Bird Table                  │
│   - Bird Updated                │
└─────────────────────────────────┘
```

### 4.3 CSV Enrichment Flow

```
┌─────────┐
│  Admin  │
└────┬────┘
     │
     │ 1. Prepare CSV File
     │    binomial, habitat, diet, notes, image_url_1, ...
     ▼
┌─────────────────────────────────┐
│   CSV File                      │
│   - enrichment.csv              │
│   - Bird Data                   │
└────┬────────────────────────────┘
     │
     │ 2. Run Enrichment Command
     │    python manage.py enrich_birds --from-csv enrichment.csv
     ▼
┌─────────────────────────────────┐
│   Django Management Command     │
│   - enrich_birds.py             │
│   - CSV Parsing                 │
└────┬────────────────────────────┘
     │
     │ 3. Parse CSV
     │    pd.read_csv(csv_path)
     ▼
┌─────────────────────────────────┐
│   Pandas DataFrame              │
│   - CSV Data                    │
│   - Column Normalization        │
└────┬────────────────────────────┘
     │
     │ 4. Process Each Row
     │    for row in df.iterrows()
     ▼
┌─────────────────────────────────┐
│   Django Management Command     │
│   - Data Validation             │
│   - Bird Update/Create          │
└────┬────────────────────────────┘
     │
     │ 5. Update or Create Bird
     │    Bird.objects.update_or_create(
     │        binomial=binomial,
     │        defaults={...}
     │    )
     ▼
┌─────────────────────────────────┐
│   Database (SQLite)             │
│   - Bird Table                  │
│   - Bird Updated/Created        │
└─────────────────────────────────┘
```

---

## 5. Error Flow

### 5.1 Error Handling Flow

```
┌─────────┐
│  Error  │
└────┬────┘
     │
     │ 1. Error Occurrence
     │    - FileNotFoundError
     │    - RuntimeError
     │    - ValueError
     ▼
┌─────────────────────────────────┐
│   Exception Handling            │
│   - Try-Catch Block             │
│   - Error Catching              │
└────┬────────────────────────────┘
     │
     │ 2. Error Logging
     │    traceback.print_exc()
     ▼
┌─────────────────────────────────┐
│   Error Logging                 │
│   - Console Logging             │
│   - Traceback Printing          │
└────┬────────────────────────────┘
     │
     │ 3. Error Response
     │    {
     │      "detail": "Error message"
     │    }
     ▼
┌─────────────────────────────────┐
│   Django Backend                │
│   - Error Response              │
│   - Status Code (400/500)       │
└────┬────────────────────────────┘
     │
     │ 4. Error Transmission
     │    HTTP Response (Error)
     ▼
┌─────────────────────────────────┐
│   React Frontend                │
│   - Error Handling              │
│   - Error Display               │
└────┬────────────────────────────┘
     │
     │ 5. Error Display
     │    Error Message to User
     ▼
┌─────────┐
│  User   │
└─────────┘
```

### 5.2 Error Types

#### Authentication Errors
```
401 Unauthorized → Invalid credentials
401 Unauthorized → Token expired/invalid
403 Forbidden → Permission denied
```

#### Validation Errors
```
400 Bad Request → Missing required fields
400 Bad Request → Invalid file format
400 Bad Request → Invalid data format
```

#### Processing Errors
```
500 Internal Server Error → Model file not found
500 Internal Server Error → Audio processing error
500 Internal Server Error → Prediction error
```

#### Network Errors
```
Network Error → Backend unavailable
Timeout Error → Request timeout
Connection Error → Connection failed
```

---

## Data Flow Summary

### Request Flow
```
User → Frontend → API → Backend → Service → Database/ML Model → Response → Frontend → User
```

### Response Flow
```
Database/ML Model → Service → Backend → API → Frontend → User
```

### Error Flow
```
Error → Exception → Logging → Response → Frontend → User
```

### Authentication Flow
```
User → Frontend → API → Backend → Database → Token → Frontend → User
```

### Prediction Flow
```
User → Frontend → API → Backend → Audio Processing → ML Model → Database → Response → Frontend → User
```

### History Flow
```
User → Frontend → API → Backend → Database → Response → Frontend → User
```

### Enrichment Flow
```
Admin → Command → External API → Data Parsing → Database → Bird Updated
```

---

## Data Flow Diagrams

### Complete System Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Record     │  │   Upload     │  │   History    │         │
│  │   Audio      │  │   File       │  │   View       │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                  │                  │                  │
│  ┌──────┴──────────────────┴──────────────────┴──────┐         │
│  │           React Frontend (State Management)        │         │
│  │  - AuthContext (Authentication State)              │         │
│  │  - API Service (HTTP Client)                       │         │
│  └──────────────────────┬─────────────────────────────┘         │
└─────────────────────────┼───────────────────────────────────────┘
                          │ HTTP/REST API
                          │ (JSON, FormData)
┌─────────────────────────┼───────────────────────────────────────┐
│                    API GATEWAY                                  │
│  ┌──────────────────────────────────────────────────────┐      │
│  │         Django REST Framework                        │      │
│  │  - URL Routing                                       │      │
│  │  - Authentication Middleware                         │      │
│  │  - CORS Middleware                                   │      │
│  │  - Request Validation                                │      │
│  └──────────────────────┬───────────────────────────────┘      │
└─────────────────────────┼───────────────────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────────────────┐
│                   BUSINESS LOGIC                                │
│  ┌──────────────────────────────────────────────────────┐      │
│  │              Views (API Endpoints)                   │      │
│  │  - RegisterView (User Registration)                  │      │
│  │  - LoginView (User Authentication)                   │      │
│  │  - PredictView (Audio Prediction)                    │      │
│  │  - HistoryView (Prediction History)                  │      │
│  └──────────────────────┬───────────────────────────────┘      │
│                         │                                       │
│  ┌──────────────────────┴───────────────────────────────┐      │
│  │         Prediction Service                           │      │
│  │  - Audio Conversion (webm → wav)                     │      │
│  │  - Audio Loading (librosa)                           │      │
│  │  - Audio Masking (melspectrogram)                    │      │
│  │  - Windowing (6,144 samples)                         │      │
│  │  - Feature Extraction (29 features)                  │      │
│  │  - ML Prediction (SVM)                               │      │
│  └──────────────────────┬───────────────────────────────┘      │
│                         │                                       │
│  ┌──────────────────────┴───────────────────────────────┐      │
│  │         Enrichment Service                           │      │
│  │  - Wikipedia API (summary, images)                   │      │
│  │  - Wikidata API (habitat, diet, images)              │      │
│  └──────────────────────────────────────────────────────┘      │
└─────────────────────────┼───────────────────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────────────────┐
│                    DATA LAYER                                   │
│  ┌──────────────────────────────────────────────────────┐      │
│  │              Django ORM                              │      │
│  │  - User Model (Django Auth)                          │      │
│  │  - Bird Model                                        │      │
│  │  - PredictionLog Model                               │      │
│  └──────────────────────┬───────────────────────────────┘      │
│                         │                                       │
│  ┌──────────────────────┴───────────────────────────────┐      │
│  │              SQLite Database                         │      │
│  │  - Users                                             │      │
│  │  - Birds (species, images, habitat, diet)           │      │
│  │  - PredictionLogs (user predictions)                │      │
│  └──────────────────────┬───────────────────────────────┘      │
│                         │                                       │
│  ┌──────────────────────┴───────────────────────────────┐      │
│  │              ML Artifacts                            │      │
│  │  - svm.sav (trained model)                           │      │
│  │  - train.csv (feature schema)                        │      │
│  └──────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

### Prediction Data Flow (Detailed)

```
User Input (Audio)
    │
    ▼
┌─────────────────┐
│  React Frontend │
│  - AudioRecorder│
│  - FileUpload   │
└────────┬────────┘
         │
         │ POST /api/predict/
         │ FormData { audio: Blob }
         ▼
┌─────────────────┐
│  Django Backend │
│  - PredictView  │
│  - Auth Check   │
└────────┬────────┘
         │
         │ Save File
         ▼
┌─────────────────┐
│  File System    │
│  - Temp File    │
└────────┬────────┘
         │
         │ Audio Processing
         ▼
┌─────────────────┐
│  Audio Service  │
│  1. Convert     │
│     webm → wav  │
│  2. Load        │
│     librosa     │
│  3. Mask        │
│     silence     │
│  4. Window      │
│     6,144 samps │
│  5. Features    │
│     29 features │
└────────┬────────┘
         │
         │ ML Prediction
         ▼
┌─────────────────┐
│  ML Model (SVM) │
│  - Normalize    │
│  - Predict      │
│  - Aggregate    │
└────────┬────────┘
         │
         │ Prediction Result
         ▼
┌─────────────────┐
│  Database       │
│  - Match Bird   │
│  - Save Log     │
└────────┬────────┘
         │
         │ Response
         ▼
┌─────────────────┐
│  React Frontend │
│  - ResultDisplay│
│  - Show Result  │
└─────────────────┘
```

### Authentication Data Flow

```
User Registration/Login
    │
    ▼
┌─────────────────┐
│  React Frontend │
│  - Login/Register│
│  - Form Submit  │
└────────┬────────┘
         │
         │ POST /api/register/ or /api/login/
         ▼
┌─────────────────┐
│  Django Backend │
│  - RegisterView │
│  - LoginView    │
│  - User Create  │
│  - Token Create │
└────────┬────────┘
         │
         │ Database Operation
         ▼
┌─────────────────┐
│  Database       │
│  - User Table   │
│  - Token Table  │
└────────┬────────┘
         │
         │ Token + User Data
         ▼
┌─────────────────┐
│  React Frontend │
│  - Store Token  │
│  - Store User   │
│  - Update State │
└─────────────────┘
```

### History Data Flow

```
User Request History
    │
    ▼
┌─────────────────┐
│  React Frontend │
│  - History View │
│  - API Call     │
└────────┬────────┘
         │
         │ GET /api/history/
         ▼
┌─────────────────┐
│  Django Backend │
│  - HistoryView  │
│  - User Filter  │
└────────┬────────┘
         │
         │ Database Query
         ▼
┌─────────────────┐
│  Database       │
│  - PredictionLog│
│  - User Filter  │
│  - Order DESC   │
└────────┬────────┘
         │
         │ Serialized Data
         ▼
┌─────────────────┐
│  React Frontend │
│  - History View │
│  - Display List │
└─────────────────┘
```

### Enrichment Data Flow

```
Admin Command
    │
    ▼
┌─────────────────┐
│  Management Cmd │
│  - enrich_birds │
│  - Bird Query   │
└────────┬────────┘
         │
         │ External API
         ▼
┌─────────────────┐
│  Wikipedia API  │
│  - Summary      │
│  - Images       │
└────────┬────────┘
         │
         │
         ▼
┌─────────────────┐
│  Wikidata API   │
│  - QID Search   │
│  - Properties   │
│  - Labels       │
└────────┬────────┘
         │
         │ Data Parsing
         ▼
┌─────────────────┐
│  Database       │
│  - Bird Update  │
│  - Data Store   │
└─────────────────┘
```

---

## Data Flow Summary

### Key Data Flows

1. **Authentication Flow**: User → Frontend → API → Backend → Database → Token → Frontend
2. **Prediction Flow**: User → Frontend → API → Backend → Audio Processing → ML Model → Database → Response → Frontend
3. **History Flow**: User → Frontend → API → Backend → Database → Response → Frontend
4. **Enrichment Flow**: Admin → Command → External API → Data Parsing → Database

### Data Transformations

1. **Audio**: WebM/MP3 → WAV → NumPy Array → Features → Prediction
2. **User Data**: Form Data → Serializer → Database → JSON → Frontend
3. **Bird Data**: External API → Parsing → Database → Serializer → JSON → Frontend
4. **Prediction Data**: ML Model → Aggregation → Database → Serializer → JSON → Frontend

### Data Storage

1. **User Data**: SQLite (User table)
2. **Bird Data**: SQLite (Bird table)
3. **Prediction Data**: SQLite (PredictionLog table)
4. **ML Artifacts**: File System (svm.sav, train.csv)
5. **Audio Files**: File System (temporary storage)

---

This data flow diagram documentation provides comprehensive coverage of all data flows in the Bird Sound Recognition System.


# Bird Sound Recognition System - Complete Documentation

## Table of Contents
1. [Overview](#overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Data Flow Diagram](#data-flow-diagram)
4. [ER Diagram](#er-diagram)
5. [Methodology](#methodology)
6. [Code Snippets](#code-snippets)
7. [Validation Methods](#validation-methods)
8. [Test Cases](#test-cases)
9. [Related References](#related-references)

---

## Overview

### Project Description
Bird Sound Recognition System is a web-based application that identifies bird species from audio recordings. The system uses machine learning (SVM) to analyze audio features and match them against a trained model, providing users with species identification, confidence scores, and detailed bird information.

### Key Features
- **Audio Processing**: Record or upload audio files (supports multiple formats)
- **Machine Learning Prediction**: SVM-based classification model
- **User Authentication**: Secure login/registration system
- **Prediction History**: Track all user predictions
- **Bird Information Enrichment**: Wikipedia/Wikidata integration for images, habitat, diet, and notes
- **Modern UI**: Apple-inspired design with responsive layout

### Technology Stack
- **Backend**: Django 5.2.8, Django REST Framework
- **Frontend**: React 18.2, React Router
- **Machine Learning**: scikit-learn, librosa, pandas, numpy
- **Audio Processing**: librosa, pydub, ffmpeg
- **Database**: SQLite (development)
- **Authentication**: Token-based authentication

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   React App  │  │  AudioRecorder│  │  FileUpload  │         │
│  │   (Frontend) │  │   Component   │  │  Component   │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                  │                  │                  │
│  ┌──────┴──────────────────┴──────────────────┴──────┐         │
│  │           API Service (axios)                      │         │
│  │  - Authentication (login/register)                 │         │
│  │  - Audio Upload                                    │         │
│  │  - History Fetch                                   │         │
│  └──────────────────────┬─────────────────────────────┘         │
└─────────────────────────┼───────────────────────────────────────┘
                          │ HTTPS/REST API
┌─────────────────────────┼───────────────────────────────────────┐
│                    API GATEWAY LAYER                            │
│  ┌──────────────────────────────────────────────────────┐      │
│  │         Django REST Framework                        │      │
│  │  - URL Routing                                       │      │
│  │  - Authentication (Token-based)                      │      │
│  │  - CORS Handling                                     │      │
│  │  - Request Validation                                │      │
│  └──────────────────────┬───────────────────────────────┘      │
└─────────────────────────┼───────────────────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────────────────┐
│                   BUSINESS LOGIC LAYER                          │
│  ┌──────────────────────────────────────────────────────┐      │
│  │              Views (API Endpoints)                   │      │
│  │  - /api/register/  - User registration              │      │
│  │  - /api/login/     - User authentication            │      │
│  │  - /api/predict/   - Audio prediction               │      │
│  │  - /api/history/   - Prediction history             │      │
│  │  - /api/user/      - User information               │      │
│  └──────────────────────┬───────────────────────────────┘      │
│                         │                                       │
│  ┌──────────────────────┴───────────────────────────────┐      │
│  │         Prediction Service                           │      │
│  │  - Audio conversion (webm → wav)                     │      │
│  │  - Feature extraction (melspectrogram, chroma)       │      │
│  │  - Model prediction (SVM)                            │      │
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
│  └──────────────────────────────────────────────────────┘      │
│                         │                                       │
│  ┌──────────────────────┴───────────────────────────────┐      │
│  │              ML Artifacts                            │      │
│  │  - svm.sav (trained model)                           │      │
│  │  - train.csv (feature schema)                        │      │
│  └──────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

### Component Description

#### Frontend (React)
- **Components**: AudioRecorder, FileUpload, ResultDisplay, Login, Register, History
- **State Management**: React Context API (AuthContext)
- **Routing**: React Router with protected routes
- **API Communication**: Axios with token authentication

#### Backend (Django)
- **Views**: API endpoints handling HTTP requests
- **Serializers**: Data validation and transformation
- **Models**: Database schema definitions
- **Services**: Business logic (prediction, enrichment)

#### Machine Learning
- **Model**: SVM classifier (scikit-learn)
- **Features**: Spectral centroid, chroma features
- **Processing**: Librosa for audio analysis

---

## Data Flow Diagram

```
┌─────────────┐
│   User      │
└──────┬──────┘
       │
       │ 1. Record/Upload Audio
       ▼
┌─────────────────────────────────┐
│   React Frontend                │
│   - AudioRecorder/FileUpload    │
└──────┬──────────────────────────┘
       │
       │ 2. POST /api/predict/ (FormData)
       ▼
┌─────────────────────────────────┐
│   Django Backend                │
│   - PredictView                 │
│   - Authentication Check        │
└──────┬──────────────────────────┘
       │
       │ 3. Save audio file
       ▼
┌─────────────────────────────────┐
│   Audio Processing              │
│   - Convert webm → wav (ffmpeg) │
│   - Load audio (librosa)        │
└──────┬──────────────────────────┘
       │
       │ 4. Extract features
       ▼
┌─────────────────────────────────┐
│   Feature Extraction            │
│   - Melspectrogram              │
│   - Spectral Centroid           │
│   - Chroma Features             │
└──────┬──────────────────────────┘
       │
       │ 5. Predict
       ▼
┌─────────────────────────────────┐
│   ML Model (SVM)                │
│   - Load model (svm.sav)        │
│   - Predict species             │
│   - Calculate confidence        │
└──────┬──────────────────────────┘
       │
       │ 6. Match bird in database
       ▼
┌─────────────────────────────────┐
│   Database Query                │
│   - Search Bird by binomial     │
│   - Get bird details            │
└──────┬──────────────────────────┘
       │
       │ 7. Save prediction
       ▼
┌─────────────────────────────────┐
│   PredictionLog                 │
│   - Store prediction            │
│   - Link to user & bird         │
└──────┬──────────────────────────┘
       │
       │ 8. Return response
       ▼
┌─────────────────────────────────┐
│   JSON Response                 │
│   - Prediction result           │
│   - Bird information            │
│   - Confidence score            │
└──────┬──────────────────────────┘
       │
       │ 9. Display result
       ▼
┌─────────────────────────────────┐
│   ResultDisplay Component       │
│   - Show prediction             │
│   - Display bird info           │
│   - Show images                 │
└─────────────────────────────────┘
```

### Data Flow Steps

1. **User Input**: User records audio or uploads file
2. **Frontend Processing**: Audio converted to Blob, sent as FormData
3. **Backend Reception**: Django receives file, validates authentication
4. **File Storage**: Temporary file saved to media/predict_uploads/
5. **Audio Conversion**: WebM converted to WAV (if needed)
6. **Feature Extraction**: Audio analyzed for spectral features
7. **ML Prediction**: SVM model predicts species
8. **Database Lookup**: Match predicted species with Bird records
9. **Logging**: Save prediction to PredictionLog
10. **Response**: Return prediction and bird details to frontend
11. **Display**: Frontend renders result with images and information

---

## ER Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         ER DIAGRAM                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────┐
│      User           │
│  (Django Auth)      │
├─────────────────────┤
│ PK id               │
│    username         │
│    email            │
│    password (hash)  │
│    first_name       │
│    last_name        │
└──────────┬──────────┘
           │
           │ 1:N
           │
           ▼
┌─────────────────────┐
│   PredictionLog     │
├─────────────────────┤
│ PK id               │
│ FK user_id          │──────┐
│ FK matched_bird_id  │──┐   │
│    created_at       │  │   │
│    filename         │  │   │
│    predicted_label  │  │   │
│    confidence       │  │   │
│    top_votes_json   │  │   │
└─────────────────────┘  │   │
                         │   │
                         │   │ N:1
                         │   │
                         │   │
┌─────────────────────┐  │   │
│      Bird           │  │   │
├─────────────────────┤  │   │
│ PK id               │◄─┘   │
│    genus            │      │
│    species          │      │
│ UK binomial         │      │
│    english_cname    │      │
│    habitat          │      │
│    diet             │      │
│    notes            │      │
│    image_url_1      │      │
│    image_credit_1   │      │
│    image_url_2      │      │
│    image_credit_2   │      │
│    image_url_3      │      │
│    image_credit_3   │      │
│    wikipedia_title  │      │
│    wikipedia_url    │      │
│    wikidata_qid     │      │
└─────────────────────┘      │
                             │
                             │
Relationships:               │
- User 1:N PredictionLog     │
- Bird 1:N PredictionLog     │
- User has many Predictions  │
- Bird can have many Predictions
```

### Entity Descriptions

#### User
- Django's built-in User model
- Stores user authentication information
- Linked to PredictionLog via foreign key

#### Bird
- Stores bird species information
- Includes scientific name (binomial), common name
- Enrichment fields: habitat, diet, notes, images
- Wikipedia/Wikidata integration fields

#### PredictionLog
- Stores each prediction made by users
- Links user and bird (if matched)
- Stores prediction details: label, confidence, votes
- Timestamped for history tracking

---

## Methodology

### Machine Learning Pipeline

#### 1. Data Preparation
```
Audio Files → Preprocessing → Feature Extraction → Training Data
```

**Steps:**
- Load audio files from dataset
- Resample to 22,050 Hz
- Apply masking to remove silence
- Extract features (spectral centroid, chroma)
- Create windows of 6,144 samples each
- Label with species information

#### 2. Feature Extraction
```python
Features:
- Spectral Centroid:
  * Mean, Std, Percentiles (10th, 50th, 90th)
- Chroma Features:
  * Mean and Std for each of 12 chroma bins
```

#### 3. Model Training
- **Algorithm**: Support Vector Machine (SVM)
- **Kernel**: Linear
- **Preprocessing**: StandardScaler
- **Train/Test Split**: 80/20 (stratified by files)
- **Evaluation**: Accuracy score, classification report

#### 4. Prediction Process
1. Receive audio file
2. Convert format if needed (webm → wav)
3. Load and preprocess audio
4. Extract features
5. Normalize features
6. Predict using SVM model
7. Aggregate predictions across windows
8. Return top prediction with confidence

### Audio Processing Methodology

#### Audio Loading
- **Target Sample Rate**: 22,050 Hz
- **Channels**: Mono
- **Format Support**: WAV, FLAC, MP3, M4A, OGG, WebM (via conversion)

#### Masking Algorithm
1. Compute melspectrogram
2. Find center point (maximum energy)
3. Calculate threshold (M/20.0)
4. Create mask for frames above threshold
5. Apply mask to audio signal
6. Return masked audio

#### Windowing
- **Window Size**: 6,144 samples (~0.279 seconds)
- **Hop Length**: 512 samples
- **Method**: Non-overlapping windows
- **Minimum Windows**: 1 (for prediction)

### Enrichment Methodology

#### Wikipedia Integration
1. Search by common name (if available)
2. Fallback to binomial name
3. Extract summary text (notes)
4. Extract images
5. Store Wikipedia URL

#### Wikidata Integration
1. Search for QID using binomial name
2. Fetch properties:
   - P18: Images
   - P141: Habitat
   - P2078/P2079: Diet
3. Resolve item references to labels
4. Store in database

---

## Code Snippets

### 1. Audio Prediction Endpoint

```python
# bird_backend/birds/views.py
class PredictView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request, *args, **kwargs):
        f = request.FILES.get("audio")
        if not f:
            return Response({"detail": "No 'audio' file provided."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Save to temp path
        media_root = Path(settings.MEDIA_ROOT)
        predict_dir = media_root / "predict_uploads"
        predict_dir.mkdir(parents=True, exist_ok=True)
        temp_name = f"{uuid.uuid4().hex}_{f.name}"
        temp_path = predict_dir / temp_name
        
        with temp_path.open("wb") as out:
            for chunk in f.chunks():
                out.write(chunk)

        try:
            # Run prediction
            pred = predict_audio_file(temp_path)
            label = pred.get("pred_top")
            
            # Match bird in database
            matched = Bird.objects.filter(binomial__iexact=label).first()
            
            # Save prediction log
            PredictionLog.objects.create(
                user=request.user,
                filename=f.name,
                predicted_label=label,
                confidence=pred.get("confidence", 0.0),
                top_votes_json=pred.get("votes", {}),
                matched_bird=matched,
            )

            return Response({
                "prediction": {
                    "label": label,
                    "confidence": pred["confidence"],
                    "votes": pred["votes"],
                    "windows": pred.get("windows", 0),
                },
                "bird": BirdSerializer(matched).data if matched else None,
                "ambiguous": (matched is None and " " not in label),
            })
        finally:
            temp_path.unlink(missing_ok=True)
```

### 2. Audio Processing and Feature Extraction

```python
# bird_backend/birds/predict_service.py
def _load_audio_masked(audio_path: Path) -> np.ndarray:
    # Convert to wav if needed
    converted_path = _convert_audio_to_wav(audio_path)
    
    # Load audio
    y, sr = librosa.load(converted_path, sr=TARGET_SR, mono=True)
    
    if y.size == 0:
        return y
    
    # Create melspectrogram
    sg = lf.melspectrogram(y=y, sr=TARGET_SR, hop_length=HOP, n_mels=N_MELS)
    
    # Find center point (maximum energy)
    centerpoint = int(np.argmax(sg.mean(axis=0)))
    M = float(sg[:, centerpoint].mean())
    
    # Create mask (frames above threshold)
    mask_frames = sg.mean(axis=0) >= (M / 20.0)
    audio_mask = np.zeros_like(y, dtype=bool)
    
    for i, keep in enumerate(mask_frames):
        s = i * HOP
        e = min((i + 1) * HOP, len(y))
        audio_mask[s:e] = keep
    
    return y[audio_mask] if audio_mask.any() else y

def _extract_features(window: np.ndarray) -> dict:
    # Spectral Centroid
    sc = lf.spectral_centroid(y=window, sr=TARGET_SR, hop_length=HOP)
    scv = sc[0] if sc.ndim == 2 else sc
    
    # Chroma Features
    chroma = lf.chroma_stft(y=window, sr=TARGET_SR, hop_length=HOP)
    
    feats = {
        "sc_mean": float(np.mean(scv)),
        "sc_std": float(np.std(scv)),
        "sc_p10": float(np.percentile(scv, 10)),
        "sc_p50": float(np.percentile(scv, 50)),
        "sc_p90": float(np.percentile(scv, 90)),
    }
    
    # Chroma features (12 bins)
    for k in range(chroma.shape[0]):
        v = chroma[k]
        feats[f"ch{k}_mean"] = float(np.mean(v))
        feats[f"ch{k}_std"] = float(np.std(v))
    
    return feats
```

### 3. Model Prediction

```python
# bird_backend/birds/predict_service.py
def predict_audio_file(audio_path: Path) -> dict:
    # Ensure model is loaded
    _ensure_model_loaded()
    
    if _MODEL is None or _FEATURE_COLS is None:
        raise RuntimeError("Model not loaded.")
    
    # Load and mask audio
    y = _load_audio_masked(audio_path)
    
    # Create windows
    chunks = _window_signal(y, WIN_SAMPLES)
    if not chunks:
        return {"windows": 0, "pred_top": None, "confidence": 0.0, "votes": {}}
    
    # Extract features
    X = _featurize_windows(chunks).values
    
    # Predict
    preds = _MODEL.predict(X)
    counts = Counter(preds)
    
    if not counts:
        return {"windows": len(chunks), "pred_top": None, "confidence": 0.0, "votes": {}}
    
    # Get top prediction
    pred_top, votes = counts.most_common(1)[0]
    
    return {
        "windows": len(chunks),
        "pred_top": str(pred_top),
        "confidence": votes / len(preds),
        "votes": dict(sorted(counts.items(), key=lambda x: -x[1])[:5]),
    }
```

### 4. Frontend API Service

```javascript
// react-frontend/src/services/api.js
export const uploadAudio = async (audioBlob, fileName) => {
  const formData = new FormData();
  formData.append('audio', audioBlob, fileName);

  const response = await api.post('/api/predict/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  if (response.data && response.data.prediction) {
    return {
      prediction: response.data.prediction,
      bird: response.data.bird,
      ambiguous: response.data.ambiguous || false,
    };
  } else {
    throw new Error(response.data?.message || 'Prediction failed');
  }
};
```

### 5. Authentication

```python
# bird_backend/birds/views.py
class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {'detail': 'Invalid credentials.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        token, _ = Token.objects.get_or_create(user=user)
        login(request, user)
        
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })
```

### 6. Wikidata Enrichment

```python
# bird_backend/birds/management/commands/enrich_birds.py
def wd_get_property_labels(qid: str, property_ids: List[str]) -> Dict[str, str]:
    """Get labels for specific Wikidata properties."""
    params = {
        "action": "wbgetentities",
        "ids": qid,
        "props": "claims",
        "languages": "en",
        "format": "json",
    }
    r = SESSION.get(WIKIDATA_API, params=params, timeout=20)
    data = r.json()
    ent = data.get("entities", {}).get(qid, {})
    claims = ent.get("claims", {})
    
    result = {}
    for prop_id in property_ids:
        if prop_id not in claims:
            continue
        snak = claims[prop_id][0]
        mainsnak = snak.get("mainsnak", {})
        if mainsnak.get("datatype") == "wikibase-item":
            item_id = mainsnak.get("datavalue", {}).get("value", {}).get("id")
            if item_id:
                # Get label for referenced item
                label = _get_wikidata_label(item_id)
                if label:
                    result[prop_id] = label
    
    return result
```

---

## Validation Methods

### 1. Input Validation

#### Audio File Validation
```python
# File type validation
- Accepted formats: audio/* (webm, wav, flac, mp3, m4a, ogg)
- File size: Limited by Django settings
- Required field: 'audio' in request.FILES
```

#### User Input Validation
```python
# Registration validation
- Username: Required, unique
- Email: Required, unique, valid email format
- Password: Required, minimum length (enforced by Django)

# Login validation
- Username: Required
- Password: Required
```

### 2. Authentication Validation

```python
# Token-based authentication
- Token must be present in Authorization header
- Token format: "Token <token_key>"
- Token must be valid and not expired
- User must be authenticated for protected endpoints
```

### 3. Data Validation

#### Model Validation
```python
# Bird model
- binomial: Required, unique, max_length=140
- genus: Required, max_length=64
- species: Required, max_length=64
- All URL fields: Valid URL format
- All text fields: Max length constraints

# PredictionLog model
- user: Required (ForeignKey)
- filename: Required, max_length=255
- predicted_label: Required, max_length=140
- confidence: Required, FloatField (0.0-1.0)
- top_votes_json: Required, JSONField
```

#### Serializer Validation
```python
# BirdSerializer
- Validates all fields according to model constraints
- Ensures URL fields are valid URLs
- Validates text field lengths

# UserSerializer
- Validates username, email format
- Ensures required fields are present
```

### 4. Audio Processing Validation

```python
# Audio validation
- File must be readable by librosa
- Audio must have non-zero duration
- Sample rate conversion validation
- Format conversion validation (webm → wav)
```

### 5. ML Model Validation

```python
# Model validation
- Model file (svm.sav) must exist
- Training CSV (train.csv) must exist
- Feature columns must match training data
- Input features must be valid numbers
- Prediction must return valid species label
```

### 6. API Response Validation

```python
# Response structure validation
{
    "prediction": {
        "label": str,
        "confidence": float (0.0-1.0),
        "votes": dict,
        "windows": int
    },
    "bird": {
        "binomial": str,
        "english_cname": str,
        "habitat": str,
        "diet": str,
        "notes": str,
        "image_url_1": str,
        ...
    } | None,
    "ambiguous": bool
}
```

---

## Test Cases

### 1. Authentication Tests

#### Test Case 1.1: User Registration
```python
# Test: Successful registration
POST /api/register/
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
}
Expected: 201 Created
Response: {
    "token": "...",
    "user": {"id": 1, "username": "testuser", ...}
}

# Test: Duplicate username
POST /api/register/
{
    "username": "testuser",  # Already exists
    "email": "test2@example.com",
    "password": "testpass123"
}
Expected: 400 Bad Request
Response: {"detail": "Username already exists."}

# Test: Missing fields
POST /api/register/
{
    "username": "testuser"
    # Missing email and password
}
Expected: 400 Bad Request
Response: {"detail": "Username, email, and password are required."}
```

#### Test Case 1.2: User Login
```python
# Test: Successful login
POST /api/login/
{
    "username": "testuser",
    "password": "testpass123"
}
Expected: 200 OK
Response: {
    "token": "...",
    "user": {"id": 1, "username": "testuser", ...}
}

# Test: Invalid credentials
POST /api/login/
{
    "username": "testuser",
    "password": "wrongpassword"
}
Expected: 401 Unauthorized
Response: {"detail": "Invalid credentials."}
```

#### Test Case 1.3: Protected Endpoint Access
```python
# Test: Access without token
POST /api/predict/
Headers: {}
Expected: 401 Unauthorized

# Test: Access with valid token
POST /api/predict/
Headers: {"Authorization": "Token <valid_token>"}
Expected: 200 OK or 400 Bad Request (if no audio file)
```

### 2. Audio Prediction Tests

#### Test Case 2.1: Audio Upload
```python
# Test: Successful prediction
POST /api/predict/
Headers: {"Authorization": "Token <token>"}
Body: FormData with audio file
Expected: 200 OK
Response: {
    "prediction": {
        "label": "Sylvia communis",
        "confidence": 0.85,
        "votes": {...},
        "windows": 10
    },
    "bird": {...},
    "ambiguous": false
}

# Test: No audio file
POST /api/predict/
Headers: {"Authorization": "Token <token>"}
Body: {}
Expected: 400 Bad Request
Response: {"detail": "No 'audio' file provided."}

# Test: Invalid audio file
POST /api/predict/
Headers: {"Authorization": "Token <token>"}
Body: FormData with invalid file
Expected: 500 Internal Server Error
Response: {"detail": "Prediction error: ..."}
```

#### Test Case 2.2: Audio Format Support
```python
# Test: WebM format (browser recording)
- Record audio in browser
- Submit as webm
- Expected: Converted to WAV, prediction successful

# Test: WAV format
- Upload WAV file
- Expected: Direct processing, prediction successful

# Test: FLAC format
- Upload FLAC file
- Expected: Direct processing, prediction successful

# Test: MP3 format
- Upload MP3 file
- Expected: Converted to WAV, prediction successful
```

#### Test Case 2.3: Prediction Accuracy
```python
# Test: High confidence prediction
- Use known bird audio
- Expected: Confidence > 0.7, correct species

# Test: Low confidence prediction
- Use unclear/ambiguous audio
- Expected: Confidence < 0.5, may be ambiguous

# Test: No prediction (audio too short)
- Use very short audio clip
- Expected: {"prediction": {"label": None}, "message": "Audio too short..."}
```

### 3. Bird Database Tests

#### Test Case 3.1: Bird Matching
```python
# Test: Exact binomial match
- Predict "Sylvia communis"
- Database has "Sylvia communis"
- Expected: matched_bird is not None

# Test: Case-insensitive match
- Predict "sylvia communis"
- Database has "Sylvia communis"
- Expected: matched_bird is not None

# Test: No match
- Predict "Unknown species"
- Database doesn't have this species
- Expected: matched_bird is None, ambiguous: true
```

#### Test Case 3.2: Bird Enrichment
```python
# Test: Wikipedia enrichment
python manage.py enrich_birds --from-wiki --limit 5
Expected: 
- Wikipedia summary fetched
- Images fetched
- Notes populated
- Wikipedia URL stored

# Test: Wikidata enrichment
- Run enrichment with Wikidata QID
- Expected:
- Habitat fetched (P141)
- Diet fetched (P2078/P2079)
- Images fetched (P18)

# Test: CSV enrichment
python manage.py enrich_birds --from-csv enrichment.csv
Expected:
- Habitat from CSV
- Diet from CSV
- Notes from CSV
- Images from CSV
```

### 4. History Tests

#### Test Case 4.1: Prediction History
```python
# Test: Get user history
GET /api/history/
Headers: {"Authorization": "Token <token>"}
Expected: 200 OK
Response: {
    "count": 5,
    "results": [
        {
            "id": 1,
            "created_at": "2025-11-11T12:00:00Z",
            "filename": "recording.webm",
            "predicted_label": "Sylvia communis",
            "confidence": 0.85,
            "bird": {...}
        },
        ...
    ]
}

# Test: History filtered by user
- User A makes prediction
- User B makes prediction
- User A requests history
- Expected: Only User A's predictions returned
```

### 5. Frontend Tests

#### Test Case 5.1: Audio Recording
```javascript
// Test: Start recording
- Click "Start Recording" button
- Expected: Microphone access requested, recording starts

// Test: Stop recording
- Click "Stop Recording" button
- Expected: Recording stops, audio preview shown

// Test: Submit recording
- Record audio, click "Submit for Analysis"
- Expected: Loading state, API call, result displayed
```

#### Test Case 5.2: File Upload
```javascript
// Test: File selection
- Click upload area, select audio file
- Expected: File preview shown, audio player displayed

// Test: Drag and drop
- Drag audio file onto upload area
- Expected: File accepted, preview shown

// Test: Invalid file type
- Try to upload non-audio file
- Expected: Error message, file rejected
```

#### Test Case 5.3: Result Display
```javascript
// Test: Prediction result
- Submit audio, receive prediction
- Expected: 
  - Species name displayed
  - Confidence score shown
  - Bird information displayed (if matched)
  - Images displayed (if available)

// Test: No bird match
- Submit audio, no database match
- Expected: Prediction shown, "No bird details found" message

// Test: History view
- Navigate to History page
- Expected: List of all user predictions
```

### 6. Error Handling Tests

#### Test Case 6.1: Network Errors
```python
# Test: Backend unavailable
- Frontend tries to call API
- Backend is down
- Expected: Error message "Unable to connect to server"

# Test: Timeout
- Large audio file upload
- Network timeout
- Expected: Error message, request fails gracefully
```

#### Test Case 6.2: Validation Errors
```python
# Test: Invalid token
- Request with invalid/expired token
- Expected: 401 Unauthorized, redirect to login

# Test: Missing required fields
- Registration without email
- Expected: 400 Bad Request, error message
```

#### Test Case 6.3: Model Errors
```python
# Test: Model file missing
- svm.sav not found
- Expected: RuntimeError with clear message

# Test: Feature mismatch
- Training CSV has different features
- Expected: RuntimeError during prediction
```

---

## Related References

### Technologies and Frameworks

#### Backend
- **Django**: https://www.djangoproject.com/
  - Version: 5.2.8
  - Documentation: https://docs.djangoproject.com/en/5.2/
  
- **Django REST Framework**: https://www.django-rest-framework.org/
  - Version: 3.15+
  - Documentation: https://www.django-rest-framework.org/api-guide/
  
- **Django CORS Headers**: https://github.com/adamchainz/django-cors-headers
  - Version: 4.3.0+
  - Documentation: https://pypi.org/project/django-cors-headers/

#### Frontend
- **React**: https://react.dev/
  - Version: 18.2.0
  - Documentation: https://react.dev/learn
  
- **React Router**: https://reactrouter.com/
  - Version: 6.20.0
  - Documentation: https://reactrouter.com/en/main
  
- **Axios**: https://axios-http.com/
  - Version: 1.6.0
  - Documentation: https://axios-http.com/docs/intro

#### Machine Learning
- **scikit-learn**: https://scikit-learn.org/
  - Version: 1.5+
  - Documentation: https://scikit-learn.org/stable/
  - SVM Documentation: https://scikit-learn.org/stable/modules/svm.html
  
- **librosa**: https://librosa.org/
  - Version: 0.10.1+
  - Documentation: https://librosa.org/doc/latest/
  - Audio Loading: https://librosa.org/doc/latest/generated/librosa.load.html
  - Feature Extraction: https://librosa.org/doc/latest/feature.html
  
- **pandas**: https://pandas.pydata.org/
  - Version: 2.2+
  - Documentation: https://pandas.pydata.org/docs/
  
- **numpy**: https://numpy.org/
  - Version: 1.26+
  - Documentation: https://numpy.org/doc/

#### Audio Processing
- **pydub**: https://github.com/jiaaro/pydub
  - Version: 0.25.1+
  - Documentation: https://github.com/jiaaro/pydub
  
- **ffmpeg**: https://ffmpeg.org/
  - Installation: https://ffmpeg.org/download.html
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt-get install ffmpeg`

### APIs and Services

#### Wikipedia API
- **REST API**: https://en.wikipedia.org/api/rest_v1/
- **Page Summary**: https://en.wikipedia.org/api/rest_v1/page/summary/{title}
- **Documentation**: https://www.mediawiki.org/wiki/API:REST_API

#### Wikidata API
- **API Documentation**: https://www.wikidata.org/w/api.php
- **Entity Search**: https://www.wikidata.org/wiki/Special:ApiSandbox
- **Properties**:
  - P18: Image
  - P141: Habitat
  - P2078: Diet (food)
  - P2079: Diet (alternative)

### Machine Learning Resources

#### Audio Feature Extraction
- **Melspectrogram**: https://librosa.org/doc/latest/generated/librosa.feature.melspectrogram.html
- **Spectral Centroid**: https://librosa.org/doc/latest/generated/librosa.feature.spectral_centroid.html
- **Chroma Features**: https://librosa.org/doc/latest/generated/librosa.feature.chroma_stft.html

#### SVM Classifier
- **scikit-learn SVM**: https://scikit-learn.org/stable/modules/svm.html
- **Linear SVM**: https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html

### Database

#### SQLite
- **Documentation**: https://www.sqlite.org/docs.html
- **Django SQLite**: https://docs.djangoproject.com/en/5.2/ref/databases/#sqlite-notes

### Authentication

#### Token Authentication
- **Django REST Framework Tokens**: https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
- **Token Model**: https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication

### Web Standards

#### CORS
- **MDN CORS**: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
- **CORS Headers**: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Origin

#### MediaRecorder API
- **MDN MediaRecorder**: https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder
- **Browser Support**: https://caniuse.com/mediastream

### Development Tools

#### Python
- **Python Documentation**: https://docs.python.org/3/
- **Virtual Environments**: https://docs.python.org/3/tutorial/venv.html

#### Node.js
- **Node.js Documentation**: https://nodejs.org/en/docs
- **npm**: https://docs.npmjs.com/

### Data Sources

#### Bird Data
- **eBird**: https://ebird.org/
- **Xeno-canto**: https://xeno-canto.org/
- **Wikipedia**: https://www.wikipedia.org/
- **Wikidata**: https://www.wikidata.org/

### Research Papers and Articles

#### Audio Classification
- **Bird Sound Classification**: Various papers on bioacoustics
- **SVM for Audio Classification**: Machine learning applications in audio processing

#### Feature Extraction
- **Melspectrogram**: Standard in audio classification
- **Chroma Features**: Useful for pitch-based classification
- **Spectral Centroid**: Energy distribution analysis

---

## Additional Documentation

### Setup Instructions

#### Backend Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run migrations
cd bird_backend
python manage.py makemigrations
python manage.py migrate

# 3. Create superuser (optional)
python manage.py createsuperuser

# 4. Import bird data
python manage.py import_birds dataset/birdsong_metadata.csv

# 5. Enrich bird data (optional)
python manage.py enrich_birds --from-wiki --limit 10

# 6. Start server
python manage.py runserver
```

#### Frontend Setup
```bash
# 1. Install dependencies
cd react-frontend
npm install

# 2. Start development server
npm start
```

#### System Requirements
- **Python**: 3.8+
- **Node.js**: 16+
- **ffmpeg**: Required for audio conversion
- **Memory**: 2GB+ RAM recommended
- **Storage**: 1GB+ for model and dataset

### API Endpoints

#### Authentication Endpoints
- `POST /api/register/` - User registration
- `POST /api/login/` - User login
- `POST /api/logout/` - User logout
- `GET /api/user/` - Get current user info

#### Prediction Endpoints
- `POST /api/predict/` - Upload audio and get prediction
- `GET /api/history/` - Get user prediction history

#### Admin Endpoints
- `GET /admin/` - Django admin interface

### Configuration

#### Django Settings
- `ML_ARTIFACT_DIR`: Path to model files (svm.sav, train.csv)
- `MEDIA_ROOT`: Path for uploaded files
- `CORS_ALLOWED_ORIGINS`: Allowed frontend origins
- `DEBUG`: Debug mode (set to False in production)

#### Environment Variables
- `REACT_APP_API_URL`: Backend API URL (default: http://localhost:8000)

### Deployment Considerations

#### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up proper CORS configuration
- [ ] Use environment variables for secrets
- [ ] Set up SSL/HTTPS
- [ ] Configure static file serving
- [ ] Set up logging
- [ ] Configure backup strategy
- [ ] Set up monitoring

#### Security Considerations
- Token-based authentication
- CORS configuration
- Input validation
- File upload restrictions
- SQL injection prevention (Django ORM)
- XSS prevention (React)

---

## Conclusion

This documentation provides a comprehensive overview of the Bird Sound Recognition System, including architecture, data flow, methodology, code examples, test cases, and references. The system is designed to be scalable, maintainable, and user-friendly, with robust error handling and validation throughout.

For questions or issues, please refer to the related references or contact the development team.

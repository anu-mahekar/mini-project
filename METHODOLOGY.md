# Methodology Documentation

## Table of Contents
1. [System Methodology](#system-methodology)
2. [Machine Learning Methodology](#machine-learning-methodology)
3. [Audio Processing Methodology](#audio-processing-methodology)
4. [Data Enrichment Methodology](#data-enrichment-methodology)
5. [Authentication Methodology](#authentication-methodology)
6. [Prediction Methodology](#prediction-methodology)
7. [Data Flow Methodology](#data-flow-methodology)

---

## 1. System Methodology

### 1.1 Architecture Methodology

#### Three-Tier Architecture
```
┌─────────────────────────────────────────────────────────┐
│              PRESENTATION LAYER (React)                  │
│  - User Interface                                        │
│  - User Interaction                                      │
│  - State Management                                      │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP/REST API
┌──────────────────────┴──────────────────────────────────┐
│           APPLICATION LAYER (Django)                     │
│  - Business Logic                                        │
│  - API Endpoints                                         │
│  - Authentication                                        │
│  - Data Processing                                       │
└──────────────────────┬──────────────────────────────────┘
                       │ Database Queries
┌──────────────────────┴──────────────────────────────────┐
│                DATA LAYER (SQLite)                       │
│  - User Data                                             │
│  - Bird Data                                             │
│  - Prediction Logs                                       │
│  - ML Artifacts (svm.sav, train.csv)                    │
└─────────────────────────────────────────────────────────┘
```

**Methodology:**
- **Separation of Concerns**: Each layer has distinct responsibilities
- **API-Based Communication**: RESTful API between layers
- **Stateless Backend**: Django backend is stateless (scalable)
- **Token Authentication**: Token-based authentication for security

### 1.2 Development Methodology

#### Agile Development
- **Iterative Development**: Incremental feature development
- **User-Centered Design**: Focus on user experience
- **Continuous Integration**: Regular testing and integration
- **Documentation**: Comprehensive documentation at each stage

#### Testing Methodology
- **Unit Testing**: Individual component testing
- **Integration Testing**: End-to-end testing
- **User Testing**: User acceptance testing
- **Performance Testing**: Load and performance testing

---

## 2. Machine Learning Methodology

### 2.1 Training Methodology

#### Data Preparation
```
Audio Files → Preprocessing → Feature Extraction → Training Data → Model Training
```

**Steps:**
1. **Audio Loading**: Load audio files from dataset
2. **Preprocessing**: Resample to 22,050 Hz, convert to mono
3. **Masking**: Remove silence using melspectrogram-based masking
4. **Windowing**: Create windows of 6,144 samples each
5. **Feature Extraction**: Extract spectral centroid and chroma features
6. **Labeling**: Label with species information
7. **Train/Test Split**: 80/20 split (stratified by files)

#### Feature Extraction Methodology

**Spectral Centroid Features:**
```python
# Spectral Centroid (5 features)
sc = lf.spectral_centroid(y=window, sr=TARGET_SR, hop_length=HOP)
feats = {
    "sc_mean": float(np.mean(sc)),      # Mean
    "sc_std": float(np.std(sc)),         # Standard deviation
    "sc_p10": float(np.percentile(sc, 10)),  # 10th percentile
    "sc_p50": float(np.percentile(sc, 50)),  # 50th percentile (median)
    "sc_p90": float(np.percentile(sc, 90)),  # 90th percentile
}
```

**Chroma Features:**
```python
# Chroma Features (24 features: 12 bins × 2 stats)
chroma = lf.chroma_stft(y=window, sr=TARGET_SR, hop_length=HOP)
for k in range(12):  # 12 chroma bins
    v = chroma[k]
    feats[f"ch{k}_mean"] = float(np.mean(v))  # Mean
    feats[f"ch{k}_std"] = float(np.std(v))     # Standard deviation
```

**Total Features**: 5 (spectral centroid) + 24 (chroma) = 29 features

#### Model Training Methodology

**Algorithm**: Support Vector Machine (SVM)
```python
# SVM Pipeline
clf = make_pipeline(
    StandardScaler(with_mean=True),  # Feature normalization
    SVC(kernel="linear",             # Linear kernel
        probability=False,            # No probability estimates
        random_state=RANDOM_STATE,    # Reproducibility
        class_weight=None)            # Balanced classes
)
clf.fit(X_train, y_train_lab)
```

**Training Process:**
1. **Feature Normalization**: StandardScaler (mean=0, std=1)
2. **Model Training**: Linear SVM classifier
3. **Hyperparameters**: Linear kernel, no class weighting
4. **Evaluation**: Accuracy score, classification report
5. **Model Saving**: Pickle serialization (svm.sav)

#### Evaluation Methodology

**Metrics:**
- **Accuracy**: Overall classification accuracy
- **Precision**: Per-class precision
- **Recall**: Per-class recall
- **F1-Score**: Per-class F1-score
- **Classification Report**: Detailed per-class metrics

**Validation:**
- **Train/Test Split**: 80/20 split
- **Stratified Split**: Maintain class distribution
- **File-Based Split**: No data leakage between train/test

### 2.2 Prediction Methodology

#### Prediction Pipeline
```
Audio File → Conversion → Loading → Masking → Windowing → Feature Extraction → Normalization → Prediction → Aggregation
```

**Steps:**
1. **Audio Conversion**: Convert to WAV format (if needed)
2. **Audio Loading**: Load audio at 22,050 Hz, mono
3. **Audio Masking**: Remove silence using melspectrogram
4. **Windowing**: Create windows of 6,144 samples
5. **Feature Extraction**: Extract 29 features per window
6. **Feature Normalization**: Normalize using StandardScaler
7. **Prediction**: Predict species for each window
8. **Aggregation**: Vote across windows, return top prediction

#### Prediction Aggregation

**Voting Method:**
```python
# Prediction aggregation
preds = _MODEL.predict(X)  # Predictions for all windows
counts = Counter(preds)    # Count votes for each species
pred_top, votes = counts.most_common(1)[0]  # Get top prediction
confidence = votes / len(preds)  # Calculate confidence
```

**Methodology:**
- **Window-Based Prediction**: Each window gets a prediction
- **Voting**: Majority vote across windows
- **Confidence**: Percentage of windows voting for top prediction
- **Top Predictions**: Top 5 predictions with vote counts

---

## 3. Audio Processing Methodology

### 3.1 Audio Loading Methodology

#### Audio Conversion
```
Input Audio (webm/mp3/m4a/ogg) → Conversion (ffmpeg/pydub) → WAV → Loading (librosa)
```

**Conversion Process:**
1. **Format Detection**: Check file extension
2. **Direct Processing**: WAV/FLAC processed directly
3. **Conversion**: Other formats converted to WAV
4. **Sample Rate**: Converted to 22,050 Hz
5. **Channels**: Converted to mono (1 channel)
6. **Format**: Output as WAV format

#### Audio Loading
```python
# Audio loading
y, sr = librosa.load(audio_path, sr=TARGET_SR, mono=True)
```

**Methodology:**
- **Sample Rate**: Resample to 22,050 Hz (target sample rate)
- **Channels**: Convert to mono (single channel)
- **Format**: Load as numpy array (float32)
- **Normalization**: Automatic normalization by librosa

### 3.2 Audio Masking Methodology

#### Silence Removal
```
Audio Signal → Melspectrogram → Energy Analysis → Mask Creation → Masked Audio
```

**Masking Process:**
1. **Melspectrogram**: Compute melspectrogram (128 mel bands)
2. **Energy Analysis**: Calculate mean energy per frame
3. **Center Point**: Find frame with maximum energy
4. **Threshold**: Calculate threshold (M / 20.0 = 5% of maximum)
5. **Mask Creation**: Create mask for frames above threshold
6. **Mask Application**: Apply mask to audio signal

**Methodology:**
```python
# Audio masking
sg = lf.melspectrogram(y=y, sr=TARGET_SR, hop_length=HOP, n_mels=N_MELS)
centerpoint = int(np.argmax(sg.mean(axis=0)))  # Maximum energy frame
M = float(sg[:, centerpoint].mean())  # Mean energy at center
mask_frames = sg.mean(axis=0) >= (M / 20.0)  # Frames above threshold
audio_mask = np.zeros_like(y, dtype=bool)
for i, keep in enumerate(mask_frames):
    s = i * HOP
    e = min((i + 1) * HOP, len(y))
    audio_mask[s:e] = keep
return y[audio_mask] if audio_mask.any() else y
```

**Rationale:**
- **Remove Silence**: Remove silent portions of audio
- **Focus on Activity**: Focus on portions with bird sounds
- **Threshold**: 5% of maximum energy (conservative threshold)
- **Preserve Signal**: Preserve audio signal if no mask created

### 3.3 Windowing Methodology

#### Signal Windowing
```
Masked Audio → Windowing → Windows (6,144 samples each) → Feature Extraction
```

**Windowing Process:**
1. **Window Size**: 6,144 samples (~0.279 seconds at 22,050 Hz)
2. **Non-Overlapping**: Windows don't overlap
3. **Minimum Size**: Audio must be at least 6,144 samples
4. **Window Count**: Number of windows = len(audio) // WIN_SAMPLES

**Methodology:**
```python
# Windowing
def _window_signal(y: np.ndarray, W: int = WIN_SAMPLES) -> list[np.ndarray]:
    if y is None or y.size < W:
        return []  # Audio too short
    n = len(y) // W  # Number of windows
    return [y[i*W:(i+1)*W] for i in range(n)]  # Non-overlapping windows
```

**Rationale:**
- **Fixed Size**: Consistent window size for feature extraction
- **Non-Overlapping**: Avoid redundant information
- **Multiple Windows**: Multiple predictions for better accuracy
- **Aggregation**: Vote across windows for final prediction

### 3.4 Feature Extraction Methodology

#### Spectral Centroid Extraction
```
Audio Window → Spectral Centroid → Statistics (mean, std, percentiles)
```

**Spectral Centroid:**
- **Definition**: Center of mass of the spectrum
- **Calculation**: librosa.feature.spectral_centroid
- **Features**: Mean, std, 10th, 50th, 90th percentiles
- **Purpose**: Capture frequency distribution

#### Chroma Feature Extraction
```
Audio Window → Chroma STFT → 12 Chroma Bins → Statistics (mean, std)
```

**Chroma Features:**
- **Definition**: 12-dimensional chroma representation
- **Calculation**: librosa.feature.chroma_stft
- **Features**: Mean and std for each of 12 chroma bins
- **Purpose**: Capture pitch and harmonic content

**Total Features**: 5 (spectral centroid) + 24 (chroma) = 29 features

---

## 4. Data Enrichment Methodology

### 4.1 Wikipedia Enrichment Methodology

#### Wikipedia Summary Fetching
```
Bird Binomial → Wikipedia API → Summary Text → Notes Field
```

**Process:**
1. **Search Strategy**: Try common name first, then binomial
2. **API Call**: Wikipedia REST API (page summary)
3. **Data Extraction**: Extract summary text (notes)
4. **Image Extraction**: Extract images (if available)
5. **URL Storage**: Store Wikipedia URL

**Methodology:**
```python
# Wikipedia enrichment
def wiki_summary_for_title(title: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    url = WIKI_SUMMARY_API.format(title=quote(title))
    r = SESSION.get(url, timeout=20)
    j = r.json()
    display_title = j.get("title")
    extract = j.get("extract")  # Summary text
    img = j.get("originalimage", {}).get("source")  # Image URL
    return display_title, extract, img
```

### 4.2 Wikidata Enrichment Methodology

#### Wikidata Property Fetching
```
Bird Binomial → Wikidata Search → QID → Properties (P141, P2078, P18) → Labels
```

**Process:**
1. **QID Search**: Search for Wikidata QID using binomial
2. **Property Fetching**: Fetch properties (P141: habitat, P2078: diet, P18: images)
3. **Label Resolution**: Resolve item references to labels
4. **Data Storage**: Store habitat, diet, images

**Methodology:**
```python
# Wikidata enrichment
def wd_get_property_labels(qid: str, property_ids: List[str]) -> Dict[str, str]:
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
    
    # Extract properties
    for prop_id in property_ids:
        if prop_id in claims:
            # Resolve item references to labels
            item_id = claims[prop_id][0].get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id")
            if item_id:
                label = _get_wikidata_label(item_id)
                result[prop_id] = label
```

**Properties:**
- **P141**: Habitat (wikibase-item)
- **P2078**: Diet (wikibase-item)
- **P2079**: Diet (alternative, wikibase-item)
- **P18**: Images (commonsMedia)

### 4.3 CSV Enrichment Methodology

#### CSV Data Import
```
CSV File → Parsing → Data Validation → Database Update
```

**Process:**
1. **CSV Parsing**: Read CSV file using pandas
2. **Column Normalization**: Normalize column names (lowercase)
3. **Data Validation**: Validate required fields (binomial)
4. **Database Update**: Update or create Bird records
5. **Transaction**: Atomic transaction for data consistency

**Methodology:**
```python
# CSV enrichment
def apply_csv_enrichment(csv_path: Path) -> Tuple[int, int]:
    df = pd.read_csv(csv_path)
    df.columns = [c.strip().lower() for c in df.columns]
    
    if "binomial" not in df.columns:
        raise ValueError("CSV must include a 'binomial' column")
    
    for _, row in df.iterrows():
        binomial = str(row["binomial"]).strip()
        defaults = {}
        for col in ["habitat", "diet", "notes", "image_url_1", ...]:
            if col in df.columns and pd.notna(row[col]):
                defaults[col] = str(row[col]).strip()
        
        Bird.objects.update_or_create(
            binomial=binomial,
            defaults=defaults
        )
```

---

## 5. Authentication Methodology

### 5.1 Token-Based Authentication

#### Token Generation
```
User Registration/Login → Token Creation → Token Storage → Token Return
```

**Process:**
1. **User Creation**: Create user account
2. **Token Generation**: Generate or retrieve token
3. **Token Storage**: Store token in database
4. **Token Return**: Return token to client

**Methodology:**
```python
# Token generation
user = User.objects.create_user(username=username, email=email, password=password)
token, _ = Token.objects.get_or_create(user=user)
return Response({
    'token': token.key,
    'user': UserSerializer(user).data
})
```

#### Token Validation
```
API Request → Token Extraction → Token Validation → User Authentication
```

**Process:**
1. **Token Extraction**: Extract token from Authorization header
2. **Token Lookup**: Lookup token in database
3. **User Validation**: Validate user is active
4. **Request Processing**: Process request with authenticated user

**Methodology:**
```python
# Token validation (automatic via DRF)
class PredictView(APIView):
    permission_classes = [IsAuthenticated]
    # Token is automatically validated
    # request.user is set to authenticated user
```

### 5.2 Session Management

#### Session Creation
```
User Login → Session Creation → Session Storage → Session Return
```

**Process:**
1. **User Authentication**: Authenticate user credentials
2. **Session Creation**: Create Django session
3. **Session Storage**: Store session in database/cache
4. **Session Return**: Return session ID to client

**Methodology:**
```python
# Session creation
user = authenticate(username=username, password=password)
if user:
    login(request, user)  # Create session
    return Response({'user': UserSerializer(user).data})
```

#### Session Validation
```
API Request → Session Extraction → Session Validation → User Authentication
```

**Process:**
1. **Session Extraction**: Extract session ID from cookies
2. **Session Lookup**: Lookup session in database/cache
3. **User Validation**: Validate user is active
4. **Request Processing**: Process request with authenticated user

---

## 6. Prediction Methodology

### 6.1 Prediction Pipeline

#### Complete Prediction Flow
```
User Input → File Upload → Authentication → Audio Processing → Feature Extraction → ML Prediction → Database Matching → Response
```

**Detailed Steps:**
1. **User Input**: User records or uploads audio
2. **File Upload**: Audio file uploaded to server
3. **Authentication**: User authenticated via token
4. **File Storage**: File saved to temporary location
5. **Audio Conversion**: Convert to WAV format (if needed)
6. **Audio Loading**: Load audio at target sample rate
7. **Audio Masking**: Remove silence using melspectrogram
8. **Windowing**: Create windows of fixed size
9. **Feature Extraction**: Extract features from each window
10. **Feature Normalization**: Normalize features using StandardScaler
11. **ML Prediction**: Predict species for each window
12. **Vote Aggregation**: Aggregate predictions across windows
13. **Database Matching**: Match predicted species with Bird records
14. **Prediction Logging**: Save prediction to PredictionLog
15. **Response**: Return prediction and bird information

### 6.2 Database Matching Methodology

#### Species Matching
```
Predicted Label → Database Query → Bird Matching → Bird Information
```

**Matching Process:**
1. **Label Parsing**: Parse predicted label (binomial or species)
2. **Exact Match**: Try exact match with binomial
3. **Case-Insensitive Match**: Try case-insensitive match
4. **Species Match**: Try matching by species epithet
5. **Genus Hint**: Use genus hint if provided
6. **Ambiguous Flag**: Set ambiguous flag if no match

**Methodology:**
```python
# Database matching
if " " in label:
    # Already binomial (e.g., "Sylvia communis")
    binomial = label.strip()
    matched = Bird.objects.filter(binomial__iexact=binomial).first()
else:
    # Species epithet only (e.g., "communis")
    genus_hint = request.data.get("genus_hint", "").strip()
    if genus_hint:
        binomial = f"{genus_hint} {label}"
        matched = Bird.objects.filter(binomial__iexact=binomial).first()
    else:
        # Fallback: search by species epithet
        candidates = Bird.objects.filter(species__iexact=label)
        matched = candidates.first() if candidates.exists() else None
```

### 6.3 Prediction Logging Methodology

#### Prediction Storage
```
Prediction Result → Database Transaction → PredictionLog Creation → User/Bird Linking
```

**Process:**
1. **Transaction Start**: Start database transaction
2. **PredictionLog Creation**: Create PredictionLog record
3. **User Linking**: Link prediction to user
4. **Bird Linking**: Link prediction to bird (if matched)
5. **Data Storage**: Store prediction details (label, confidence, votes)
6. **Transaction Commit**: Commit transaction

**Methodology:**
```python
# Prediction logging
with transaction.atomic():
    plog = PredictionLog.objects.create(
        user=request.user,
        filename=f.name,
        predicted_label=label,
        confidence=float(pred.get("confidence", 0.0)),
        top_votes_json=pred.get("votes", {}),
        matched_bird=matched,
    )
```

---

## 7. Data Flow Methodology

### 7.1 Request Flow Methodology

#### API Request Flow
```
Client → HTTP Request → Django Middleware → URL Router → View → Service → Database → Response
```

**Detailed Flow:**
1. **Client Request**: HTTP request from React frontend
2. **CORS Middleware**: CORS headers added
3. **Authentication Middleware**: Token validation
4. **URL Router**: Route to appropriate view
5. **View Processing**: Business logic processing
6. **Service Layer**: Audio processing, ML prediction
7. **Database Query**: Database operations
8. **Response Serialization**: Data serialization
9. **Response Return**: JSON response to client

### 7.2 Response Flow Methodology

#### API Response Flow
```
Database → Serializer → View → Response → Client
```

**Detailed Flow:**
1. **Database Query**: Query database for data
2. **Serializer**: Serialize data to JSON
3. **View Response**: Create HTTP response
4. **Response Headers**: Add CORS headers
5. **Response Return**: Return JSON response
6. **Client Processing**: Process response in React
7. **State Update**: Update React state
8. **UI Update**: Update UI with new data

### 7.3 Error Flow Methodology

#### Error Handling Flow
```
Error Occurrence → Exception Handling → Error Logging → Error Response → Client Display
```

**Detailed Flow:**
1. **Error Occurrence**: Error occurs in processing
2. **Exception Handling**: Catch exception in try-catch
3. **Error Logging**: Log error to console/file
4. **Error Response**: Create error response
5. **Error Serialization**: Serialize error to JSON
6. **Error Return**: Return error response
7. **Client Handling**: Handle error in React
8. **Error Display**: Display error message to user

---

## Methodology Summary

### Machine Learning Methodology
- **Training**: Supervised learning with SVM
- **Features**: Spectral centroid (5) + Chroma (24) = 29 features
- **Evaluation**: Accuracy, precision, recall, F1-score
- **Prediction**: Window-based prediction with voting

### Audio Processing Methodology
- **Loading**: Resample to 22,050 Hz, mono
- **Masking**: Remove silence using melspectrogram
- **Windowing**: Non-overlapping windows of 6,144 samples
- **Features**: Spectral centroid and chroma features

### Data Enrichment Methodology
- **Wikipedia**: Fetch summaries and images
- **Wikidata**: Fetch habitat (P141), diet (P2078/P2079), images (P18)
- **CSV**: Import data from CSV files
- **Rate Limiting**: 0.6 seconds between API requests

### Authentication Methodology
- **Token-Based**: Django REST Framework tokens
- **Session-Based**: Django sessions (optional)
- **Protected Routes**: React Router guards
- **User Management**: Django User model

### Prediction Methodology
- **Pipeline**: Audio → Features → Prediction → Matching → Response
- **Aggregation**: Vote across windows for final prediction
- **Matching**: Database matching with case-insensitive search
- **Logging**: Store predictions in PredictionLog

### Data Flow Methodology
- **Request Flow**: Client → Middleware → View → Service → Database
- **Response Flow**: Database → Serializer → View → Response → Client
- **Error Flow**: Error → Exception → Logging → Response → Client

---

This methodology documentation provides comprehensive coverage of all methodologies used in the Bird Sound Recognition System.


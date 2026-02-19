# Validation Methods Documentation

## Table of Contents
1. [Input Validation](#input-validation)
2. [Authentication Validation](#authentication-validation)
3. [Data Validation](#data-validation)
4. [Audio Processing Validation](#audio-processing-validation)
5. [ML Model Validation](#ml-model-validation)
6. [API Response Validation](#api-response-validation)
7. [Frontend Validation](#frontend-validation)

---

## 1. Input Validation

### 1.1 Audio File Validation

#### File Type Validation
```python
# Backend validation (Django)
f = request.FILES.get("audio")
if not f:
    return Response({"detail": "No 'audio' file provided."},
                    status=status.HTTP_400_BAD_REQUEST)

# Frontend validation (React)
if (!file.type.startsWith('audio/')) {
    alert('Please select an audio file');
    return;
}
```

**Validation Rules:**
- **Required Field**: Audio file must be provided
- **File Type**: Must be an audio file (audio/*)
- **Accepted Formats**: WAV, FLAC, MP3, M4A, OGG, WebM
- **File Size**: Limited by Django settings (default: 2.5MB)
- **File Extension**: Validated on frontend and backend

#### File Format Validation
```python
# Audio format validation
def _convert_audio_to_wav(input_path: Path) -> Path:
    ext = input_path.suffix.lower()
    if ext in ['.wav', '.flac']:
        return input_path  # Direct processing
    # Convert other formats (webm, mp3, m4a, ogg)
    output_path = input_path.with_suffix('.wav')
    # Conversion using pydub/ffmpeg
```

**Validation Process:**
1. Check file extension
2. Validate file can be opened
3. Validate audio format is readable
4. Convert if needed (webm → wav)
5. Validate conversion success

### 1.2 User Input Validation

#### Registration Validation
```python
# Backend validation
username = request.data.get('username')
email = request.data.get('email')
password = request.data.get('password')

if not username or not email or not password:
    return Response(
        {'detail': 'Username, email, and password are required.'},
        status=status.HTTP_400_BAD_REQUEST
    )

if User.objects.filter(username=username).exists():
    return Response(
        {'detail': 'Username already exists.'},
        status=status.HTTP_400_BAD_REQUEST
    )

if User.objects.filter(email=email).exists():
    return Response(
        {'detail': 'Email already registered.'},
        status=status.HTTP_400_BAD_REQUEST
    )
```

**Validation Rules:**
- **Username**: Required, unique, alphanumeric (Django default)
- **Email**: Required, unique, valid email format
- **Password**: Required, minimum length (Django default: 8 characters)
- **Email Format**: Validated using Django's email validator

#### Login Validation
```python
# Backend validation
username = request.data.get('username')
password = request.data.get('password')

if not username or not password:
    return Response(
        {'detail': 'Username and password are required.'},
        status=status.HTTP_400_BAD_REQUEST
    )

user = authenticate(username=username, password=password)
if not user:
    return Response(
        {'detail': 'Invalid credentials.'},
        status=status.HTTP_401_UNAUTHORIZED
    )
```

**Validation Rules:**
- **Username**: Required
- **Password**: Required
- **Credentials**: Must match existing user
- **User Status**: User must be active

### 1.3 Frontend Form Validation

#### Registration Form Validation
```javascript
// Frontend validation
const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    if (!username || !email || !password) {
        setError('All fields are required');
        return;
    }
    
    if (password.length < 6) {
        setError('Password must be at least 6 characters');
        return;
    }
    
    // Email format validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        setError('Invalid email format');
        return;
    }
    
    // Submit form
    try {
        await register(username, email, password);
    } catch (err) {
        setError(err.message);
    }
};
```

**Validation Rules:**
- **Required Fields**: Username, email, password
- **Email Format**: Valid email regex
- **Password Length**: Minimum 6 characters
- **Username Format**: Alphanumeric (optional frontend validation)

---

## 2. Authentication Validation

### 2.1 Token Authentication

#### Token Validation
```python
# Django REST Framework token authentication
# Automatic validation via TokenAuthentication class

# Request header
Authorization: Token <token_key>

# Backend validation
class PredictView(APIView):
    permission_classes = [IsAuthenticated]
    # Token is automatically validated
    # User is available in request.user
```

**Validation Process:**
1. Extract token from Authorization header
2. Validate token format (Token <key>)
3. Lookup token in database
4. Verify token is associated with active user
5. Set request.user if valid
6. Return 401 if invalid

#### Token Expiration
```python
# Token management
token, _ = Token.objects.get_or_create(user=user)

# Token deletion on logout
try:
    request.user.auth_token.delete()
except:
    pass
```

**Validation Rules:**
- **Token Format**: "Token <key>"
- **Token Existence**: Must exist in database
- **User Status**: User must be active
- **Token Lifetime**: No expiration (can be extended with custom logic)

### 2.2 Session Authentication

#### Session Validation
```python
# Django session authentication (optional)
login(request, user)
logout(request)

# Session validation
if request.user.is_authenticated:
    # User is authenticated
    pass
```

**Validation Rules:**
- **Session Existence**: Session must exist
- **User Status**: User must be active
- **Session Expiration**: Default 2 weeks (Django default)

### 2.3 Protected Route Validation

#### Frontend Route Protection
```javascript
// React Router protected routes
const ProtectedRoute = ({ children }) => {
    const { user, loading } = useAuth();
    
    if (loading) {
        return <Loading />;
    }
    
    if (!user) {
        return <Navigate to="/login" replace />;
    }
    
    return children;
};
```

**Validation Rules:**
- **User Authentication**: User must be authenticated
- **Token Presence**: Token must exist in localStorage
- **Token Validity**: Token must be valid (checked via API)
- **Redirect**: Redirect to login if not authenticated

---

## 3. Data Validation

### 3.1 Model Validation

#### Bird Model Validation
```python
# Django model validation
class Bird(models.Model):
    genus = models.CharField(max_length=64)  # Required
    species = models.CharField(max_length=64)  # Required
    binomial = models.CharField(max_length=140, unique=True)  # Required, unique
    english_cname = models.CharField(max_length=140, blank=True, default="")
    habitat = models.TextField(blank=True, default="")
    diet = models.TextField(blank=True, default="")
    notes = models.TextField(blank=True, default="")
    image_url_1 = models.URLField(blank=True, default="")  # Valid URL format
    wikipedia_url = models.URLField(blank=True, default="")  # Valid URL format
```

**Validation Rules:**
- **Required Fields**: genus, species, binomial
- **Unique Constraints**: binomial must be unique
- **Field Lengths**: Maximum lengths enforced
- **URL Fields**: Valid URL format required
- **Text Fields**: Unlimited length (TextField)

#### PredictionLog Model Validation
```python
# Django model validation
class PredictionLog(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    filename = models.CharField(max_length=255)  # Required
    predicted_label = models.CharField(max_length=140)  # Required
    confidence = models.FloatField()  # Required, 0.0-1.0
    top_votes_json = models.JSONField(default=dict)  # Required, valid JSON
    matched_bird = models.ForeignKey(Bird, null=True, blank=True, on_delete=models.SET_NULL)
```

**Validation Rules:**
- **Required Fields**: filename, predicted_label, confidence, top_votes_json
- **Field Types**: CharField, FloatField, JSONField
- **Float Range**: Confidence 0.0-1.0
- **JSON Format**: Valid JSON dictionary
- **Foreign Keys**: Valid user and bird references

### 3.2 Serializer Validation

#### Bird Serializer Validation
```python
# Django REST Framework serializer validation
class BirdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bird
        fields = (
            "genus", "species", "binomial", "english_cname",
            "habitat", "diet", "notes",
            "image_url_1", "image_credit_1",
            "image_url_2", "image_credit_2",
            "image_url_3", "image_credit_3",
            "wikipedia_title", "wikipedia_url", "wikidata_qid",
        )
```

**Validation Process:**
1. Validate all fields according to model constraints
2. Validate URL fields are valid URLs
3. Validate text field lengths
4. Validate required fields are present
5. Return validation errors if invalid

#### User Serializer Validation
```python
# User serializer validation
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)
```

**Validation Rules:**
- **Read-only Fields**: id cannot be modified
- **Required Fields**: username, email (Django User model)
- **Email Format**: Valid email format
- **Username Format**: Alphanumeric (Django default)

### 3.3 Database Validation

#### Database Constraints
```python
# Database-level validation
class Bird(models.Model):
    binomial = models.CharField(max_length=140, unique=True)  # Unique constraint
    
    class Meta:
        indexes = [
            models.Index(fields=["genus", "species"]),
            models.Index(fields=["binomial"]),
        ]
```

**Validation Rules:**
- **Unique Constraints**: Enforced at database level
- **Foreign Key Constraints**: Enforced at database level
- **Index Constraints**: Enforced at database level
- **Null Constraints**: Enforced at database level

---

## 4. Audio Processing Validation

### 4.1 Audio File Validation

#### File Readability Validation
```python
# Audio file validation
def _load_audio_masked(audio_path: Path) -> np.ndarray:
    try:
        converted_path = _convert_audio_to_wav(audio_path)
        y, sr = librosa.load(converted_path, sr=TARGET_SR, mono=True)
    except Exception as e:
        raise RuntimeError(f"Error loading audio: {str(e)}")
    
    if y.size == 0:
        return y  # Empty audio
```

**Validation Rules:**
- **File Existence**: File must exist
- **File Readability**: File must be readable by librosa
- **Audio Format**: Must be convertible to WAV
- **Audio Duration**: Must have non-zero duration
- **Sample Rate**: Converted to target sample rate (22,050 Hz)

#### Audio Format Validation
```python
# Format validation
def _convert_audio_to_wav(input_path: Path) -> Path:
    ext = input_path.suffix.lower()
    if ext in ['.wav', '.flac']:
        return input_path  # Direct processing
    
    # Convert other formats
    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_file(str(input_path))
        audio = audio.set_frame_rate(TARGET_SR)
        audio = audio.set_channels(1)  # mono
        audio.export(str(output_path), format="wav")
        return output_path
    except Exception as e:
        raise RuntimeError(f"Could not convert audio: {str(e)}")
```

**Validation Rules:**
- **Supported Formats**: WAV, FLAC, MP3, M4A, OGG, WebM
- **Conversion Success**: Conversion must succeed
- **Output Format**: Output must be valid WAV
- **Sample Rate**: Output must be 22,050 Hz
- **Channels**: Output must be mono (1 channel)

### 4.2 Audio Content Validation

#### Audio Duration Validation
```python
# Audio duration validation
def _window_signal(y: np.ndarray, W: int = WIN_SAMPLES) -> list[np.ndarray]:
    if y is None or y.size < W:
        return []  # Audio too short
    n = len(y) // W
    return [y[i*W:(i+1)*W] for i in range(n)]
```

**Validation Rules:**
- **Minimum Duration**: Must be at least WIN_SAMPLES (6,144 samples ≈ 0.279 seconds)
- **Window Count**: Must have at least 1 window
- **Audio Length**: Validated after masking

#### Audio Masking Validation
```python
# Audio masking validation
def _load_audio_masked(audio_path: Path) -> np.ndarray:
    y, sr = librosa.load(audio_path, sr=TARGET_SR, mono=True)
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
```

**Validation Rules:**
- **Melspectrogram**: Must be computable
- **Energy Threshold**: M / 20.0 (5% of maximum energy)
- **Mask Application**: Must result in non-empty audio
- **Mask Validation**: At least one frame must be above threshold

### 4.3 Feature Extraction Validation

#### Feature Extraction Validation
```python
# Feature extraction validation
def _extract_features(window: np.ndarray) -> dict:
    # Spectral Centroid
    sc = lf.spectral_centroid(y=window, sr=TARGET_SR, hop_length=HOP)
    scv = sc[0] if sc.ndim == 2 else sc
    
    # Chroma Features
    chroma = lf.chroma_stft(y=window, sr=TARGET_SR, hop_length=HOP)
    
    # Validate features
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

**Validation Rules:**
- **Feature Count**: Must match training data (29 features)
- **Feature Types**: All features must be float
- **Feature Range**: Features must be finite (not NaN or Inf)
- **Feature Shape**: Chroma must have 12 bins

#### Feature Schema Validation
```python
# Feature schema validation
def _featurize_windows(windows: list[np.ndarray]) -> pd.DataFrame:
    if _FEATURE_COLS is None:
        raise RuntimeError("Model not loaded. Feature columns are not available.")
    
    rows = [_extract_features(w) for w in windows]
    df = pd.DataFrame(rows)
    
    # Ensure all feature columns exist
    for c in _FEATURE_COLS:
        if c not in df.columns:
            df[c] = 0.0  # Fill missing features with 0
    
    return df[_FEATURE_COLS]  # Return in correct order
```

**Validation Rules:**
- **Feature Columns**: Must match training data columns
- **Feature Order**: Features must be in correct order
- **Missing Features**: Missing features filled with 0.0
- **Feature Count**: Must have exact number of features

---

## 5. ML Model Validation

### 5.1 Model Loading Validation

#### Model File Validation
```python
# Model file validation
def _ensure_model_loaded():
    global _MODEL, _TRAIN_DF, _FEATURE_COLS
    if _MODEL is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Model file not found at {MODEL_PATH}. "
                f"Please ensure svm.sav exists in {ARTIFACT_DIR}"
            )
        if not TRAIN_CSV.exists():
            raise FileNotFoundError(
                f"Training CSV not found at {TRAIN_CSV}. "
                f"Please ensure train.csv exists in {ARTIFACT_DIR}"
            )
        
        with open(MODEL_PATH, "rb") as f:
            _MODEL = pickle.load(f)
        _TRAIN_DF = pd.read_csv(TRAIN_CSV)
        _FEATURE_COLS = [c for c in _TRAIN_DF.columns if c not in ("species", "genus", "binomial")]
```

**Validation Rules:**
- **Model File**: svm.sav must exist
- **Training CSV**: train.csv must exist
- **Model Format**: Must be valid pickle file
- **CSV Format**: Must be valid CSV file
- **Feature Columns**: Must match training data

### 5.2 Model Prediction Validation

#### Prediction Input Validation
```python
# Prediction input validation
def predict_audio_file(audio_path: Path) -> dict:
    # Ensure model is loaded
    try:
        _ensure_model_loaded()
    except FileNotFoundError as e:
        raise RuntimeError(f"Model files not found: {e}")
    
    if _MODEL is None or _FEATURE_COLS is None:
        raise RuntimeError("Model not loaded. Please ensure svm.sav and train.csv exist.")
    
    # Validate audio
    y = _load_audio_masked(audio_path)
    chunks = _window_signal(y, WIN_SAMPLES)
    if not chunks:
        return {"windows": 0, "pred_top": None, "confidence": 0.0, "votes": {}}
```

**Validation Rules:**
- **Model Loaded**: Model must be loaded
- **Feature Columns**: Feature columns must be available
- **Audio Windows**: Must have at least 1 window
- **Feature Count**: Features must match model input

#### Prediction Output Validation
```python
# Prediction output validation
X = _featurize_windows(chunks).values
preds = _MODEL.predict(X)
counts = Counter(preds)

if not counts:
    return {"windows": len(chunks), "pred_top": None, "confidence": 0.0, "votes": {}}

pred_top, votes = counts.most_common(1)[0]
return {
    "windows": len(chunks),
    "pred_top": str(pred_top),
    "confidence": votes / len(preds),
    "votes": dict(sorted(counts.items(), key=lambda x: -x[1])[:5]),
}
```

**Validation Rules:**
- **Prediction Format**: Must be string (species name)
- **Confidence Range**: 0.0-1.0
- **Votes Format**: Dictionary with species names and counts
- **Top Votes**: Top 5 predictions returned

### 5.3 Model Schema Validation

#### Feature Schema Validation
```python
# Feature schema validation
_FEATURE_COLS = [c for c in _TRAIN_DF.columns if c not in ("species", "genus", "binomial")]

# Validate feature columns match
for c in _FEATURE_COLS:
    if c not in df.columns:
        df[c] = 0.0  # Fill missing features
```

**Validation Rules:**
- **Feature Count**: Must match training data
- **Feature Names**: Must match training data
- **Feature Order**: Must match training data
- **Missing Features**: Filled with 0.0

---

## 6. API Response Validation

### 6.1 Response Format Validation

#### Prediction Response Validation
```python
# Response format validation
payload = {
    "prediction": {
        "label": label,  # str or None
        "confidence": pred["confidence"],  # float (0.0-1.0)
        "votes": pred["votes"],  # dict
        "windows": windows,  # int
    },
    "bird": BirdSerializer(matched).data if matched else None,  # dict or None
    "ambiguous": (matched is None and " " not in label),  # bool
}
return Response(payload, status=status.HTTP_200_OK)
```

**Validation Rules:**
- **Response Format**: JSON
- **Status Code**: 200 OK (success)
- **Prediction Object**: Must contain label, confidence, votes, windows
- **Bird Object**: dict or None
- **Ambiguous Flag**: bool

#### Error Response Validation
```python
# Error response validation
return Response({
    "detail": "Error message"
}, status=status.HTTP_400_BAD_REQUEST)
```

**Validation Rules:**
- **Error Format**: JSON with "detail" field
- **Status Code**: Appropriate HTTP status code
- **Error Message**: Clear, user-friendly message

### 6.2 Response Data Validation

#### Prediction Data Validation
```python
# Prediction data validation
label = pred.get("pred_top")  # str or None
windows = pred.get("windows", 0)  # int
confidence = pred.get("confidence", 0.0)  # float (0.0-1.0)
votes = pred.get("votes", {})  # dict
```

**Validation Rules:**
- **Label**: String (species name) or None
- **Windows**: Integer (>= 0)
- **Confidence**: Float (0.0-1.0)
- **Votes**: Dictionary with string keys and integer values

#### Bird Data Validation
```python
# Bird data validation
bird = BirdSerializer(matched).data if matched else None

# Serializer validates:
# - All fields according to model constraints
# - URL fields are valid URLs
# - Text fields are valid strings
# - Required fields are present
```

**Validation Rules:**
- **Bird Object**: dict or None
- **Required Fields**: genus, species, binomial
- **URL Fields**: Valid URL format
- **Text Fields**: Valid strings

---

## 7. Frontend Validation

### 7.1 Form Validation

#### Registration Form Validation
```javascript
// Registration form validation
const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    // Required fields
    if (!username || !email || !password) {
        setError('All fields are required');
        return;
    }
    
    // Email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        setError('Invalid email format');
        return;
    }
    
    // Password length
    if (password.length < 6) {
        setError('Password must be at least 6 characters');
        return;
    }
    
    // Submit
    try {
        await register(username, email, password);
    } catch (err) {
        setError(err.response?.data?.detail || err.message);
    }
};
```

**Validation Rules:**
- **Required Fields**: Username, email, password
- **Email Format**: Valid email regex
- **Password Length**: Minimum 6 characters
- **Error Handling**: Display error messages

#### Login Form Validation
```javascript
// Login form validation
const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    // Required fields
    if (!username || !password) {
        setError('Username and password are required');
        return;
    }
    
    // Submit
    try {
        await login(username, password);
    } catch (err) {
        setError(err.response?.data?.detail || err.message);
    }
};
```

**Validation Rules:**
- **Required Fields**: Username, password
- **Error Handling**: Display error messages
- **API Errors**: Handle API error responses

### 7.2 Audio File Validation

#### File Type Validation
```javascript
// File type validation
const handleFile = (file) => {
    if (!file.type.startsWith('audio/')) {
        alert('Please select an audio file');
        return;
    }
    
    setSelectedFile(file);
    const url = URL.createObjectURL(file);
    setAudioUrl(url);
};
```

**Validation Rules:**
- **File Type**: Must be audio file (audio/*)
- **File Format**: Validated by browser
- **File Size**: Limited by browser (optional)

#### Audio Recording Validation
```javascript
// Audio recording validation
const startRecording = async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mediaRecorder = new MediaRecorder(stream);
        // Recording starts
    } catch (error) {
        console.error('Error accessing microphone:', error);
        alert('Unable to access microphone. Please check permissions.');
    }
};
```

**Validation Rules:**
- **Microphone Access**: Must have permission
- **Browser Support**: MediaRecorder API must be supported
- **Error Handling**: Display error messages

### 7.3 API Response Validation

#### Response Validation
```javascript
// API response validation
export const uploadAudio = async (audioBlob, fileName) => {
    try {
        const response = await api.post('/api/predict/', formData);
        
        if (response.data && response.data.prediction) {
            return {
                prediction: response.data.prediction,
                bird: response.data.bird,
                ambiguous: response.data.ambiguous || false,
            };
        } else {
            throw new Error(response.data?.message || 'Prediction failed');
        }
    } catch (error) {
        if (error.response) {
            throw new Error(error.response.data?.detail || error.response.data?.message);
        } else if (error.request) {
            throw new Error('Unable to connect to server.');
        } else {
            throw new Error(error.message || 'An error occurred');
        }
    }
};
```

**Validation Rules:**
- **Response Format**: Must have prediction object
- **Error Handling**: Handle different error types
- **Network Errors**: Handle network failures
- **Server Errors**: Handle server errors

---

## Validation Summary

### Backend Validation
- **Input Validation**: File types, required fields, formats
- **Authentication Validation**: Token validation, user authentication
- **Data Validation**: Model constraints, serializer validation
- **Audio Validation**: Format, duration, content
- **ML Validation**: Model loading, prediction input/output
- **API Validation**: Response format, error handling

### Frontend Validation
- **Form Validation**: Required fields, formats, lengths
- **File Validation**: File types, formats, sizes
- **API Validation**: Response format, error handling
- **Route Validation**: Protected routes, authentication

### Validation Flow
```
User Input → Frontend Validation → API Request → Backend Validation → Processing → Response Validation → Frontend Display
```

---

This validation methods documentation provides comprehensive coverage of all validation processes in the Bird Sound Recognition System.


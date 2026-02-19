# System Architecture Documentation

## Architecture Overview

The Bird Sound Recognition System follows a **3-tier architecture**:
1. **Presentation Layer** (React Frontend)
2. **Application Layer** (Django Backend)
3. **Data Layer** (SQLite Database + ML Model)

## Detailed Architecture

### 1. Presentation Layer (Frontend)

```
┌─────────────────────────────────────────────────────────┐
│                  React Application                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Auth       │  │   Audio      │  │   History    │ │
│  │   Components │  │   Components │  │   Components │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│         │                  │                  │         │
│  ┌──────┴──────────────────┴──────────────────┴──────┐ │
│  │           AuthContext (State Management)           │ │
│  └──────┬─────────────────────────────────────────────┘ │
│         │                                                │
│  ┌──────┴─────────────────────────────────────────────┐ │
│  │           API Service (Axios)                      │ │
│  │  - Request Interceptors (Token)                    │ │
│  │  - Response Interceptors (401 Handling)            │ │
│  └──────────────────────┬──────────────────────────────┘ │
└─────────────────────────┼─────────────────────────────────┘
                          │
                          │ HTTPS/REST API
                          │
┌─────────────────────────┼─────────────────────────────────┐
│                  Application Layer                        │
│                  (Django Backend)                         │
└─────────────────────────┼─────────────────────────────────┘
```

**Components:**
- **AuthContext**: Global authentication state
- **Login/Register**: User authentication
- **AudioRecorder**: Browser audio recording
- **FileUpload**: File upload with drag & drop
- **ResultDisplay**: Prediction results display
- **History**: User prediction history
- **Navbar**: Navigation with user info

### 2. Application Layer (Backend)

```
┌─────────────────────────────────────────────────────────┐
│              Django REST Framework                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │              URL Router                           │ │
│  │  /api/register/  → RegisterView                   │ │
│  │  /api/login/     → LoginView                      │ │
│  │  /api/predict/   → PredictView                    │ │
│  │  /api/history/   → HistoryView                    │ │
│  │  /api/user/      → UserView                       │ │
│  └──────────────────┬────────────────────────────────┘ │
│                     │                                   │
│  ┌──────────────────┴────────────────────────────────┐ │
│  │              View Layer                           │ │
│  │  - Request Validation                             │ │
│  │  - Authentication Check                           │ │
│  │  - Business Logic Orchestration                   │ │
│  │  - Response Formatting                            │ │
│  └──────────────────┬────────────────────────────────┘ │
│                     │                                   │
│  ┌──────────────────┴────────────────────────────────┐ │
│  │              Service Layer                        │ │
│  │  - predict_service.py (ML Prediction)             │ │
│  │  - audio_preprocess.py (Audio Processing)         │ │
│  │  - enrich_birds.py (Data Enrichment)              │ │
│  └──────────────────┬────────────────────────────────┘ │
│                     │                                   │
│  ┌──────────────────┴────────────────────────────────┐ │
│  │              Serializer Layer                     │ │
│  │  - Data Validation                                │ │
│  │  - Data Transformation                            │ │
│  │  - Response Serialization                         │ │
│  └──────────────────┬────────────────────────────────┘ │
└─────────────────────┼───────────────────────────────────┘
                      │
┌─────────────────────┼───────────────────────────────────┐
│                  Data Layer                             │
└─────────────────────┼───────────────────────────────────┘
```

**Services:**
- **PredictService**: Audio prediction using ML model
- **AudioPreprocess**: Audio conversion and preprocessing
- **EnrichmentService**: Wikipedia/Wikidata data fetching

### 3. Data Layer

```
┌─────────────────────────────────────────────────────────┐
│                  Database (SQLite)                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐      ┌──────────────┐               │
│  │    User      │◄─────┤ PredictionLog│               │
│  │  (Auth)      │ 1:N  │              │               │
│  └──────────────┘      └──────┬───────┘               │
│                                │ N:1                   │
│                                ▼                       │
│                       ┌──────────────┐                │
│                       │     Bird     │                │
│                       │              │                │
│                       └──────────────┘                │
│                                                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│              ML Artifacts (File System)                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  - svm.sav (Trained SVM Model)                         │
│  - train.csv (Feature Schema)                          │
│  - test.csv (Test Data)                                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Technology Stack

### Frontend
- **React 18.2**: UI framework
- **React Router 6.20**: Routing
- **Axios 1.6**: HTTP client
- **CSS3**: Styling (Apple-inspired design)

### Backend
- **Django 5.2.8**: Web framework
- **Django REST Framework 3.15**: API framework
- **Django CORS Headers 4.3.0**: CORS handling
- **Django Auth Tokens**: Authentication

### Machine Learning
- **scikit-learn 1.5**: ML library (SVM)
- **librosa 0.10.1**: Audio processing
- **pandas 2.2**: Data manipulation
- **numpy 1.26**: Numerical computing

### Audio Processing
- **pydub 0.25.1**: Audio conversion
- **ffmpeg**: Audio format conversion
- **soundfile 0.12**: Audio I/O

### Database
- **SQLite**: Development database
- **Django ORM**: Database abstraction

## Communication Flow

### Authentication Flow
```
User → Frontend → API Service → Django → Database
                ← Token        ← User Data
```

### Prediction Flow
```
User → Frontend → API Service → Django → PredictService → ML Model
                ← Result      ← Prediction ← Feature Extraction
```

### Enrichment Flow
```
Management Command → Wikidata API → Parse Data → Database
                  → Wikipedia API → Parse Data → Database
```

## Security Architecture

### Authentication
- **Token-based**: Django REST Framework tokens
- **Session-based**: Django sessions (optional)
- **Protected Routes**: React Router guards

### Authorization
- **User-based**: Each user sees only their predictions
- **API-level**: Token validation on all endpoints
- **Database-level**: Foreign key constraints

### Data Security
- **Input Validation**: Serializer validation
- **SQL Injection Prevention**: Django ORM
- **XSS Prevention**: React automatic escaping
- **CORS Configuration**: Restricted origins

## Scalability Considerations

### Horizontal Scaling
- **Stateless Backend**: Django can be scaled horizontally
- **Load Balancing**: Multiple Django instances
- **Database**: Can migrate to PostgreSQL for scaling

### Performance Optimization
- **Model Caching**: ML model loaded once at startup
- **Database Indexing**: Indexed fields for fast queries
- **Audio Processing**: Async processing (future enhancement)
- **CDN**: Static files served via CDN (production)

### Monitoring
- **Logging**: Django logging framework
- **Error Tracking**: Sentry (recommended for production)
- **Performance Monitoring**: APM tools

## Deployment Architecture

### Development
```
React Dev Server (3000) → Django Dev Server (8000) → SQLite
```

### Production (Recommended)
```
Nginx → React Build → Django (Gunicorn) → PostgreSQL
     → Static Files → Media Files → ML Artifacts
```

## API Architecture

### RESTful Design
- **Resources**: Users, Birds, Predictions
- **HTTP Methods**: GET, POST, PUT, DELETE
- **Status Codes**: Standard HTTP status codes
- **Response Format**: JSON

### Endpoint Structure
```
/api/register/     POST   - Create user
/api/login/        POST   - Authenticate user
/api/logout/       POST   - Logout user
/api/user/         GET    - Get current user
/api/predict/      POST   - Predict bird species
/api/history/      GET    - Get prediction history
```

## Error Handling Architecture

### Frontend
- **API Errors**: Caught and displayed to user
- **Network Errors**: Retry logic (future enhancement)
- **Validation Errors**: Form-level validation

### Backend
- **Exception Handling**: Try-catch blocks
- **Error Responses**: Standardized error format
- **Logging**: All errors logged
- **Traceback**: Development mode shows tracebacks

## Data Flow Architecture

### Request Flow
1. User action (click, upload)
2. Frontend state update
3. API call (Axios)
4. Django URL routing
5. View processing
6. Service layer
7. Database/ML model
8. Response serialization
9. Frontend state update
10. UI update

### Response Flow
1. Service result
2. Serializer transformation
3. JSON response
4. Axios response interceptor
5. Frontend state update
6. Component re-render
7. UI update

---

This architecture provides a solid foundation for the Bird Sound Recognition System, with clear separation of concerns and scalability considerations.

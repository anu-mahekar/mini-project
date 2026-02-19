# Bird Sound Recognition - React Frontend

A modern React web application for identifying bird species from audio recordings.

## Features

- 🎤 **Audio Recording**: Record bird sounds directly from your browser
- 📁 **File Upload**: Upload audio files (MP3, WAV, FLAC, M4A, OGG, etc.)
- 🐦 **Species Identification**: AI-powered bird species recognition
- 📋 **Detailed Information**: View bird details, diet, and common diseases

## Prerequisites

- Node.js 14+ and npm
- Django backend running on `http://localhost:8000`

## Installation

1. Navigate to the React frontend directory:
```bash
cd react-frontend
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

1. Make sure the Django backend is running (see main project README)

2. Start the React development server:
```bash
npm start
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

## Configuration

### API URL

By default, the app connects to `http://localhost:8000`. To change this:

1. Create a `.env` file in the `react-frontend` directory:
```
REACT_APP_API_URL=http://your-backend-url:8000
```

2. Restart the development server

## Project Structure

```
react-frontend/
├── public/
│   └── index.html          # HTML template
├── src/
│   ├── components/         # React components
│   │   ├── AudioRecorder.js    # Audio recording component
│   │   ├── FileUpload.js        # File upload component
│   │   └── ResultDisplay.js    # Results display component
│   ├── services/
│   │   └── api.js          # API service for backend communication
│   ├── App.js              # Main app component
│   ├── App.css             # App styles
│   ├── index.js            # Entry point
│   └── index.css           # Global styles
├── package.json            # Dependencies and scripts
└── README.md              # This file
```

## Usage

### Recording Audio

1. Click on the "Record Audio" tab
2. Click "Start Recording" and allow microphone access
3. Record your bird sound
4. Click "Stop Recording" when done
5. Review the recording and click "Submit for Analysis"

### Uploading Audio File

1. Click on the "Upload File" tab
2. Drag and drop an audio file or click to browse
3. Select your audio file
4. Review the file and click "Submit for Analysis"

### Viewing Results

After analysis, you'll see:
- Identified bird species
- Bird information (name, locations, lifespan)
- Diet information
- Common diseases

## Building for Production

To create a production build:

```bash
npm run build
```

This creates an optimized build in the `build/` folder that can be served by any static file server.

## Troubleshooting

### CORS Errors

If you see CORS errors, make sure:
1. Django backend has `django-cors-headers` installed
2. CORS is properly configured in Django settings
3. Backend is running and accessible

### Microphone Not Working

- Check browser permissions for microphone access
- Use HTTPS in production (required for microphone access)
- Try a different browser

### API Connection Issues

- Verify Django backend is running on the correct port
- Check `REACT_APP_API_URL` in `.env` file
- Check browser console for detailed error messages

## Technologies Used

- **React 18** - UI framework
- **Axios** - HTTP client for API calls
- **MediaRecorder API** - Browser audio recording
- **CSS3** - Styling with modern CSS features

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Opera (latest)

Note: Audio recording requires a browser that supports MediaRecorder API.


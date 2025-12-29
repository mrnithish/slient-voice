# 📘 Silent Voice Diary

A privacy-first voice diary application that uses AI to analyze emotional patterns from voice recordings. Built with Flutter (Android), FastAPI, MongoDB, and Google Gemini AI.

## 🎯 Overview

Silent Voice Diary allows users to record voice entries and receive AI-powered emotional insights. The app prioritizes privacy and does not provide medical or therapeutic advice.

### Key Features

- **Google SSO Authentication** - Secure sign-in with Google
- **Voice Recording** - Record up to 5 minutes of audio
- **AI Emotion Analysis** - Powered by Google Gemini AI
- **Timeline View** - Browse past entries with emotional summaries
- **Privacy-First** - No third-party analytics on voice data

## 🏗️ Architecture

```
silent-voice-diary/
├── mobile/flutter_app/     # Flutter Android app
├── backend/api/             # FastAPI backend
├── ai/gemini_agent/         # Gemini AI integration
└── infra/config/            # Infrastructure configuration
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Flutter SDK 3.0+
- MongoDB instance (local or cloud) ✅
- Google Cloud account (for Gemini API and Speech-to-Text)
- Google OAuth credentials
- Cloudflare account (for R2 storage - free tier available)

### Environment Variables

#### Backend (.env)

```env
# MongoDB
MONGODB_URI=mongodb://localhost:27017/silent_voice

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id

# JWT
JWT_SECRET=your_jwt_secret_key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Google Gemini AI
GEMINI_API_KEY=your_gemini_api_key

# Cloudflare R2 Storage
R2_ENDPOINT_URL=https://your-account-id.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=your_r2_access_key_id
R2_SECRET_ACCESS_KEY=your_r2_secret_access_key
R2_BUCKET_NAME=your_bucket_name
R2_PUBLIC_URL=  # Optional: custom domain
```

**📖 For detailed instructions on where to get each value, see [ENV_VARIABLES_GUIDE.md](ENV_VARIABLES_GUIDE.md)**

#### Flutter App (.env)

```env
API_BASE_URL=http://localhost:8000
GOOGLE_CLIENT_ID=your_google_client_id
```

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend/api
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

5. **Start the server:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

   The API will be available at `http://localhost:8000`
   
   API documentation: `http://localhost:8000/docs`

### Flutter App Setup

1. **Navigate to Flutter app directory:**
   ```bash
   cd mobile/flutter_app
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API base URL and Google Client ID
   ```

3. **Install dependencies:**
   ```bash
   flutter pub get
   ```

4. **Configure Google Sign-In:**
   - Add your Google OAuth Client ID to `android/app/src/main/AndroidManifest.xml` if needed
   - Configure SHA-1 fingerprint in Google Cloud Console
   - Update `GOOGLE_CLIENT_ID` in `.env`

5. **Run the app:**
   ```bash
   flutter run
   ```

   Or build for release:
   ```bash
   flutter build apk --release
   ```

## 📱 Mobile App

### Features

- Google Sign-In integration
- Voice recording (max 5 minutes)
- Audio upload to backend
- Emotion results display
- Timeline/history view

### Android Configuration

The app is configured for Android-only deployment. Ensure you have:

1. **Android SDK installed** (via Android Studio)
2. **Google Sign-In setup:**
   - Create OAuth 2.0 credentials in Google Cloud Console
   - Add SHA-1 fingerprint from your keystore:
     ```bash
     keytool -list -v -keystore ~/.android/debug.keystore -alias androiddebugkey -storepass android -keypass android
     ```
   - Add the SHA-1 to your OAuth credentials
3. **Package name:** `com.silentvoice.diary` (configured in `android/app/build.gradle`)
4. **Permissions:** Microphone and Internet (already configured in `AndroidManifest.xml`)

## 🔧 Backend API

### Endpoints

#### Authentication
- `POST /auth/google` - Verify Google ID token and issue JWT

#### Voice Entries
- `POST /entry/upload` - Upload audio file and process
- `GET /entry/list` - Get all entries for authenticated user
- `GET /entry/{id}` - Get specific entry by ID

### Authentication

All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

## 🤖 AI Module

The Gemini AI agent performs:

1. **Speech-to-Text** - Transcribes audio to text using Google Speech-to-Text API
2. **Emotion Analysis** - Analyzes emotional patterns using Gemini Pro and returns structured JSON

### AI Agent Behavior

The emotion intelligence agent:
- ✅ Analyzes emotional patterns
- ✅ Returns structured insights
- ❌ Does NOT provide advice
- ❌ Does NOT act as a therapist
- ❌ Does NOT diagnose conditions

**Important:** This is an emotion analysis tool, not a medical or therapeutic service.

### Emotion Analysis Output

```json
{
  "primary_emotion": "anxious",
  "secondary_emotions": ["worried", "uncertain"],
  "mood_score": -3,
  "stress_level": "high",
  "themes": ["work", "deadlines"],
  "energy_level": "low",
  "confidence_level": "low",
  "summary": "User expresses anxiety about upcoming work deadlines..."
}
```

## 🔒 Security & Privacy

- JWT tokens stored securely in Flutter secure storage
- Audio files encrypted at rest
- User data isolation (users can only access their own entries)
- No third-party analytics on voice data
- **Disclaimer**: This app is not a medical or therapeutic service

## ☁️ Storage

The app uses **Cloudflare R2** for audio file storage (S3-compatible, free tier available).

### Setup Cloudflare R2

1. Create account at [Cloudflare](https://dash.cloudflare.com/sign-up)
2. Enable R2 in dashboard
3. Create a bucket
4. Generate API token
5. Get endpoint URL and credentials

**See [ENV_VARIABLES_GUIDE.md](ENV_VARIABLES_GUIDE.md) for detailed R2 setup instructions.**

## 📊 Database Schema

### Users Collection

```json
{
  "_id": "ObjectId",
  "email": "string",
  "name": "string",
  "provider": "google",
  "provider_id": "string",
  "created_at": "datetime"
}
```

### Voice Entries Collection

```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId",
  "audio_url": "string",
  "transcript": "string",
  "emotion_data": {
    "primary_emotion": "string",
    "secondary_emotions": [],
    "mood_score": -3,
    "stress_level": "high",
    "themes": [],
    "energy_level": "low",
    "confidence_level": "low",
    "summary": "string"
  },
  "created_at": "datetime"
}
```

## 🐛 Error Handling

The app handles:
- Audio upload failures
- AI processing timeouts
- Invalid Gemini responses
- Network errors

Fallback message: "We couldn't analyze this entry. Please try again."

## 📝 Logging

The backend logs:
- Authentication events
- AI request duration
- Upload errors
- API request/response (without sensitive data)

**Note**: Raw audio and transcripts are NOT logged.

## 🚢 Deployment

### Backend

#### Option 1: Docker Compose (Recommended for Development)

```bash
cd infra/config
docker-compose up -d
```

#### Option 2: Manual Deployment

1. **Server Requirements:**
   - Python 3.9+
   - MongoDB instance
   - GPU-capable instance (optional, for faster AI processing)

2. **Deployment Steps:**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Set environment variables
   export MONGODB_URI=...
   export GEMINI_API_KEY=...
   # ... etc
   
   # Run with production server
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **Production Checklist:**
   - ✅ Use HTTPS (configure reverse proxy with nginx/Apache)
   - ✅ Secure environment variables (use secrets management)
   - ✅ Enable CORS for production domain only
   - ✅ Set up logging and monitoring
   - ✅ Configure auto-scaling if needed
   - ✅ Set up database backups

### Mobile App

1. **Build Release APK:**
   ```bash
   cd mobile/flutter_app
   flutter build apk --release
   ```

2. **Build App Bundle (for Play Store):**
   ```bash
   flutter build appbundle --release
   ```

3. **Production Checklist:**
   - ✅ Configure Google Sign-In for production (use release keystore SHA-1)
   - ✅ Update API base URL to production endpoint
   - ✅ Test all features in release mode
   - ✅ Add privacy policy and terms of service
   - ✅ Submit to Google Play Store

## 🧪 Testing

### Backend API Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test authentication (replace with actual ID token)
curl -X POST http://localhost:8000/auth/google \
  -H "Content-Type: application/json" \
  -d '{"id_token": "your_google_id_token"}'
```

### Flutter App Testing

```bash
cd mobile/flutter_app
flutter test
```

## 📝 Development Notes

### Project Structure

- **Backend API:** FastAPI with async MongoDB (Motor)
- **Mobile App:** Flutter with Provider for state management
- **AI Module:** Standalone module for emotion analysis
- **Storage:** S3-compatible storage for audio files

### Key Technologies

- **Backend:** FastAPI, Motor (async MongoDB), Google Auth, Gemini AI
- **Mobile:** Flutter, Provider, Google Sign-In, Audio Recording
- **Storage:** AWS S3 (or compatible)
- **Database:** MongoDB

## 🤝 Contributing

This is a private project. For issues or questions, please contact the project maintainer.

## 📄 License

Private project - All rights reserved

## ⚠️ Disclaimer

**This application is not a medical or therapeutic service.** 

It provides emotional insights for informational purposes only and should not be used as a substitute for professional medical or mental health advice, diagnosis, or treatment. Always seek the advice of qualified health providers with any questions you may have regarding a medical condition or mental health concern.

## 📞 Support

For technical support or questions, please refer to the project documentation or contact the development team.


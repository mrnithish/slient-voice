# 🚀 Silent Voice Diary - Setup Guide

This guide will help you set up the Silent Voice Diary application from scratch.

## Prerequisites Checklist

- [ ] Python 3.9+ installed
- [ ] Flutter SDK 3.0+ installed
- [ ] MongoDB instance (local or cloud)
- [ ] Google Cloud account
- [ ] AWS account (for S3) or Google Cloud Storage
- [ ] Android Studio (for Flutter development)

## Step 1: Backend Setup

### 1.1 Install Python Dependencies

```bash
cd backend/api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 1.2 Configure Environment Variables

Create `.env` file in `backend/api/`:

```env
# MongoDB
MONGODB_URI=mongodb://localhost:27017/silent_voice

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id_here

# JWT
JWT_SECRET=generate-a-secure-random-string-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Gemini AI
GEMINI_API_KEY=your_gemini_api_key_here

# Storage (S3)
STORAGE_TYPE=s3
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_BUCKET_NAME=your_bucket_name
AWS_REGION=us-east-1
```

### 1.3 Get Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs
6. Copy Client ID to `.env`

### 1.4 Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy to `.env`

### 1.5 Setup MongoDB ✅ (You Have This)

You already have MongoDB connection. Use your existing connection string in `.env`.

**Option A: Local MongoDB**
```bash
# If using local MongoDB
MONGODB_URI=mongodb://localhost:27017/silent_voice
```

**Option B: MongoDB Atlas (Cloud)**
```bash
# If using MongoDB Atlas
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/silent_voice
```

### 1.6 Setup Cloudflare R2 Storage

1. **Create Cloudflare Account:**
   - Go to https://dash.cloudflare.com/sign-up
   - Sign up (free tier available)

2. **Enable R2:**
   - In dashboard, go to "R2" in sidebar
   - Click "Get Started"

3. **Create Bucket:**
   - Click "Create bucket"
   - Name: `silent-voice-audio` (or your choice)
   - Choose location
   - Click "Create"

4. **Get API Credentials:**
   - Go to "Manage R2 API Tokens"
   - Click "Create API Token"
   - Copy Access Key ID and Secret Access Key

5. **Get Endpoint URL:**
   - Format: `https://<account-id>.r2.cloudflarestorage.com`
   - Find your account ID in R2 dashboard

6. **Update `.env`:**
   ```env
   R2_ENDPOINT_URL=https://your-account-id.r2.cloudflarestorage.com
   R2_ACCESS_KEY_ID=your_access_key_id
   R2_SECRET_ACCESS_KEY=your_secret_access_key
   R2_BUCKET_NAME=silent-voice-audio
   ```

**📖 Detailed instructions: See [ENV_VARIABLES_GUIDE.md](ENV_VARIABLES_GUIDE.md)**

### 1.7 Start Backend Server

```bash
cd backend/api
uvicorn main:app --reload --port 8000
```

Verify: Visit `http://localhost:8000/docs` for API documentation

## Step 2: Flutter App Setup

### 2.1 Install Flutter Dependencies

```bash
cd mobile/flutter_app
flutter pub get
```

### 2.2 Configure Environment Variables

Create `.env` file in `mobile/flutter_app/`:

```env
API_BASE_URL=http://localhost:8000
GOOGLE_CLIENT_ID=your_google_client_id_here
```

**Note:** For Android emulator, use `http://10.0.2.2:8000` instead of `localhost`

### 2.3 Configure Google Sign-In for Android

1. Get SHA-1 fingerprint:
   ```bash
   keytool -list -v -keystore ~/.android/debug.keystore -alias androiddebugkey -storepass android -keypass android
   ```

2. Add SHA-1 to Google Cloud Console OAuth credentials

3. Update `GOOGLE_CLIENT_ID` in Flutter `.env`

### 2.4 Run Flutter App

```bash
cd mobile/flutter_app
flutter run
```

## Step 3: Testing

### 3.1 Test Backend

```bash
# Health check
curl http://localhost:8000/health

# Should return: {"status": "healthy"}
```

### 3.2 Test Flutter App

1. Launch app on Android device/emulator
2. Tap "Sign in with Google"
3. Grant permissions
4. Try recording a voice entry
5. Verify upload and emotion analysis

## Troubleshooting

### Backend Issues

**MongoDB Connection Error:**
- Check MongoDB is running
- Verify `MONGODB_URI` in `.env`
- Check firewall settings

**Gemini API Error:**
- Verify API key is correct
- Check API quota/limits
- Ensure billing is enabled

**R2 Upload Error:**
- Verify R2 credentials
- Check bucket permissions
- Verify bucket name and endpoint URL
- Ensure R2 is enabled in your Cloudflare account

### Flutter Issues

**Google Sign-In Not Working:**
- Verify SHA-1 fingerprint is added to Google Cloud Console
- Check `GOOGLE_CLIENT_ID` matches backend
- Ensure OAuth consent screen is configured

**API Connection Error:**
- For Android emulator, use `http://10.0.2.2:8000`
- For physical device, use your computer's IP address
- Check backend CORS settings

**Audio Recording Not Working:**
- Grant microphone permission
- Check Android manifest permissions
- Verify audio service initialization

## Next Steps

1. ✅ Backend running on port 8000
2. ✅ Flutter app connected to backend
3. ✅ Google Sign-In working
4. ✅ Voice recording functional
5. ✅ Emotion analysis working

## Production Deployment

See main `README.md` for production deployment instructions.

## Support

For issues or questions, refer to the main README or contact the development team.


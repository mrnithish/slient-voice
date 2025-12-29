# ⚡ Quick Reference

## Environment Variables

### Backend (`backend/api/.env`)
```env
MONGODB_URI=mongodb://localhost:27017/silent_voice
GOOGLE_CLIENT_ID=your_client_id
JWT_SECRET=your_secret
GEMINI_API_KEY=your_key
R2_ENDPOINT_URL=https://account-id.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=your_r2_key
R2_SECRET_ACCESS_KEY=your_r2_secret
R2_BUCKET_NAME=your_bucket
```

### Flutter (`mobile/flutter_app/.env`)
```env
API_BASE_URL=http://localhost:8000
GOOGLE_CLIENT_ID=your_client_id
```

## Common Commands

### Backend
```bash
# Start server
cd backend/api && uvicorn main:app --reload

# Install dependencies
pip install -r requirements.txt

# Run with Docker
cd infra/config && docker-compose up
```

### Flutter
```bash
# Get dependencies
cd mobile/flutter_app && flutter pub get

# Run app
flutter run

# Build APK
flutter build apk --release
```

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/google` | No | Authenticate with Google |
| POST | `/entry/upload` | Yes | Upload voice entry |
| GET | `/entry/list` | Yes | List user entries |
| GET | `/entry/{id}` | Yes | Get entry details |
| GET | `/health` | No | Health check |

## File Structure

```
backend/api/app/
├── config.py          # Settings
├── database.py        # MongoDB
├── auth.py           # JWT & Google auth
├── storage.py        # S3 uploads
├── ai_agent.py      # Gemini AI
└── routers/          # API routes

mobile/flutter_app/lib/
├── services/         # API, Auth, Audio
└── screens/          # UI screens
```

## Troubleshooting

**Backend won't start:**
- Check MongoDB is running
- Verify `.env` file exists
- Check port 8000 is available

**Flutter build fails:**
- Run `flutter clean`
- Run `flutter pub get`
- Check Android SDK is installed

**Google Sign-In fails:**
- Verify SHA-1 fingerprint
- Check OAuth credentials
- Ensure Client ID matches

**Audio upload fails:**
- Check R2 credentials
- Verify bucket permissions
- Check file size (< 50MB)
- Verify R2 endpoint URL format

## Key Files

- `README.md` - Full documentation
- `SETUP_GUIDE.md` - Setup instructions
- `PROJECT_SUMMARY.md` - Project overview


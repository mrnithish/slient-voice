# Environment Variables Setup

See the main [ENV_VARIABLES_GUIDE.md](../../ENV_VARIABLES_GUIDE.md) for complete instructions.

## Quick Reference

Create a `.env` file in this directory (`backend/api/.env`) with:

```env
# MongoDB
MONGODB_URI=your_mongodb_connection_string
DATABASE_NAME=silent_voice

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id

# JWT
JWT_SECRET=generate-secure-random-string
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Google Gemini AI
GEMINI_API_KEY=your_gemini_api_key

# Cloudflare R2 Storage
R2_ENDPOINT_URL=https://your-account-id.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=your_r2_access_key_id
R2_SECRET_ACCESS_KEY=your_r2_secret_access_key
R2_BUCKET_NAME=your-bucket-name
R2_PUBLIC_URL=
```

For detailed instructions on where to get each value, see [ENV_VARIABLES_GUIDE.md](../../ENV_VARIABLES_GUIDE.md).




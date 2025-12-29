# 🔐 Environment Variables Guide

Complete guide on where to get all environment variables for Silent Voice Diary.

## 📋 Quick Checklist

- [ ] MongoDB URI (you have this ✅)
- [ ] Google OAuth Client ID
- [ ] Google Gemini API Key
- [ ] JWT Secret (generate yourself)
- [ ] Cloudflare R2 credentials

---

## 1. MongoDB URI ✅ (You Have This)

**Variable:** `MONGODB_URI`

**Current Value:** Your existing MongoDB connection string

**Format:**
```
mongodb://localhost:27017/silent_voice
```
or for MongoDB Atlas:
```
mongodb+srv://username:password@cluster.mongodb.net/silent_voice
```

**Where to get it:**
- **Local MongoDB:** `mongodb://localhost:27017/silent_voice`
- **MongoDB Atlas:** 
  1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
  2. Click "Connect" on your cluster
  3. Choose "Connect your application"
  4. Copy the connection string
  5. Replace `<password>` with your password

---

## 2. Google OAuth Client ID

**Variable:** `GOOGLE_CLIENT_ID`

**Where to get it:**

1. **Go to Google Cloud Console:**
   - Visit: https://console.cloud.google.com/

2. **Create or Select Project:**
   - Click project dropdown at top
   - Create new project or select existing

3. **Enable APIs:**
   - Go to "APIs & Services" > "Library"
   - Search for "Google+ API" and enable it
   - Search for "Google Identity" and enable it

4. **Create OAuth Credentials:**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - If prompted, configure OAuth consent screen first:
     - User Type: External
     - App name: Silent Voice Diary
     - Support email: your email
     - Add your email to test users
     - Save

5. **Create OAuth Client:**
   - Application type: **Web application**
   - Name: Silent Voice Diary
   - Authorized redirect URIs: 
     - `http://localhost:8000/auth/callback` (for testing)
     - Add your production URL later
   - Click "Create"
   - **Copy the Client ID** (not the secret)

6. **For Android (Flutter app):**
   - Create another OAuth client
   - Application type: **Android**
   - Package name: `com.silentvoice.diary`
   - Get SHA-1 fingerprint:
     ```bash
     keytool -list -v -keystore ~/.android/debug.keystore -alias androiddebugkey -storepass android -keypass android
     ```
   - Add SHA-1 to the Android OAuth client
   - Use the **same Client ID** for both web and Android (or create separate ones)

**Example:**
```
GOOGLE_CLIENT_ID=123456789-abcdefghijklmnop.apps.googleusercontent.com
```

---

## 3. Google Gemini API Key

**Variable:** `GEMINI_API_KEY`

**Where to get it:**

1. **Go to Google AI Studio:**
   - Visit: https://makersuite.google.com/app/apikey
   - Or: https://aistudio.google.com/app/apikey

2. **Sign in with Google account**

3. **Create API Key:**
   - Click "Create API Key"
   - Select your Google Cloud project (or create new)
   - Copy the API key

4. **Enable Billing (if required):**
   - Some features may require billing enabled
   - Go to Google Cloud Console > Billing
   - Link a billing account

**Example:**
```
GEMINI_API_KEY=AIzaSyAbc123Def456Ghi789Jkl012Mno345Pqr
```

**Note:** Also need Google Speech-to-Text API:
- Go to Google Cloud Console
- Enable "Cloud Speech-to-Text API"
- Same project as Gemini API key

---

## 4. JWT Secret

**Variable:** `JWT_SECRET`

**Generate yourself - this is a secret key for signing JWT tokens**

**How to generate:**

**Option 1: Using Python:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Option 2: Using OpenSSL:**
```bash
openssl rand -base64 32
```

**Option 3: Online (less secure):**
- Visit: https://randomkeygen.com/
- Use "CodeIgniter Encryption Keys"

**Example:**
```
JWT_SECRET=your-super-secret-random-string-at-least-32-characters-long
```

**Important:** 
- Use a long, random string (at least 32 characters)
- Never commit this to git
- Use different secrets for development and production

---

## 5. Cloudflare R2 Storage

**Variables:**
- `R2_ENDPOINT_URL`
- `R2_ACCESS_KEY_ID`
- `R2_SECRET_ACCESS_KEY`
- `R2_BUCKET_NAME`
- `R2_PUBLIC_URL` (optional)

**Where to get them:**

### Step 1: Create Cloudflare Account
1. Go to https://dash.cloudflare.com/sign-up
2. Sign up for free account

### Step 2: Enable R2 Storage
1. In Cloudflare dashboard, go to "R2" in sidebar
2. Click "Get Started" or "Create bucket"
3. Accept terms if prompted

### Step 3: Create R2 Bucket
1. Click "Create bucket"
2. Bucket name: `silent-voice-audio` (or your choice)
3. Location: Choose closest to you
4. Click "Create bucket"
5. **Copy the bucket name** → This is `R2_BUCKET_NAME`

### Step 4: Create API Token
1. In R2 dashboard, click "Manage R2 API Tokens"
2. Or go to: https://dash.cloudflare.com/profile/api-tokens
3. Click "Create Token"
4. Use "Edit Cloudflare Workers" template, or:
   - Permissions: R2:Edit
   - Account Resources: Include - All accounts
   - Zone Resources: Include - All zones
5. Click "Continue to summary" > "Create Token"
6. **Copy the token** → This is `R2_SECRET_ACCESS_KEY`

### Step 5: Get Access Key ID
1. In R2 dashboard, go to "Manage R2 API Tokens"
2. Under "R2 Token", you'll see:
   - **Access Key ID** → This is `R2_ACCESS_KEY_ID`
   - **Secret Access Key** → This is `R2_SECRET_ACCESS_KEY` (from step 4)

### Step 6: Get Endpoint URL
1. In R2 bucket settings, find "S3 API" section
2. You'll see endpoint URL like:
   ```
   https://<account-id>.r2.cloudflarestorage.com
   ```
3. **Copy this** → This is `R2_ENDPOINT_URL`

   **Or find Account ID:**
   - Go to R2 dashboard
   - Your account ID is in the URL or dashboard
   - Format: `https://<account-id>.r2.cloudflarestorage.com`

### Step 7: (Optional) Set Up Custom Domain
1. In R2 bucket, go to "Settings" > "Public Access"
2. Enable "Allow Access"
3. You can use the default R2 URL or set up custom domain
4. If using custom domain, that's `R2_PUBLIC_URL`

**Example values:**
```
R2_ENDPOINT_URL=https://abc123def456.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=your-access-key-id-here
R2_SECRET_ACCESS_KEY=your-secret-access-key-here
R2_BUCKET_NAME=silent-voice-audio
R2_PUBLIC_URL=https://your-bucket.your-domain.com  # Optional
```

---

## 📝 Complete .env File Template

Create `backend/api/.env` file:

```env
# MongoDB (you have this ✅)
MONGODB_URI=your_mongodb_connection_string_here
DATABASE_NAME=silent_voice

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id_here

# JWT (generate yourself)
JWT_SECRET=generate-a-secure-random-string-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Google Gemini AI
GEMINI_API_KEY=your_gemini_api_key_here

# Cloudflare R2 Storage
R2_ENDPOINT_URL=https://your-account-id.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=your_r2_access_key_id
R2_SECRET_ACCESS_KEY=your_r2_secret_access_key
R2_BUCKET_NAME=your-bucket-name
R2_PUBLIC_URL=  # Optional: leave empty or add custom domain

# CORS (add your frontend URLs)
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

---

## 📱 Flutter App .env File

Create `mobile/flutter_app/.env` file:

```env
# Backend API URL
API_BASE_URL=http://localhost:8000
# For Android emulator, use: http://10.0.2.2:8000
# For physical device, use your computer's IP: http://192.168.1.x:8000

# Google OAuth Client ID (same as backend or Android-specific)
GOOGLE_CLIENT_ID=your_google_client_id_here
```

---

## ✅ Verification Checklist

After setting up all variables:

1. **MongoDB:**
   ```bash
   # Test connection
   mongosh "your_mongodb_uri"
   ```

2. **Google OAuth:**
   - Test in Google Cloud Console > OAuth consent screen
   - Verify redirect URIs are correct

3. **Gemini API:**
   - Test at: https://aistudio.google.com/
   - Try generating content

4. **Cloudflare R2:**
   - Test upload in R2 dashboard
   - Verify bucket is accessible

5. **Backend:**
   ```bash
   cd backend/api
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   uvicorn main:app --reload
   # Should start without errors
   ```

---

## 🆘 Troubleshooting

**"Invalid Google token" error:**
- Check Client ID matches in backend and Flutter app
- Verify OAuth consent screen is configured
- Check redirect URIs

**"Gemini API error":**
- Verify API key is correct
- Check billing is enabled in Google Cloud
- Ensure Speech-to-Text API is enabled

**"R2 upload failed":**
- Verify endpoint URL format
- Check access key and secret are correct
- Ensure bucket name matches
- Check bucket permissions

**"MongoDB connection failed":**
- Verify connection string format
- Check network/firewall settings
- For Atlas: Check IP whitelist

---

## 🔒 Security Notes

- **Never commit `.env` files to git**
- Use different secrets for development and production
- Rotate secrets regularly
- Use environment-specific values
- Keep JWT secret long and random (32+ characters)

---

## 📚 Additional Resources

- [Google Cloud Console](https://console.cloud.google.com/)
- [Google AI Studio](https://aistudio.google.com/)
- [Cloudflare R2 Docs](https://developers.cloudflare.com/r2/)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)




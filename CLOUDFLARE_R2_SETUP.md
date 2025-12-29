# ☁️ Cloudflare R2 Setup Guide

Quick guide for setting up Cloudflare R2 storage for Silent Voice Diary.

## Why Cloudflare R2?

- ✅ **S3-compatible API** - Works with existing boto3 code
- ✅ **Free tier** - 10GB storage + 1M Class A operations/month
- ✅ **No egress fees** - Unlike AWS S3
- ✅ **Fast global CDN** - Built on Cloudflare network
- ✅ **Easy setup** - Simple dashboard interface

## Step-by-Step Setup

### 1. Create Cloudflare Account

1. Go to https://dash.cloudflare.com/sign-up
2. Sign up (free account works)
3. Verify your email

### 2. Enable R2 Storage

1. In Cloudflare dashboard, click **"R2"** in the left sidebar
2. If you see "Get Started", click it
3. Accept terms if prompted
4. R2 is now enabled!

### 3. Create a Bucket

1. Click **"Create bucket"**
2. **Bucket name:** `silent-voice-audio` (or your choice)
   - Must be globally unique
   - Lowercase, hyphens allowed
3. **Location:** Choose closest to you (e.g., `WNAM` for US West)
4. Click **"Create bucket"**
5. ✅ **Save the bucket name** → This is `R2_BUCKET_NAME`

### 4. Get API Credentials

#### Option A: Using R2 Dashboard

1. In R2 dashboard, click **"Manage R2 API Tokens"**
2. Or go to: https://dash.cloudflare.com/profile/api-tokens
3. Scroll to **"R2 Token"** section
4. Click **"Create API Token"**
5. Configure:
   - **Token name:** `Silent Voice Diary`
   - **Permissions:** R2:Edit
   - **Account Resources:** Include - All accounts
6. Click **"Continue to summary"** > **"Create Token"**
7. **Copy the token immediately** (you won't see it again!)
   - This is `R2_SECRET_ACCESS_KEY`

#### Option B: Using Workers Dashboard

1. Go to Workers dashboard
2. Click **"Manage R2 API Tokens"**
3. Follow same steps as Option A

### 5. Get Access Key ID

1. In R2 dashboard, go to **"Manage R2 API Tokens"**
2. Under **"R2 Token"**, you'll see:
   - **Access Key ID** → This is `R2_ACCESS_KEY_ID`
   - **Secret Access Key** → This is `R2_SECRET_ACCESS_KEY` (from step 4)

**Note:** If you don't see Access Key ID, you may need to create it:
1. Click **"Create API Token"**
2. This will generate both Access Key ID and Secret

### 6. Get Endpoint URL

The R2 endpoint URL format is:
```
https://<account-id>.r2.cloudflarestorage.com
```

**To find your Account ID:**

1. Go to R2 dashboard
2. Look at the URL: `https://dash.cloudflare.com/<account-id>/r2/...`
3. Or go to any Cloudflare dashboard page
4. Account ID is in the URL or visible in dashboard header

**Example:**
If your account ID is `abc123def456`, your endpoint is:
```
https://abc123def456.r2.cloudflarestorage.com
```

### 7. (Optional) Set Up Public Access

If you want public URLs for audio files:

1. In your R2 bucket, go to **"Settings"**
2. Scroll to **"Public Access"**
3. Click **"Allow Access"**
4. Choose:
   - **Public bucket** - All files public
   - **Custom domain** - Use your own domain (recommended)

**For Custom Domain:**
1. Add your domain to Cloudflare
2. In R2 bucket settings, add custom domain
3. Use that domain as `R2_PUBLIC_URL`

## Environment Variables

Add these to your `backend/api/.env`:

```env
# Cloudflare R2 Storage
R2_ENDPOINT_URL=https://your-account-id.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=your_access_key_id_here
R2_SECRET_ACCESS_KEY=your_secret_access_key_here
R2_BUCKET_NAME=silent-voice-audio
R2_PUBLIC_URL=  # Optional: leave empty or add custom domain
```

## Testing R2 Connection

### Using Python

```python
import boto3
from botocore.config import Config

client = boto3.client(
    's3',
    endpoint_url='https://your-account-id.r2.cloudflarestorage.com',
    aws_access_key_id='your_access_key_id',
    aws_secret_access_key='your_secret_access_key',
    region_name='auto',
    config=Config(signature_version='s3v4')
)

# List buckets
buckets = client.list_buckets()
print(buckets)

# Upload test file
with open('test.txt', 'rb') as f:
    client.put_object(
        Bucket='silent-voice-audio',
        Key='test.txt',
        Body=f
    )
print("Upload successful!")
```

### Using AWS CLI (if installed)

```bash
# Configure endpoint
export AWS_ACCESS_KEY_ID=your_access_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_access_key
export AWS_ENDPOINT_URL=https://your-account-id.r2.cloudflarestorage.com

# List buckets
aws s3 ls --endpoint-url=$AWS_ENDPOINT_URL

# Upload file
aws s3 cp test.txt s3://silent-voice-audio/ --endpoint-url=$AWS_ENDPOINT_URL
```

## Pricing

**Free Tier:**
- 10 GB storage
- 1M Class A operations/month (writes, lists)
- 10M Class B operations/month (reads)

**After Free Tier:**
- Storage: $0.015/GB/month
- Class A: $4.50/million
- Class B: $0.36/million
- **No egress fees!** (unlike AWS S3)

## Troubleshooting

**"Invalid endpoint" error:**
- Verify endpoint URL format: `https://<account-id>.r2.cloudflarestorage.com`
- Check account ID is correct

**"Access denied" error:**
- Verify Access Key ID and Secret are correct
- Check token has R2:Edit permissions
- Ensure bucket name matches

**"Bucket not found" error:**
- Verify bucket name is correct
- Check bucket exists in R2 dashboard
- Ensure you're using the right account

**Upload works but can't access files:**
- Enable public access in bucket settings
- Or use signed URLs (implemented in code)
- Or set up custom domain

## Next Steps

1. ✅ R2 bucket created
2. ✅ API credentials obtained
3. ✅ Environment variables configured
4. ✅ Test upload successful
5. Ready to use in app!

For complete environment setup, see [ENV_VARIABLES_GUIDE.md](ENV_VARIABLES_GUIDE.md)




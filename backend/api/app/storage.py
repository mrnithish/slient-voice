"""
File storage utilities for audio files
Uses Cloudflare R2 (S3-compatible)
"""

import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
from fastapi import UploadFile
import logging
import uuid
from datetime import datetime, timedelta
from typing import Optional

from app.config import settings

logger = logging.getLogger(__name__)

# R2 client (initialized lazily)
_r2_client = None


def get_r2_client():
    """Get or create Cloudflare R2 client (S3-compatible)"""
    global _r2_client
    
    if _r2_client is None:
        # R2 uses S3-compatible API with custom endpoint
        _r2_client = boto3.client(
            's3',
            endpoint_url=settings.R2_ENDPOINT_URL,
            aws_access_key_id=settings.R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
            region_name='auto',  # R2 uses 'auto' as region
            config=Config(signature_version='s3v4')
        )
    
    return _r2_client


async def upload_audio_file(audio: UploadFile, user_id: str) -> str:
    """
    Upload audio file to Cloudflare R2 storage
    Returns the URL of the uploaded file
    """
    try:
        # Generate unique filename
        file_extension = audio.filename.split('.')[-1] if audio.filename else 'mp3'
        filename = f"{user_id}/{uuid.uuid4()}.{file_extension}"
        
        return await _upload_to_r2(audio, filename)
            
    except Exception as e:
        logger.error(f"Error uploading audio file: {e}")
        raise


async def _upload_to_r2(audio: UploadFile, filename: str) -> str:
    """Upload file to Cloudflare R2"""
    try:
        r2_client = get_r2_client()
        
        # Read file content
        content = await audio.read()
        
        # Upload to R2
        r2_client.put_object(
            Bucket=settings.R2_BUCKET_NAME,
            Key=filename,
            Body=content,
            ContentType=audio.content_type or "audio/mpeg"
        )
        
        # Generate public URL (if bucket is public) or use custom domain
        if settings.R2_PUBLIC_URL:
            # Use custom domain if configured
            url = f"{settings.R2_PUBLIC_URL.rstrip('/')}/{filename}"
        else:
            # Use R2 public URL format
            # Extract account ID from endpoint URL
            endpoint = settings.R2_ENDPOINT_URL.rstrip('/')
            url = f"{endpoint}/{settings.R2_BUCKET_NAME}/{filename}"
        
        logger.info(f"File uploaded to R2: {filename}")
        return url
        
    except ClientError as e:
        logger.error(f"R2 upload error: {e}")
        raise Exception("Failed to upload file to storage")


def get_audio_url(filename: str, expires_in: int = 3600) -> Optional[str]:
    """
    Generate signed URL for audio file
    expires_in: URL expiration time in seconds (default 1 hour)
    """
    try:
        r2_client = get_r2_client()
        url = r2_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.R2_BUCKET_NAME, 'Key': filename},
            ExpiresIn=expires_in
        )
        return url
    except Exception as e:
        logger.error(f"Error generating signed URL: {e}")
        return None


"""
Authentication utilities - JWT and Google token verification
"""

from datetime import datetime, timedelta
from jose import JWTError, jwt
from google.auth.transport import requests
from google.oauth2 import id_token
import logging

from app.config import settings

logger = logging.getLogger(__name__)


def create_access_token(data: dict) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt


def verify_token(token: str) -> dict:
    """Verify JWT token"""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError as e:
        logger.warning(f"JWT verification failed: {e}")
        raise


async def verify_google_token(id_token_str: str) -> dict:
    """Verify Google ID token and return user info"""
    try:
        # Verify the token
        idinfo = id_token.verify_oauth2_token(
            id_token_str,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )
        
        # Verify issuer
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        
        # Return user info
        return {
            "email": idinfo.get("email"),
            "name": idinfo.get("name"),
            "provider_id": idinfo.get("sub"),
            "picture": idinfo.get("picture")
        }
        
    except ValueError as e:
        logger.error(f"Google token verification failed: {e}")
        raise ValueError("Invalid Google token")




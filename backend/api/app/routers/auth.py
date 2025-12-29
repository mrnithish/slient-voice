"""
Authentication routes
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging

from app.models import GoogleAuthRequest, AuthResponse
from app.auth import verify_google_token, create_access_token
from app.database import get_database
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter()
security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Dependency to get current authenticated user"""
    from app.auth import verify_token
    
    token = credentials.credentials
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except Exception as e:
        logger.warning(f"Token verification failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@router.post("/google", response_model=AuthResponse)
async def google_auth(request: GoogleAuthRequest):
    """
    Authenticate with Google ID token
    Verify token, create/update user, and issue JWT
    """
    try:
        # Verify Google token
        user_info = await verify_google_token(request.id_token)
        
        if not user_info.get("email"):
            raise HTTPException(status_code=400, detail="Email not found in token")
        
        db = get_database()
        users_collection = db.users
        
        # Check if user exists
        existing_user = await users_collection.find_one({"email": user_info["email"]})
        
        if existing_user:
            user_id = str(existing_user["_id"])
            logger.info(f"Existing user logged in: {user_info['email']}")
        else:
            # Create new user
            new_user = {
                "email": user_info["email"],
                "name": user_info.get("name", ""),
                "provider": "google",
                "provider_id": user_info["provider_id"],
                "created_at": datetime.utcnow()
            }
            result = await users_collection.insert_one(new_user)
            user_id = str(result.inserted_id)
            logger.info(f"New user created: {user_info['email']}")
        
        # Create JWT token
        access_token = create_access_token(data={"sub": user_id, "email": user_info["email"]})
        
        return AuthResponse(
            access_token=access_token,
            token_type="bearer",
            user={
                "id": user_id,
                "email": user_info["email"],
                "name": user_info.get("name", "")
            }
        )
        
    except ValueError as e:
        logger.error(f"Google auth error: {e}")
        raise HTTPException(status_code=401, detail="Invalid Google token")
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(status_code=500, detail="Authentication failed")




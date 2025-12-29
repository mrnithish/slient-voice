"""
Pydantic models for request/response validation
"""

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId for Pydantic"""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


# Auth Models
class GoogleAuthRequest(BaseModel):
    """Google authentication request"""
    id_token: str = Field(..., description="Google ID token")


class AuthResponse(BaseModel):
    """Authentication response"""
    access_token: str
    token_type: str = "bearer"
    user: dict


# Voice Entry Models
class EmotionData(BaseModel):
    """Emotion analysis data"""
    primary_emotion: str
    secondary_emotions: List[str] = []
    mood_score: int = Field(..., ge=-5, le=5, description="Mood score from -5 to 5")
    stress_level: str = Field(..., pattern="^(low|medium|high)$")
    themes: List[str] = []
    energy_level: str = Field(..., pattern="^(low|medium|high)$")
    confidence_level: str = Field(..., pattern="^(low|medium|high)$")
    summary: str


class VoiceEntryCreate(BaseModel):
    """Voice entry creation model"""
    transcript: Optional[str] = None
    emotion_data: Optional[EmotionData] = None


class VoiceEntryResponse(BaseModel):
    """Voice entry response model"""
    id: str = Field(..., alias="_id")
    user_id: str
    audio_url: str
    transcript: Optional[str] = None
    emotion_data: Optional[EmotionData] = None
    created_at: datetime
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


class VoiceEntryListResponse(BaseModel):
    """List of voice entries"""
    entries: List[VoiceEntryResponse]
    total: int




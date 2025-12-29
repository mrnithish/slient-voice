"""
Voice entry routes
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from typing import Optional
import logging
from datetime import datetime
from bson import ObjectId

from app.models import VoiceEntryResponse, VoiceEntryListResponse, EmotionData
from app.routers.auth import get_current_user
from app.database import get_database
from app.storage import upload_audio_file, get_audio_url
from app.ai_agent import process_voice_entry

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/upload", response_model=VoiceEntryResponse)
async def upload_entry(
    audio: UploadFile = File(...),
    current_user_id: str = Depends(get_current_user)
):
    """
    Upload voice entry audio file
    Process audio: transcribe, analyze emotion, store in database
    """
    try:
        db = get_database()
        entries_collection = db.voice_entries
        
        # Validate audio file
        if not audio.content_type or not audio.content_type.startswith("audio/"):
            raise HTTPException(status_code=400, detail="Invalid file type. Audio file required.")
        
        # Check file size (max 50MB)
        audio.file.seek(0, 2)  # Seek to end
        file_size = audio.file.tell()
        audio.file.seek(0)  # Reset to beginning
        
        max_size = 50 * 1024 * 1024  # 50MB
        if file_size > max_size:
            raise HTTPException(
                status_code=400,
                detail="File too large. Maximum size is 50MB."
            )
        
        # Reset file pointer
        await audio.seek(0)
        
        # Upload audio to storage
        logger.info(f"Uploading audio file for user {current_user_id}")
        audio_url = await upload_audio_file(audio, current_user_id)
        
        # Process audio with AI agent
        logger.info(f"Processing audio with AI agent for user {current_user_id}")
        try:
            result = await process_voice_entry(audio)
            transcript = result.get("transcript", "")
            emotion_data = result.get("emotion_data")
        except Exception as ai_error:
            logger.error(f"AI processing failed: {ai_error}")
            # Continue without emotion data
            transcript = ""
            emotion_data = None
        
        # Create voice entry document
        entry = {
            "user_id": ObjectId(current_user_id),
            "audio_url": audio_url,
            "transcript": transcript,
            "emotion_data": emotion_data.dict() if emotion_data else None,
            "created_at": datetime.utcnow()
        }
        
        # Insert into database
        result = await entries_collection.insert_one(entry)
        entry["_id"] = result.inserted_id
        
        logger.info(f"Voice entry created: {result.inserted_id}")
        
        return VoiceEntryResponse(
            _id=str(entry["_id"]),
            user_id=current_user_id,
            audio_url=entry["audio_url"],
            transcript=entry["transcript"],
            emotion_data=emotion_data,
            created_at=entry["created_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading entry: {e}")
        raise HTTPException(
            status_code=500,
            detail="We couldn't analyze this entry. Please try again."
        )


@router.get("/list", response_model=VoiceEntryListResponse)
async def list_entries(
    current_user_id: str = Depends(get_current_user),
    limit: int = 50,
    skip: int = 0
):
    """
    Get list of voice entries for current user
    Sorted by date (newest first)
    """
    try:
        db = get_database()
        entries_collection = db.voice_entries
        
        # Query user's entries
        cursor = entries_collection.find(
            {"user_id": ObjectId(current_user_id)}
        ).sort("created_at", -1).skip(skip).limit(limit)
        
        entries = await cursor.to_list(length=limit)
        
        # Get total count
        total = await entries_collection.count_documents(
            {"user_id": ObjectId(current_user_id)}
        )
        
        # Convert to response models
        entry_responses = []
        for entry in entries:
            emotion_data = None
            if entry.get("emotion_data"):
                emotion_data = EmotionData(**entry["emotion_data"])
            
            entry_responses.append(
                VoiceEntryResponse(
                    _id=str(entry["_id"]),
                    user_id=str(entry["user_id"]),
                    audio_url=entry["audio_url"],
                    transcript=entry.get("transcript"),
                    emotion_data=emotion_data,
                    created_at=entry["created_at"]
                )
            )
        
        return VoiceEntryListResponse(entries=entry_responses, total=total)
        
    except Exception as e:
        logger.error(f"Error listing entries: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve entries")


@router.get("/{entry_id}", response_model=VoiceEntryResponse)
async def get_entry(
    entry_id: str,
    current_user_id: str = Depends(get_current_user)
):
    """
    Get specific voice entry by ID
    Only returns entry if it belongs to current user
    """
    try:
        db = get_database()
        entries_collection = db.voice_entries
        
        # Validate ObjectId
        if not ObjectId.is_valid(entry_id):
            raise HTTPException(status_code=400, detail="Invalid entry ID")
        
        # Find entry
        entry = await entries_collection.find_one({
            "_id": ObjectId(entry_id),
            "user_id": ObjectId(current_user_id)
        })
        
        if not entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        
        # Convert to response model
        emotion_data = None
        if entry.get("emotion_data"):
            emotion_data = EmotionData(**entry["emotion_data"])
        
        return VoiceEntryResponse(
            _id=str(entry["_id"]),
            user_id=str(entry["user_id"]),
            audio_url=entry["audio_url"],
            transcript=entry.get("transcript"),
            emotion_data=emotion_data,
            created_at=entry["created_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting entry: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve entry")


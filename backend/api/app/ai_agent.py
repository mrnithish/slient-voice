"""
Gemini AI Agent for emotion analysis
Handles speech-to-text and emotion analysis
"""

import json
import logging
from typing import Dict, Optional
from fastapi import UploadFile

from app.config import settings
from app.models import EmotionData

logger = logging.getLogger(__name__)

# Try to import Gemini SDK
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("Google Generative AI SDK not installed. AI features will be disabled.")


def init_gemini():
    """Initialize Gemini API client"""
    if not GEMINI_AVAILABLE:
        return None
    
    if not settings.GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY not set. AI features disabled.")
        return None
    
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        return genai
    except Exception as e:
        logger.error(f"Failed to initialize Gemini: {e}")
        return None


# Initialize Gemini on module load
_gemini = init_gemini()


async def process_voice_entry(audio: UploadFile) -> Dict:
    """
    Process voice entry: transcribe and analyze emotion
    Returns dict with transcript and emotion_data
    """
    if not _gemini:
        raise Exception("Gemini AI not available")
    
    try:
        # Step 1: Speech-to-Text
        logger.info("Starting speech-to-text transcription")
        transcript = await transcribe_audio(audio)
        
        if not transcript or len(transcript.strip()) == 0:
            raise Exception("Empty transcript received")
        
        logger.info(f"Transcript received ({len(transcript)} chars)")
        
        # Step 2: Emotion Analysis
        logger.info("Starting emotion analysis")
        emotion_data = await analyze_emotion(transcript)
        
        logger.info("Emotion analysis completed")
        
        return {
            "transcript": transcript,
            "emotion_data": emotion_data
        }
        
    except Exception as e:
        logger.error(f"Error processing voice entry: {e}")
        raise


async def transcribe_audio(audio: UploadFile) -> str:
    """
    Transcribe audio to text using Google Speech-to-Text API
    Falls back to Gemini multimodal if Speech-to-Text is not available
    """
    try:
        # Read audio file
        audio_content = await audio.read()
        
        # Reset file pointer for potential reuse
        await audio.seek(0)
        
        # Try Google Speech-to-Text API first
        try:
            from google.cloud import speech
            
            client = speech.SpeechClient()
            
            # Configure audio
            audio_data = speech.RecognitionAudio(content=audio_content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
                sample_rate_hertz=44100,
                language_code="en-US",
                enable_automatic_punctuation=True,
            )
            
            # Perform transcription
            response = client.recognize(config=config, audio=audio_data)
            
            # Extract transcript
            transcript = ""
            for result in response.results:
                transcript += result.alternatives[0].transcript + " "
            
            if transcript.strip():
                logger.info("Transcription successful via Speech-to-Text API")
                return transcript.strip()
                
        except ImportError:
            logger.warning("Google Cloud Speech-to-Text not available")
        except Exception as e:
            logger.warning(f"Speech-to-Text API failed: {e}, trying Gemini multimodal")
        
        # Fallback: Try Gemini multimodal (if supported)
        if _gemini:
            try:
                # Note: This requires Gemini 1.5 Pro or later with multimodal support
                # For audio, you may need to convert to a supported format first
                model = _gemini.GenerativeModel('gemini-1.5-pro')
                
                # Gemini may require base64 encoded audio or file path
                # This is a placeholder - adjust based on actual Gemini API capabilities
                import base64
                audio_b64 = base64.b64encode(audio_content).decode('utf-8')
                
                # Attempt transcription via Gemini (if it supports audio)
                # This may not work with current Gemini API - adjust as needed
                prompt = "Transcribe this audio to text. Return only the transcript, no other text."
                
                # Note: Actual implementation depends on Gemini's audio input format
                # You may need to use a different approach or API
                logger.warning("Gemini multimodal audio transcription may require different implementation")
                
            except Exception as e:
                logger.error(f"Gemini transcription attempt failed: {e}")
        
        # If all else fails, raise error
        raise Exception("Audio transcription not available. Please configure Google Speech-to-Text API or Gemini audio support.")
        
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        raise Exception("Failed to transcribe audio")


async def analyze_emotion(transcript: str) -> EmotionData:
    """
    Analyze emotion from transcript using Gemini
    Returns structured EmotionData
    """
    try:
        if not _gemini:
            raise Exception("Gemini not initialized")
        
        # Use EmotionAgent from ai module if available, otherwise use direct model
        try:
            import sys
            import os
            # Add ai module to path
            ai_module_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '..', 'ai')
            if os.path.exists(ai_module_path):
                sys.path.insert(0, os.path.dirname(ai_module_path))
                from gemini_agent.emotion_agent import EmotionAgent
            
            model = _gemini.GenerativeModel('gemini-pro')
            agent = EmotionAgent(gemini_model=model)
            emotion_dict = agent.analyze_emotion(transcript)
        except (ImportError, Exception) as e:
            logger.warning(f"Could not use EmotionAgent module: {e}, using direct model")
            # Fallback to direct model usage
            model = _gemini.GenerativeModel('gemini-pro')
            
            # Emotion analysis prompt
            prompt = f"""SYSTEM:
You are an Emotion Intelligence AI Agent.

You analyze personal voice diary text.

You must not give advice or solutions.

You must not act as a therapist.

Only return emotional insights.

USER INPUT:
{transcript}

TASK:
Return ONLY valid JSON in this format:

{{
  "primary_emotion": "",
  "secondary_emotions": [],
  "mood_score": -5 to 5,
  "stress_level": "low|medium|high",
  "themes": [],
  "energy_level": "low|medium|high",
  "confidence_level": "low|medium|high",
  "summary": ""
}}

Return ONLY the JSON object, no other text."""

            # Generate response
            response = model.generate_content(prompt)
            
            # Extract JSON from response
            response_text = response.text.strip()
            
            # Try to extract JSON if wrapped in markdown
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            # Parse JSON
            emotion_dict = json.loads(response_text)
        
        # Validate and create EmotionData
        emotion_data = EmotionData(**emotion_dict)
        
        return emotion_data
        
    except Exception as e:
        logger.error(f"Emotion analysis error: {e}")
        raise Exception("Failed to analyze emotion")


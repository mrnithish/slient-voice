"""
Emotion Intelligence AI Agent
Analyzes voice diary transcripts and returns structured emotional insights
"""

import json
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Emotion analysis prompt template
EMOTION_ANALYSIS_PROMPT = """SYSTEM:
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


class EmotionAgent:
    """Emotion Intelligence Agent for analyzing voice diary entries"""
    
    def __init__(self, gemini_model=None):
        """
        Initialize Emotion Agent
        
        Args:
            gemini_model: Initialized Gemini GenerativeModel instance
        """
        self.model = gemini_model
        if not self.model:
            logger.warning("Gemini model not provided. Agent will not function.")
    
    def analyze_emotion(self, transcript: str) -> Dict:
        """
        Analyze emotion from transcript
        
        Args:
            transcript: Text transcript of voice recording
            
        Returns:
            Dictionary with emotion analysis results
            
        Raises:
            Exception: If analysis fails
        """
        if not self.model:
            raise Exception("Gemini model not initialized")
        
        if not transcript or len(transcript.strip()) == 0:
            raise ValueError("Empty transcript provided")
        
        try:
            # Format prompt
            prompt = EMOTION_ANALYSIS_PROMPT.format(transcript=transcript)
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            # Extract JSON from response
            response_text = response.text.strip()
            
            # Clean response text
            response_text = self._extract_json(response_text)
            
            # Parse JSON
            emotion_dict = json.loads(response_text)
            
            # Validate structure
            self._validate_emotion_data(emotion_dict)
            
            logger.info(f"Emotion analysis completed for transcript ({len(transcript)} chars)")
            
            return emotion_dict
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse emotion JSON: {e}")
            logger.error(f"Response text: {response_text}")
            raise Exception("Invalid JSON response from AI")
        except Exception as e:
            logger.error(f"Emotion analysis error: {e}")
            raise Exception(f"Failed to analyze emotion: {str(e)}")
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from response text, handling markdown code blocks"""
        # Remove markdown code blocks if present
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        
        # Find JSON object boundaries
        start_idx = text.find('{')
        end_idx = text.rfind('}') + 1
        
        if start_idx != -1 and end_idx > start_idx:
            return text[start_idx:end_idx]
        
        return text.strip()
    
    def _validate_emotion_data(self, data: Dict):
        """Validate emotion data structure"""
        required_fields = [
            'primary_emotion',
            'mood_score',
            'stress_level',
            'energy_level',
            'confidence_level',
            'summary'
        ]
        
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate mood_score range
        mood_score = data.get('mood_score')
        if not isinstance(mood_score, int) or mood_score < -5 or mood_score > 5:
            raise ValueError(f"Invalid mood_score: {mood_score}. Must be between -5 and 5")
        
        # Validate enum fields
        stress_level = data.get('stress_level', '').lower()
        if stress_level not in ['low', 'medium', 'high']:
            raise ValueError(f"Invalid stress_level: {stress_level}")
        
        energy_level = data.get('energy_level', '').lower()
        if energy_level not in ['low', 'medium', 'high']:
            raise ValueError(f"Invalid energy_level: {energy_level}")
        
        confidence_level = data.get('confidence_level', '').lower()
        if confidence_level not in ['low', 'medium', 'high']:
            raise ValueError(f"Invalid confidence_level: {confidence_level}")




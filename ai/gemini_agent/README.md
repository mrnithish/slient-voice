# Gemini AI Agent Module

Standalone module for emotion intelligence analysis using Google Gemini AI.

## Purpose

This module provides emotion analysis capabilities for voice diary entries. It:
- Analyzes transcribed voice diary text
- Returns structured emotional insights
- Does NOT provide advice or therapeutic guidance
- Focuses solely on emotional pattern recognition

## Usage

```python
import google.generativeai as genai
from ai.gemini_agent.emotion_agent import EmotionAgent

# Initialize Gemini
genai.configure(api_key="your_api_key")
model = genai.GenerativeModel('gemini-pro')

# Create agent
agent = EmotionAgent(gemini_model=model)

# Analyze transcript
transcript = "I had a really stressful day at work today..."
result = agent.analyze_emotion(transcript)

print(result)
# {
#   "primary_emotion": "stressed",
#   "secondary_emotions": ["anxious", "overwhelmed"],
#   "mood_score": -3,
#   "stress_level": "high",
#   "themes": ["work", "pressure"],
#   "energy_level": "low",
#   "confidence_level": "medium",
#   "summary": "User expresses stress and anxiety about work..."
# }
```

## Output Format

The agent returns a structured JSON object with:

- `primary_emotion`: Main emotion detected (string)
- `secondary_emotions`: List of additional emotions (array)
- `mood_score`: Numeric score from -5 to +5 (integer)
- `stress_level`: "low", "medium", or "high" (string)
- `themes`: List of topics/themes identified (array)
- `energy_level`: "low", "medium", or "high" (string)
- `confidence_level`: "low", "medium", or "high" (string)
- `summary`: Brief summary of emotional state (string)

## Integration

This module is integrated into the FastAPI backend at `backend/api/app/ai_agent.py`.




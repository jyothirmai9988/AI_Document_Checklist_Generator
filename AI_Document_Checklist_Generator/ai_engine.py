"""Optional AI layer.

The main application works offline using rule-based detection.
This module is a starter point for connecting Gemini or another LLM.
"""

import os

def gemini_available():
    return bool(os.getenv("GEMINI_API_KEY"))

def generate_ai_checklist(text):
    """Return an AI-generated checklist when you connect your preferred model.

    This function is intentionally left as a safe extension point. The project
    does not require an API key to run.
    """
    if not gemini_available():
        return None
    # Add google-genai client logic here when an API key is configured.
    return None

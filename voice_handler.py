# voice_handler.py - OpenAI Whisper & TTS for voice features
import os
from openai import OpenAI
import tempfile

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def speech_to_text(audio_bytes):
    """Convert speech to text using OpenAI Whisper"""
    try:
        # Save audio bytes to temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            temp_audio.write(audio_bytes)
            temp_audio_path = temp_audio.name
        
        # Transcribe using Whisper
        with open(temp_audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="ko"  # Korean language
            )
        
        # Clean up temp file
        os.unlink(temp_audio_path)
        
        return transcript.text
    
    except Exception as e:
        print(f"Speech-to-text error: {e}")
        return None

def text_to_speech(text, language="ko"):
    """Convert text to speech using OpenAI TTS"""
    try:
        # Select voice based on language
        voice_map = {
            "ko": "alloy",  # Korean - natural voice
            "en": "nova",   # English
            "ja": "shimmer", # Japanese
            "zh": "fable"   # Chinese
        }
        
        voice = voice_map.get(language, "alloy")
        
        # Generate speech
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        
        # Return audio bytes
        return response.content
    
    except Exception as e:
        print(f"Text-to-speech error: {e}")
        return None

def get_language_code(language_mode):
    """Convert language mode to language code"""
    language_codes = {
        "한국어": "ko",
        "English": "en",
        "日本語": "ja",
        "中文": "zh"
    }
    return language_codes.get(language_mode, "ko")

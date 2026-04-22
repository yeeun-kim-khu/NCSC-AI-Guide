# voice.py - 음성 입출력 처리 (voice_handler.py에서 이름 변경)
import os
from openai import OpenAI
import tempfile
import streamlit as st
import base64
import requests
import re

_openai_client = None
_openai_client_key = None


def _safe_secret_get(key: str, default: str = "") -> str:
    try:
        return st.secrets.get(key, default)
    except Exception:
        return default


def _get_openai_api_key() -> str:
    key = os.environ.get("OPENAI_API_KEY", "")
    if (not key) and hasattr(st, "secrets"):
        key = _safe_secret_get("OPENAI_API_KEY", "")
    return key or ""


def _get_openai_client() -> OpenAI:
    global _openai_client, _openai_client_key
    key = _get_openai_api_key()
    if (not key):
        raise ValueError("OPENAI_API_KEY is missing")
    if _openai_client is None or _openai_client_key != key:
        _openai_client = OpenAI(api_key=key)
        _openai_client_key = key
    return _openai_client

def speech_to_text(audio_bytes):
    """Convert speech to text using OpenAI Whisper"""
    try:
        # Save audio bytes to temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            temp_audio.write(audio_bytes)
            temp_audio_path = temp_audio.name
        
        # Transcribe using Whisper
        with open(temp_audio_path, "rb") as audio_file:
            transcript = _get_openai_client().audio.transcriptions.create(
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
    text = preprocess_tts_text(text, language=language)
    eleven_key = os.environ.get("ELEVENLABS_API_KEY")
    if (not eleven_key) and hasattr(st, "secrets"):
        eleven_key = _safe_secret_get("ELEVENLABS_API_KEY", "")

    if eleven_key:
        eleven_voice_id = os.environ.get("ELEVENLABS_VOICE_ID")
        if (not eleven_voice_id) and hasattr(st, "secrets"):
            eleven_voice_id = _safe_secret_get("ELEVENLABS_VOICE_ID", "")
        if not eleven_voice_id:
            eleven_voice_id = "21m00Tcm4TlvDq8ikWAM"

        eleven_model_id = os.environ.get("ELEVENLABS_MODEL_ID")
        if (not eleven_model_id) and hasattr(st, "secrets"):
            eleven_model_id = _safe_secret_get("ELEVENLABS_MODEL_ID", "")
        if not eleven_model_id:
            eleven_model_id = "eleven_multilingual_v2"

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{eleven_voice_id}"
        headers = {
            "xi-api-key": eleven_key,
            "accept": "audio/mpeg",
            "content-type": "application/json",
        }
        payload = {
            "text": text,
            "model_id": eleven_model_id,
            "voice_settings": {
                "stability": 0.45,
                "similarity_boost": 0.75,
                "style": 0.35,
                "use_speaker_boost": True,
            },
        }
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            if resp.status_code == 200 and resp.content:
                return resp.content
            print(f"ElevenLabs TTS 오류: status={resp.status_code}, body={resp.text[:500]}")
        except Exception as e:
            print(f"ElevenLabs TTS 호출 오류: {e}")

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
        response = _get_openai_client().audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        
        # Return audio bytes
        return response.content
    
    except Exception as e:
        print(f"Text-to-speech error: {e}")
        return None


def get_tts_cache_namespace(language: str = "ko") -> str:
    eleven_key = os.environ.get("ELEVENLABS_API_KEY")
    if (not eleven_key) and hasattr(st, "secrets"):
        eleven_key = _safe_secret_get("ELEVENLABS_API_KEY", "")

    if eleven_key:
        eleven_voice_id = os.environ.get("ELEVENLABS_VOICE_ID")
        if (not eleven_voice_id) and hasattr(st, "secrets"):
            eleven_voice_id = _safe_secret_get("ELEVENLABS_VOICE_ID", "")
        if not eleven_voice_id:
            eleven_voice_id = "21m00Tcm4TlvDq8ikWAM"

        eleven_model_id = os.environ.get("ELEVENLABS_MODEL_ID")
        if (not eleven_model_id) and hasattr(st, "secrets"):
            eleven_model_id = _safe_secret_get("ELEVENLABS_MODEL_ID", "")
        if not eleven_model_id:
            eleven_model_id = "eleven_multilingual_v2"

        return f"elevenlabs::{eleven_model_id}::{eleven_voice_id}"

    voice_map = {
        "ko": "alloy",
        "en": "nova",
        "ja": "shimmer",
        "zh": "fable",
    }
    voice = voice_map.get(language, "alloy")
    return f"openai::tts-1::{voice}"

def get_language_code(language_mode):
    """Convert language mode to language code"""
    language_codes = {
        "한국어": "ko",
        "English": "en",
        "日本語": "ja",
        "中文": "zh"
    }
    return language_codes.get(language_mode, "ko")

def autoplay_audio(audio_bytes):
    """Auto-play audio in Streamlit"""
    try:
        b64 = base64.b64encode(audio_bytes).decode()
        audio_html = f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    except Exception as e:
        print(f"Autoplay error: {e}")


def preprocess_tts_text(text: str, language: str = "ko") -> str:
    if not text:
        return text
    if language != "ko":
        return text

    def _format_time(hh: str, mm: str) -> str:
        h = int(hh)
        m = int(mm)
        if m == 0:
            return f"{h}시"
        return f"{h}시 {m}분"

    def _repl(match: re.Match) -> str:
        h1, m1 = match.group(1), match.group(2)
        h2, m2 = match.group(3), match.group(4)
        if h2 and m2:
            return f"{_format_time(h1, m1)}부터 {_format_time(h2, m2)}까지"
        return _format_time(h1, m1)

    text = re.sub(r"\b(\d{1,2})\s*:\s*(\d{2})\s*[~∼-]\s*(\d{1,2})\s*:\s*(\d{2})\b", _repl, text)
    text = re.sub(r"\b(\d{1,2})\s*:\s*(\d{2})\b", _repl, text)
    return text

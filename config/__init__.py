"""Módulo de configuração do VictorIA"""

from .settings import (
    GROQ_API_KEY,
    WHISPER_MODEL,
    CHAT_MODEL,
    WAKE_WORDS,
    validate_api_key
)

__all__ = [
    'GROQ_API_KEY',
    'WHISPER_MODEL', 
    'CHAT_MODEL',
    'WAKE_WORDS',
    'validate_api_key'
]

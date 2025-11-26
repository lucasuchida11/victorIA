"""
core/transcription.py
Módulo de transcrição de áudio usando Groq Whisper
"""

import traceback
from groq import Groq
from config.settings import GROQ_API_KEY, WHISPER_MODEL


# Cliente Groq (singleton)
_client = None


def get_groq_client() -> Groq:
    """Retorna instância do cliente Groq (singleton)"""
    global _client
    if _client is None:
        _client = Groq(api_key=GROQ_API_KEY)
    return _client


def transcribe_audio(audio_path: str) -> str:
    """
    Transcreve arquivo de áudio usando Groq Whisper.
    
    Args:
        audio_path: Caminho do arquivo de áudio
    
    Returns:
        Texto transcrito
    
    Raises:
        Exception: Se houver erro na transcrição
    """
    print(f"[Transcription] Transcrevendo: {audio_path}")
    
    try:
        client = get_groq_client()
        
        with open(audio_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=WHISPER_MODEL,
                file=audio_file
            )
        
        text = transcription.text
        print(f"[Transcription] Resultado: {text}")
        
        return text
        
    except Exception as e:
        print(f"[Transcription] Erro: {e}")
        traceback.print_exc()
        return ""


def transcribe_audio_with_language(audio_path: str, language: str = "pt") -> str:
    """
    Transcreve áudio especificando o idioma.
    
    Args:
        audio_path: Caminho do arquivo de áudio
        language: Código do idioma (ex: 'pt', 'en')
    
    Returns:
        Texto transcrito
    """
    try:
        client = get_groq_client()
        
        with open(audio_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=WHISPER_MODEL,
                file=audio_file,
                language=language
            )
        
        return transcription.text
        
    except Exception as e:
        print(f"[Transcription] Erro: {e}")
        return ""
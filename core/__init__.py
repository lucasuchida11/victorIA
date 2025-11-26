"""Módulos principais do VictorIA"""

from .audio_capture import record_audio
from .transcription import transcribe_audio
from .chat import query_chat
from .tts import synthesize_text, start_edge_loop, stop_edge_loop

__all__ = [
    'record_audio',
    'transcribe_audio',
    'query_chat',
    'synthesize_text',
    'start_edge_loop',
    'stop_edge_loop'
]
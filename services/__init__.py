"""Serviços de alto nível do VictorIA"""

from .voice_handler import get_voice_handler, VoiceHandler
from .continuous_listener import get_continuous_listener, ContinuousListener

__all__ = [
    'get_voice_handler',
    'VoiceHandler',
    'get_continuous_listener',
    'ContinuousListener'
]
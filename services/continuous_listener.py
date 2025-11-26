"""
services/continuous_listener.py
Serviço de escuta contínua com VAD e wake-word detection
"""

import time
import threading
from typing import Callable, Optional
from core.audio_capture import record_audio
from core.transcription import transcribe_audio
from utils.text_cleaner import clean_transcript, remove_wake_words
from services.voice_handler import get_voice_handler
from config.settings import CONTINUOUS_CHUNK_DURATION, WAKE_WORDS


class ContinuousListener:
    """Listener contínuo com suporte a wake-word"""
    
    def __init__(self):
        self.running = False
        self.wake_word_enabled = True
        self.listener_thread = None
        self.on_transcript_callback = None
    
    def start(
        self,
        wake_word_enabled: bool = True,
        on_transcript_callback: Optional[Callable[[str], None]] = None
    ):
        """
        Inicia escuta contínua.
        
        Args:
            wake_word_enabled: Se True, requer wake-word
            on_transcript_callback: Callback chamado com cada transcrição
        """
        if self.running:
            print("[ContinuousListener] Já está rodando")
            return
        
        self.running = True
        self.wake_word_enabled = wake_word_enabled
        self.on_transcript_callback = on_transcript_callback
        
        self.listener_thread = threading.Thread(
            target=self._listen_loop,
            daemon=True
        )
        self.listener_thread.start()
        
        print(f"[ContinuousListener] Iniciado (wake-word={'ON' if wake_word_enabled else 'OFF'})")
    
    def stop(self):
        """Para a escuta contínua"""
        self.running = False
        
        if self.listener_thread:
            self.listener_thread.join(timeout=2.0)
        
        print("[ContinuousListener] Parado")
    
    def toggle_wake_word(self, enabled: bool):
        """Alterna detecção de wake-word"""
        self.wake_word_enabled = enabled
        print(f"[ContinuousListener] Wake-word={'ON' if enabled else 'OFF'}")
    
    def _listen_loop(self):
        """Loop principal de escuta"""
        handler = get_voice_handler()
        
        while self.running:
            try:
                # Grava chunk de áudio
                audio_path = record_audio(duration=CONTINUOUS_CHUNK_DURATION)
                
                # Transcreve
                raw_text = transcribe_audio(audio_path)
                cleaned = clean_transcript(raw_text)
                
                if not cleaned:
                    continue
                
                print(f"[ContinuousListener] Transcrito: {cleaned}")
                
                # Notifica callback
                if self.on_transcript_callback:
                    self.on_transcript_callback(cleaned)
                
                # Processa com/sem wake-word
                if self.wake_word_enabled:
                    self._process_with_wake_word(cleaned, handler)
                else:
                    self._process_without_wake_word(cleaned, handler)
                
            except Exception as e:
                print(f"[ContinuousListener] Erro no loop: {e}")
                time.sleep(0.5)
    
    def _process_with_wake_word(self, text: str, handler):
        """Processa texto verificando wake-word"""
        lower_text = text.lower()
        
        # Verifica se contém wake-word
        has_wake_word = any(w in lower_text for w in WAKE_WORDS)
        
        if not has_wake_word:
            return  # Ignora se não tem wake-word
        
        # Remove wake-word do texto
        cleaned = remove_wake_words(text, WAKE_WORDS)
        
        if cleaned:
            # Processa comando após wake-word
            handler.handle_user_text(cleaned, stream=True, synth_partial=True)
        else:
            # Wake-word isolado: resposta de confirmação
            handler.handle_quick_response("Tô ouvindo. Pode falar.")
    
    def _process_without_wake_word(self, text: str, handler):
        """Processa todo texto detectado"""
        handler.handle_user_text(text, stream=True, synth_partial=True)


# Instância singleton
_listener = None


def get_continuous_listener() -> ContinuousListener:
    """Retorna instância singleton do ContinuousListener"""
    global _listener
    if _listener is None:
        _listener = ContinuousListener()
    return _listener
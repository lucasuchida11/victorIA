"""
services/voice_handler.py
Serviço que orquestra o fluxo: transcrição → chat → TTS → reprodução
"""

from typing import Callable, Optional
from utils.text_cleaner import clean_transcript, sanitize_for_tts
from core.chat import query_chat
from core.tts import synthesize_text
from utils.audio_player import play_audio_blocking, play_audio_nonblocking
from config.settings import PARTIAL_SYNTH_THRESHOLD


class VoiceHandler:
    """Orquestrador do fluxo de voz completo"""
    
    def __init__(self):
        self.partial_buffer = ""
        self.last_synth_len = 0
    
    def handle_user_text(
        self,
        text: str,
        stream: bool = True,
        synth_partial: bool = True,
        on_response_callback: Optional[Callable[[str], None]] = None
    ) -> str:
        """
        Processa texto do usuário: chat → TTS → reprodução.
        
        Args:
            text: Texto transcrito do usuário
            stream: Se True, usa streaming do chat
            synth_partial: Se True, sintetiza parciais durante streaming
            on_response_callback: Callback chamado com resposta final
        
        Returns:
            Resposta completa do assistente
        """
        # Limpa texto
        cleaned = clean_transcript(text)
        if not cleaned:
            print("[VoiceHandler] Texto vazio após limpeza")
            return ""
        
        print(f"[VoiceHandler] Processando: {cleaned}")
        
        # Reset buffers
        self.partial_buffer = ""
        self.last_synth_len = 0
        
        # Callback para tokens do streaming
        def on_token(token: str, buffer_text: str):
            self.partial_buffer = buffer_text
            
            # Sintetiza parciais se habilitado
            if synth_partial:
                delta = len(self.partial_buffer) - self.last_synth_len
                
                if delta >= PARTIAL_SYNTH_THRESHOLD:
                    chunk = self.partial_buffer[self.last_synth_len:]
                    self.last_synth_len = len(self.partial_buffer)
                    
                    # Sintetiza e reproduz chunk
                    sanitized = sanitize_for_tts(chunk)
                    if sanitized:
                        audio_path = synthesize_text(sanitized)
                        if audio_path:
                            play_audio_nonblocking(audio_path)
        
        # Envia para chat
        if stream:
            final_response = query_chat(
                cleaned,
                stream=True,
                on_token_callback=on_token
            )
        else:
            final_response = query_chat(
                cleaned,
                stream=False
            )
        
        # Processa resposta final
        if final_response:
            print(f"[VoiceHandler] Resposta final: {final_response[:100]}...")
            
            # Sanitiza para TTS
            final_clean = sanitize_for_tts(final_response.strip())
            
            # Sintetiza e reproduz resposta completa
            if final_clean:
                audio_path = synthesize_text(final_clean)
                if audio_path:
                    play_audio_blocking(audio_path)
            
            # Callback
            if on_response_callback:
                on_response_callback(final_response)
        
        return final_response
    
    def handle_quick_response(self, text: str):
        """
        Gera resposta rápida sem streaming (ex: confirmações).
        
        Args:
            text: Texto a ser falado
        """
        sanitized = sanitize_for_tts(text)
        if sanitized:
            audio_path = synthesize_text(sanitized)
            if audio_path:
                play_audio_nonblocking(audio_path)


# Instância singleton
_handler = None


def get_voice_handler() -> VoiceHandler:
    """Retorna instância singleton do VoiceHandler"""
    global _handler
    if _handler is None:
        _handler = VoiceHandler()
    return _handler
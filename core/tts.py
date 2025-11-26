"""
core/tts.py
Módulo de Text-to-Speech usando edge-tts
"""

import os
import re
import asyncio
import tempfile
import threading
import edge_tts
from config.settings import TTS_VOICE, TTS_TMP_DIR, TTS_TIMEOUT


# Event loop asyncio para edge-tts
_edge_loop = None
_loop_thread = None


def start_edge_loop():
    """Inicia loop asyncio em thread separada para edge-tts"""
    global _edge_loop, _loop_thread
    
    if _edge_loop is not None:
        return
    
    _edge_loop = asyncio.new_event_loop()
    
    def _run_loop(loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()
    
    _loop_thread = threading.Thread(target=_run_loop, args=(_edge_loop,), daemon=True)
    _loop_thread.start()
    print("[TTS] Loop asyncio iniciado")


def stop_edge_loop():
    """Para o loop asyncio"""
    global _edge_loop
    if _edge_loop:
        _edge_loop.call_soon_threadsafe(_edge_loop.stop)
        _edge_loop = None
        print("[TTS] Loop asyncio parado")


async def _synthesize_async(text: str, voice: str = TTS_VOICE) -> str:
    """
    Sintetiza texto em áudio (versão async).
    
    Returns:
        Caminho do arquivo MP3 gerado
    """
    # Sanitiza nome do arquivo
    safe_name = re.sub(r"[^0-9A-Za-z\-_. ]+", "", text[:40]).strip() or "chunk"
    
    # Cria arquivo temporário
    fd, path = tempfile.mkstemp(
        prefix=f"tts_{safe_name}_",
        suffix=".mp3",
        dir=TTS_TMP_DIR
    )
    os.close(fd)
    
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(path)
        print(f"[TTS] Sintetizado: {path}")
        return path
    except Exception as e:
        print(f"[TTS] Erro ao sintetizar: {e}")
        return ""


def synthesize_text(text: str, voice: str = TTS_VOICE) -> str:
    """
    Sintetiza texto em áudio (versão síncrona).
    
    Args:
        text: Texto para sintetizar
        voice: Voz do edge-tts
    
    Returns:
        Caminho do arquivo MP3 gerado
    """
    if not text or not text.strip():
        return ""
    
    if _edge_loop is None:
        print("[TTS] Erro: Loop não iniciado")
        return ""
    
    print(f"[TTS] Sintetizando: {text[:50]}...")
    
    try:
        coro = _synthesize_async(text, voice)
        future = asyncio.run_coroutine_threadsafe(coro, _edge_loop)
        return future.result(timeout=TTS_TIMEOUT)
    except Exception as e:
        print(f"[TTS] Erro: {e}")
        return ""


def get_available_voices():
    """Retorna lista de vozes disponíveis (async wrapper)"""
    async def _get_voices():
        voices = await edge_tts.list_voices()
        return voices
    
    if _edge_loop:
        future = asyncio.run_coroutine_threadsafe(_get_voices(), _edge_loop)
        try:
            return future.result(timeout=10)
        except:
            return []
    return []


def get_portuguese_voices():
    """Retorna apenas vozes em português"""
    voices = get_available_voices()
    return [v for v in voices if v.get("Locale", "").startswith("pt-")]
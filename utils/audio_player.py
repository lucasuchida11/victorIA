"""
utils/audio_player.py
Módulo para reprodução de áudio usando pygame
"""

import os
import threading
import pygame


# Lock para evitar reproduções simultâneas
_play_lock = threading.Lock()


def play_audio_blocking(audio_path: str) -> bool:
    """
    Reproduz arquivo de áudio de forma bloqueante.
    
    Args:
        audio_path: Caminho do arquivo de áudio
    
    Returns:
        True se reproduzido com sucesso, False caso contrário
    """
    if not audio_path or not os.path.exists(audio_path):
        print(f"[AudioPlayer] Arquivo não encontrado: {audio_path}")
        return False
    
    try:
        with _play_lock:
            print(f"[AudioPlayer] Reproduzindo: {audio_path}")
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            
            # Aguarda término da reprodução
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(30)
            
            print(f"[AudioPlayer] Reprodução finalizada")
            return True
            
    except Exception as e:
        print(f"[AudioPlayer] Erro ao reproduzir: {e}")
        return False


def play_audio_nonblocking(audio_path: str):
    """
    Reproduz arquivo de áudio em thread separada (não-bloqueante).
    
    Args:
        audio_path: Caminho do arquivo de áudio
    """
    thread = threading.Thread(
        target=play_audio_blocking,
        args=(audio_path,),
        daemon=True
    )
    thread.start()


def stop_playback():
    """Para a reprodução atual"""
    try:
        pygame.mixer.music.stop()
        print("[AudioPlayer] Reprodução interrompida")
    except Exception as e:
        print(f"[AudioPlayer] Erro ao parar: {e}")


def is_playing() -> bool:
    """Verifica se há áudio sendo reproduzido"""
    try:
        return pygame.mixer.music.get_busy()
    except:
        return False


def set_volume(volume: float):
    """
    Ajusta volume da reprodução.
    
    Args:
        volume: Volume de 0.0 a 1.0
    """
    try:
        volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(volume)
        print(f"[AudioPlayer] Volume ajustado para {volume:.2f}")
    except Exception as e:
        print(f"[AudioPlayer] Erro ao ajustar volume: {e}")


def get_volume() -> float:
    """Retorna volume atual (0.0 a 1.0)"""
    try:
        return pygame.mixer.music.get_volume()
    except:
        return 1.0
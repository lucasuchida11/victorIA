"""
core/audio_capture.py
Módulo de captura de áudio do microfone
"""

import sounddevice as sd
from scipy.io.wavfile import write
from config.settings import AUDIO_SAMPLE_RATE, AUDIO_CHANNELS, AUDIO_DTYPE, AUDIO_TMP_FILE


def record_audio(duration: float, fs: int = AUDIO_SAMPLE_RATE, 
                 filename: str = AUDIO_TMP_FILE) -> str:
    """
    Grava áudio do microfone e salva em arquivo WAV.
    
    Args:
        duration: Duração da gravação em segundos
        fs: Taxa de amostragem (Hz)
        filename: Caminho do arquivo de saída
    
    Returns:
        Caminho do arquivo gravado
    
    Raises:
        Exception: Se houver erro na gravação
    """
    print(f"[AudioCapture] Capturando áudio por {duration:.1f}s")
    
    try:
        # Grava áudio
        audio = sd.rec(
            int(duration * fs), 
            samplerate=fs, 
            channels=AUDIO_CHANNELS, 
            dtype=AUDIO_DTYPE
        )
        sd.wait()
        
        # Salva em arquivo WAV
        write(filename, fs, audio)
        print(f"[AudioCapture] Áudio salvo em: {filename}")
        
        return filename
        
    except Exception as e:
        print(f"[AudioCapture] Erro ao gravar: {e}")
        raise


def get_audio_devices():
    """Retorna lista de dispositivos de áudio disponíveis"""
    return sd.query_devices()


def set_default_device(device_id: int = None):
    """Define dispositivo de áudio padrão"""
    if device_id is not None:
        sd.default.device = device_id
"""
utils/text_cleaner.py
Módulo para limpeza e sanitização de texto
"""

import re


def clean_transcript(text: str) -> str:
    """
    Limpa transcrição removendo símbolos, emojis e marcações.
    
    Args:
        text: Texto a ser limpo
    
    Returns:
        Texto limpo e sanitizado
    """
    if not text:
        return ""
    
    text = str(text)
    
    # Remove segmentos entre asteriscos *...*
    text = re.sub(r"\*.*?\*", " ", text)
    
    # Remove conteúdo entre colchetes [...]
    text = re.sub(r"\[.*?\]", " ", text)
    
    # Remove tags <...>
    text = re.sub(r"<.*?>", " ", text)
    
    # Remove barras
    text = text.replace("/", " ").replace("\\", " ")
    
    # Remove hashtags
    text = text.replace("#", " ")
    
    # Remove emoticons simples :) :D :(
    text = re.sub(r"[:;=8][\-^]?[)DPOp]", " ", text)
    
    # Remove asteriscos e underscores
    text = text.replace("*", " ").replace("_", " ")
    
    # Remove outros símbolos problemáticos
    text = re.sub(r"[\{\}\[\]\|\~\^\`\<\>]", " ", text)
    
    # Colapsa múltiplos espaços em um só
    text = re.sub(r"\s+", " ", text).strip()
    
    return text


def remove_wake_words(text: str, wake_words: list) -> str:
    """
    Remove wake words do texto.
    
    Args:
        text: Texto original
        wake_words: Lista de wake words para remover
    
    Returns:
        Texto sem wake words
    """
    lower_text = text.lower()
    
    for wake_word in wake_words:
        lower_text = lower_text.replace(wake_word.lower(), "")
    
    # Limpa novamente após remoção
    return re.sub(r"\s+", " ", lower_text).strip()


def sanitize_for_tts(text: str) -> str:
    """
    Sanitiza texto especificamente para TTS.
    Remove URLs, emails, e outros elementos que não devem ser falados.
    
    Args:
        text: Texto original
    
    Returns:
        Texto sanitizado para TTS
    """
    # Remove URLs
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"www\.\S+", "", text)
    
    # Remove emails
    text = re.sub(r"\S+@\S+", "", text)
    
    # Remove números de telefone (formato BR)
    text = re.sub(r"\(\d{2}\)\s?\d{4,5}-?\d{4}", "", text)
    
    # Remove múltiplos sinais de pontuação
    text = re.sub(r"([!?.]){2,}", r"\1", text)
    
    # Limpa espaços
    text = re.sub(r"\s+", " ", text).strip()
    
    return text


def truncate_text(text: str, max_length: int = 500) -> str:
    """
    Trunca texto mantendo integridade de frases.
    
    Args:
        text: Texto original
        max_length: Comprimento máximo
    
    Returns:
        Texto truncado
    """
    if len(text) <= max_length:
        return text
    
    # Tenta cortar no último ponto antes do limite
    truncated = text[:max_length]
    last_period = truncated.rfind(".")
    
    if last_period > max_length * 0.7:  # Se encontrou ponto razoavelmente próximo
        return truncated[:last_period + 1]
    
    # Senão, corta no último espaço
    last_space = truncated.rfind(" ")
    if last_space > 0:
        return truncated[:last_space] + "..."
    
    return truncated + "..."
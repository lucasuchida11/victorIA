"""
core/chat.py
Módulo de chat usando Groq (GPT-OSS-20B)
"""

import traceback
from typing import Callable, Optional
from core.transcription import get_groq_client
from config.settings import (
    CHAT_MODEL, 
    SYSTEM_PROMPT, 
    CHAT_TEMPERATURE, 
    CHAT_MAX_TOKENS
)


def query_chat(
    user_text: str,
    stream: bool = True,
    on_token_callback: Optional[Callable[[str, str], None]] = None,
    temperature: float = CHAT_TEMPERATURE,
    max_tokens: int = CHAT_MAX_TOKENS
) -> str:
    """
    Envia mensagem para o chat e retorna resposta.
    
    Args:
        user_text: Texto do usuário
        stream: Se True, streaming de tokens
        on_token_callback: Callback(token, buffer_completo) chamado a cada token
        temperature: Temperatura do modelo (0-2)
        max_tokens: Máximo de tokens na resposta
    
    Returns:
        Resposta completa do assistente
    """
    print(f"[Chat] Query: {user_text[:100]}...")
    
    try:
        client = get_groq_client()
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ]
        
        if stream:
            return _stream_chat(client, messages, on_token_callback, temperature, max_tokens)
        else:
            return _non_stream_chat(client, messages, temperature, max_tokens)
            
    except Exception as e:
        print(f"[Chat] Erro: {e}")
        traceback.print_exc()
        return ""


def _stream_chat(
    client,
    messages: list,
    on_token_callback: Optional[Callable],
    temperature: float,
    max_tokens: int
) -> str:
    """Processa chat em modo streaming"""
    completion = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        temperature=temperature,
        max_completion_tokens=max_tokens,
        stream=True
    )
    
    buffer_text = ""
    
    for chunk in completion:
        try:
            delta = chunk.choices[0].delta
            token = getattr(delta, "content", None) or (
                delta.get("content") if isinstance(delta, dict) else None
            )
        except Exception:
            token = None
        
        if token:
            buffer_text += token
            if on_token_callback:
                on_token_callback(token, buffer_text)
    
    print(f"[Chat] Resposta completa: {buffer_text[:100]}...")
    return buffer_text


def _non_stream_chat(
    client,
    messages: list,
    temperature: float,
    max_tokens: int
) -> str:
    """Processa chat em modo não-streaming"""
    completion = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        temperature=temperature,
        max_completion_tokens=max_tokens,
        stream=False
    )
    
    text = completion.choices[0].message.content
    print(f"[Chat] Resposta: {text[:100]}...")
    return text


def query_chat_with_history(
    user_text: str,
    history: list,
    stream: bool = True,
    on_token_callback: Optional[Callable] = None
) -> str:
    """
    Envia mensagem com histórico de conversa.
    
    Args:
        user_text: Texto atual do usuário
        history: Lista de mensagens anteriores [{"role": "...", "content": "..."}]
        stream: Se True, streaming
        on_token_callback: Callback para tokens
    
    Returns:
        Resposta do assistente
    """
    try:
        client = get_groq_client()
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
        messages.append({"role": "user", "content": user_text})
        
        if stream:
            return _stream_chat(client, messages, on_token_callback, CHAT_TEMPERATURE, CHAT_MAX_TOKENS)
        else:
            return _non_stream_chat(client, messages, CHAT_TEMPERATURE, CHAT_MAX_TOKENS)
            
    except Exception as e:
        print(f"[Chat] Erro com histórico: {e}")
        return ""
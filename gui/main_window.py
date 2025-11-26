"""
gui/main_window.py
Interface gráfica principal do VictorIA
"""

import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from core.audio_capture import record_audio
from core.transcription import transcribe_audio
from utils.text_cleaner import clean_transcript
from services.continuous_listener import get_continuous_listener
from services.voice_handler import get_voice_handler
from config.settings import (
    GUI_TITLE,
    GUI_GEOMETRY,
    WAKE_WORDS,
    PTT_DURATION,
    WAKE_WORD_ENABLED_DEFAULT
)


class VoiceGUI:
    """Interface gráfica Tkinter para VictorIA"""
    
    def __init__(self, root):
        self.root = root
        self.listener = get_continuous_listener()
        self.handler = get_voice_handler()
        
        # Configuração da janela
        root.title(GUI_TITLE)
        root.geometry(GUI_GEOMETRY)
        
        # Variáveis de controle
        self.cb_wake = tk.IntVar(value=1 if WAKE_WORD_ENABLED_DEFAULT else 0)
        self.cb_partial = tk.IntVar(value=1)
        self.status_var = tk.StringVar(value="Stopped")
        
        # Constrói interface
        self._build_ui()
    
    def _build_ui(self):
        """Constrói elementos da interface"""
        # Frame superior (botões e controles)
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=8, pady=6)
        
        # Botões à esquerda
        btn_frame = tk.Frame(top_frame)
        btn_frame.pack(side=tk.LEFT)
        
        self.btn_start = tk.Button(
            btn_frame,
            text="Start",
            width=10,
            command=self._on_start
        )
        self.btn_start.grid(row=0, column=0, padx=4)
        
        self.btn_stop = tk.Button(
            btn_frame,
            text="Stop",
            width=10,
            command=self._on_stop,
            state=tk.DISABLED
        )
        self.btn_stop.grid(row=0, column=1, padx=4)
        
        self.btn_ptt = tk.Button(
            btn_frame,
            text="Push-to-Talk",
            width=12,
            command=self._on_push_to_talk
        )
        self.btn_ptt.grid(row=0, column=2, padx=4)
        
        # Checkboxes
        self.chk_wake = tk.Checkbutton(
            btn_frame,
            text="Wake-word",
            variable=self.cb_wake,
            command=self._on_toggle_wake
        )
        self.chk_wake.grid(row=0, column=3, padx=6)
        
        self.chk_partial = tk.Checkbutton(
            btn_frame,
            text="Partial TTS (stream)",
            variable=self.cb_partial
        )
        self.chk_partial.grid(row=0, column=4, padx=6)
        
        # Status à direita
        right_frame = tk.Frame(top_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        tk.Label(right_frame, text="Status:").pack(anchor="e")
        tk.Label(
            right_frame,
            textvariable=self.status_var,
            fg="green"
        ).pack(anchor="e")
        
        # Área de histórico
        self.txt = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            height=18
        )
        self.txt.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)
        self.txt.insert(tk.END, "Histórico de conversa:\n")
        self.txt.configure(state=tk.DISABLED)
        
        # Footer
        footer = tk.Frame(self.root)
        footer.pack(fill=tk.X, padx=8, pady=6)
        
        tk.Label(
            footer,
            text=f"Wake words: {', '.join(WAKE_WORDS)}"
        ).pack(side=tk.LEFT)
    
    def _set_status(self, status: str):
        """Atualiza status na interface"""
        self.status_var.set(status)
        self.root.update_idletasks()
    
    def _append_history(self, who: str, text: str):
        """Adiciona mensagem ao histórico"""
        self.txt.configure(state=tk.NORMAL)
        self.txt.insert(tk.END, f"\n[{who}] {text}\n")
        self.txt.see(tk.END)
        self.txt.configure(state=tk.DISABLED)
    
    def _on_start(self):
        """Handler do botão Start"""
        self.btn_start.configure(state=tk.DISABLED)
        self.btn_stop.configure(state=tk.NORMAL)
        self._set_status("Running (continuous)")
        self._append_history("System", "Modo contínuo ativado.")
        
        # Inicia listener contínuo
        wake_enabled = bool(self.cb_wake.get())
        self.listener.start(
            wake_word_enabled=wake_enabled,
            on_transcript_callback=lambda t: self._append_history("You", t)
        )
    
    def _on_stop(self):
        """Handler do botão Stop"""
        self.listener.stop()
        
        self.btn_start.configure(state=tk.NORMAL)
        self.btn_stop.configure(state=tk.DISABLED)
        self._set_status("Stopped")
        self._append_history("System", "Parado.")
    
    def _on_push_to_talk(self):
        """Handler do botão Push-to-Talk"""
        self._set_status("Listening (PTT)")
        self._append_history("System", "Push-to-talk: gravando...")
        
        # Executa em thread separada
        thread = threading.Thread(
            target=self._ptt_thread,
            daemon=True
        )
        thread.start()
    
    def _ptt_thread(self):
        """Thread que executa Push-to-Talk"""
        try:
            # Grava áudio
            audio_path = record_audio(duration=PTT_DURATION)
            
            # Transcreve
            raw_text = transcribe_audio(audio_path)
            cleaned = clean_transcript(raw_text)
            
            # Atualiza interface
            self._append_history("You", cleaned)
            self._append_history("System", "Enviando para a IA...")
            
            # Processa com IA
            synth_partial = bool(self.cb_partial.get())
            response = self.handler.handle_user_text(
                cleaned,
                stream=True,
                synth_partial=synth_partial
            )
            
            # Mostra resposta
            self._append_history("Assistant", "[resposta reproduzida]")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no PTT: {e}")
        
        finally:
            self._set_status("Idle")
    
    def _on_toggle_wake(self):
        """Handler do checkbox Wake-word"""
        enabled = bool(self.cb_wake.get())
        self.listener.toggle_wake_word(enabled)
        self._append_history(
            "System",
            f"Wake-word={'ON' if enabled else 'OFF'}"
        )
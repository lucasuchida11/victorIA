"""
main.py
VictorIA - Ponto de entrada da aplicação
"""

import tkinter as tk
import pygame
from config.settings import validate_api_key
from core.tts import start_edge_loop, stop_edge_loop
from gui.main_window import VoiceGUI


def main():
    """Ponto de entrada principal da aplicação"""
    # Valida API key
    if not validate_api_key():
        print("ERRO: Defina sua variável GROQ_API_KEY no arquivo .env ou como variável de ambiente.")
        return

    # Inicializa componentes
    pygame.mixer.init()
    start_edge_loop()

    # Cria e executa GUI
    root = tk.Tk()
    gui = VoiceGUI(root)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Saindo...")
    finally:
        pygame.mixer.quit()
        stop_edge_loop()


if __name__ == "__main__":
    main()
# 🎙️ VictorIA - Assistente de Voz Inteligente

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

**Assistente de voz conversacional com IA, interface gráfica e síntese de voz em português brasileiro**

[Características](#-características) •
[Instalação](#-instalação) •
[Uso](#️-uso) •
[Configuração](#️-configuração) •
[Documentação](#-documentação)

</div>

---

## 📖 Sobre o Projeto

VictorIA é um assistente de voz inteligente desenvolvido em Python que combina tecnologias de ponta para criar uma experiência conversacional natural. O projeto integra:

- 🎤 **Transcrição de áudio** via Groq Whisper (whisper-large-v3)
- 🤖 **IA conversacional** com Groq GPT-OSS-20B em streaming
- 🗣️ **Síntese de voz** em português brasileiro (Microsoft edge-tts)
- 🖥️ **Interface gráfica** intuitiva em Tkinter
- 🎯 **Detecção de wake-word** personalizável
- ⚡ **Streaming de resposta** com síntese parcial em tempo real

## ✨ Características

### 🎯 Funcionalidades Principais

- **Modo Push-to-Talk**: Clique e fale - ideal para comandos pontuais
- **Modo Contínuo**: Escuta automática com detecção de voz (VAD)
- **Wake-word Detection**: Ative apenas dizendo "Victoria" ou "Zara"
- **Streaming Inteligente**: Respostas começam a ser faladas antes do término da geração
- **Limpeza de Texto**: Remove símbolos e emojis automaticamente para áudio natural
- **Histórico Visual**: Acompanhe toda a conversa na interface

### 🏗️ Arquitetura Modular

```
victoria/
├── main.py                      # Ponto de entrada
├── config/                      # Configurações centralizadas
├── core/                        # Núcleo (áudio, transcrição, chat, TTS)
├── utils/                       # Utilitários (limpeza, reprodução)
├── services/                    # Lógica de negócio
└── gui/                         # Interface gráfica
```

**Vantagens da arquitetura:**
- ✅ Código organizado e fácil de manter
- ✅ Componentes testáveis individualmente
- ✅ Baixo acoplamento entre módulos
- ✅ Reutilização de código
- ✅ Fácil extensão e customização

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Microfone funcional
- Alto-falantes ou fones de ouvido
- Conta Groq (gratuita) para API key

### Passo a Passo

#### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/victoria.git
cd victoria
```

#### 2. Crie um ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

#### 4. Configure a API Key do Groq

##### Opção A: Arquivo .env (Recomendado)

```bash
# Copie o template
cp .env.example .env

# Edite o arquivo .env
nano .env  # ou use seu editor favorito
```

Adicione sua chave:
```env
GROQ_API_KEY=gsk_sua_chave_aqui
```

##### Opção B: Variável de ambiente

```bash
# Windows
set GROQ_API_KEY=gsk_sua_chave_aqui

# Linux/Mac
export GROQ_API_KEY=gsk_sua_chave_aqui
```

**🔑 Obtenha sua chave gratuita em:** https://console.groq.com/keys

#### 5. Execute o aplicativo

```bash
python main.py
```

## 🖥️ Uso

### Interface Gráfica

![Interface](https://via.placeholder.com/800x500?text=VictorIA+Interface)

#### Controles Principais

| Botão/Controle | Função |
|----------------|--------|
| **Start** | Inicia modo de escuta contínua |
| **Stop** | Para a escuta contínua |
| **Push-to-Talk** | Grava 4 segundos de áudio sob demanda |
| **Wake-word** | Ativa/desativa detecção de palavra-chave |
| **Partial TTS** | Ativa/desativa síntese parcial durante streaming |

### Modos de Operação

#### 🎤 Modo Push-to-Talk

1. Clique no botão **"Push-to-Talk"**
2. Fale por até 4 segundos
3. Aguarde a transcrição e resposta
4. O áudio da resposta será reproduzido automaticamente

**Ideal para:** Comandos rápidos, perguntas pontuais

#### 🔄 Modo Contínuo

1. Clique em **"Start"**
2. O sistema ficará escutando continuamente
3. Fale naturalmente
4. Clique em **"Stop"** quando terminar

**Ideal para:** Conversas longas, múltiplas interações

#### 🎯 Modo Wake-word

1. Ative a checkbox **"Wake-word"**
2. Diga uma das palavras-chave: "Victoria", "Zara", "Assistente"
3. Continue falando seu comando após a wake-word
4. O sistema responderá apenas quando detectar a palavra-chave

**Palavras-chave disponíveis:**
- victoria
- zara
- assistente
- hey zara
- hey victoria

**Ideal para:** Ambientes compartilhados, evitar ativações acidentais

### Exemplos de Uso

```
Você: "Victoria, qual é a previsão do tempo hoje?"
VictorIA: "Desculpe, não tenho acesso a dados em tempo real..."

Você: "Me conte uma piada"
VictorIA: "Por que o livro de matemática estava triste? Porque tinha muitos problemas!"

Você: "Explique o que é inteligência artificial"
VictorIA: "Inteligência artificial é..."
```

## ⚙️ Configuração

### Arquivo config/settings.py

Personalize o comportamento do VictorIA editando as configurações:

#### 🎤 Configurações de Áudio

```python
AUDIO_SAMPLE_RATE = 16000        # Taxa de amostragem (Hz)
VAD_ENERGY_THRESHOLD = 300       # Limiar de detecção de voz
PTT_DURATION = 4.0               # Duração do Push-to-Talk (segundos)
CONTINUOUS_CHUNK_DURATION = 3.0  # Duração dos chunks no modo contínuo
```

#### 🤖 Configurações de IA

```python
WHISPER_MODEL = "whisper-large-v3"     # Modelo de transcrição
CHAT_MODEL = "openai/gpt-oss-20b"      # Modelo de chat
CHAT_TEMPERATURE = 0.8                  # Criatividade (0.0 a 2.0)
CHAT_MAX_TOKENS = 1024                  # Comprimento máximo da resposta
```

#### 🗣️ Configurações de TTS

```python
TTS_VOICE = "pt-BR-FranciscaNeural"    # Voz do edge-tts
PARTIAL_SYNTH_THRESHOLD = 60            # Caracteres antes de sintetizar parcial
```

**Vozes disponíveis em português:**
- `pt-BR-FranciscaNeural` (Feminina)
- `pt-BR-AntonioNeural` (Masculino)
- `pt-PT-RaquelNeural` (Português de Portugal - Feminina)
- `pt-PT-DuarteNeural` (Português de Portugal - Masculino)

#### 🎯 Wake Words

```python
WAKE_WORDS = ["victoria", "zara", "assistente", "hey zara", "hey victoria"]
```

Adicione suas próprias palavras-chave à lista!

#### 💬 System Prompt

Personalize a personalidade do assistente:

```python
SYSTEM_PROMPT = (
    "Você é uma assistente de voz natural e amigável. "
    "Responda de forma breve e clara, como em uma conversa normal. "
    "Seja educada e prestativa."
)
```

## 🧪 Testando Componentes

### Teste Individual de Módulos

```python
# 1. Teste de captura de áudio
from core.audio_capture import record_audio
audio_path = record_audio(duration=3.0)
print(f"Áudio gravado em: {audio_path}")

# 2. Teste de transcrição
from core.transcription import transcribe_audio
text = transcribe_audio(audio_path)
print(f"Transcrição: {text}")

# 3. Teste de limpeza de texto
from utils.text_cleaner import clean_transcript
cleaned = clean_transcript(text)
print(f"Texto limpo: {cleaned}")

# 4. Teste de chat
from core.chat import query_chat
response = query_chat("Olá, como você está?")
print(f"Resposta: {response}")

# 5. Teste de TTS
from core.tts import synthesize_text, start_edge_loop
start_edge_loop()
audio_path = synthesize_text("Olá, mundo!")
print(f"Áudio TTS: {audio_path}")

# 6. Teste de reprodução
from utils.audio_player import play_audio_blocking
play_audio_blocking(audio_path)
```

### Teste do Fluxo Completo

```python
from services.voice_handler import get_voice_handler
from core.tts import start_edge_loop

# Inicializa
start_edge_loop()
handler = get_voice_handler()

# Processa texto
response = handler.handle_user_text(
    "Conte-me uma curiosidade sobre Python",
    stream=True,
    synth_partial=True
)
print(f"Resposta gerada: {response}")
```

## 📚 Documentação

### Estrutura de Módulos

#### 📦 config/
Configurações centralizadas do sistema.

- `settings.py`: Todas as constantes e configurações

#### 🎯 core/
Funcionalidades principais de baixo nível.

- `audio_capture.py`: Captura de áudio do microfone via sounddevice
- `transcription.py`: Transcrição com Groq Whisper API
- `chat.py`: Interação com Groq Chat API (streaming)
- `tts.py`: Síntese de voz com edge-tts (async)

#### 🛠️ utils/
Utilitários auxiliares.

- `text_cleaner.py`: Limpeza e sanitização de texto
- `audio_player.py`: Reprodução de áudio com pygame

#### 🎬 services/
Lógica de negócio e orquestração.

- `voice_handler.py`: Orquestra o fluxo completo (transcrição → chat → TTS)
- `continuous_listener.py`: Loop de escuta contínua com VAD e wake-word

#### 🖼️ gui/
Interface gráfica do usuário.

- `main_window.py`: Janela principal Tkinter com todos os controles

### APIs Principais

#### VoiceHandler

```python
from services.voice_handler import get_voice_handler

handler = get_voice_handler()

response = handler.handle_user_text(
    text="seu texto aqui",
    stream=True,              # Streaming do chat
    synth_partial=True,       # Síntese parcial
    on_response_callback=None # Callback com resposta final
)
```

#### ContinuousListener

```python
from services.continuous_listener import get_continuous_listener

listener = get_continuous_listener()

# Inicia escuta
listener.start(
    wake_word_enabled=True,
    on_transcript_callback=lambda text: print(text)
)

# Para escuta
listener.stop()

# Alterna wake-word
listener.toggle_wake_word(False)
```

## 🐛 Troubleshooting

### Problemas Comuns

#### ❌ Erro: "GROQ_API_KEY não encontrada"

```
ERRO: Defina sua variável GROQ_API_KEY
```

**Solução:**
1. Crie o arquivo `.env` na raiz do projeto
2. Adicione: `GROQ_API_KEY=gsk_sua_chave_aqui`
3. Reinicie a aplicação

#### ❌ Erro: "Erro ao gravar áudio"

```
Error: sounddevice.PortAudioError
```

**Solução:**
1. Verifique se o microfone está conectado
2. Teste o microfone em outras aplicações
3. No Windows: Verifique permissões de microfone nas configurações
4. No Linux: Instale `portaudio19-dev`: `sudo apt-get install portaudio19-dev`
5. No Mac: Conceda permissões de microfone nas Preferências do Sistema

#### ❌ Erro: "ModuleNotFoundError"

```
ModuleNotFoundError: No module named 'config'
```

**Solução:**
1. Certifique-se de estar no diretório correto: `cd victoria`
2. Execute sempre: `python main.py` (não `python src/main.py`)
3. Verifique se todos os `__init__.py` existem nos diretórios

#### ❌ TTS não funciona

```
[TTS] Erro: Loop não iniciado
```

**Solução:**
1. O loop asyncio é iniciado automaticamente no `main.py`
2. Se testando módulos isoladamente, chame `start_edge_loop()` primeiro
3. Verifique conexão com a internet (edge-tts precisa de internet)

#### ❌ Audio muito baixo/alto

**Solução:**
```python
from utils.audio_player import set_volume

set_volume(0.5)  # 50% do volume (0.0 a 1.0)
```

#### ❌ Wake-word não detecta

**Solução:**
1. Fale mais alto e claramente
2. Ajuste `VAD_ENERGY_THRESHOLD` em `config/settings.py`
3. Valores menores = mais sensível (ex: 200)
4. Valores maiores = menos sensível (ex: 500)
5. Teste diferentes palavras-chave

### Logs e Debug

Ative logs detalhados:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 🔧 Dependências

### Core

- **sounddevice** (0.4.6): Captura de áudio do microfone
- **numpy** (1.24.3): Processamento de arrays de áudio
- **scipy** (1.11.3): Manipulação de arquivos WAV
- **groq** (0.4.1): Cliente Python para API Groq
- **edge-tts** (6.1.9): Síntese de voz Microsoft
- **pygame** (2.5.2): Reprodução de áudio

### GUI

- **tkinter**: Interface gráfica (incluído no Python)

### Opcional

- **python-dotenv** (1.0.0): Carregamento de variáveis de ambiente

## 🚧 Roadmap

### Versão 1.1 (Em Planejamento)

- [ ] Suporte a múltiplos idiomas
- [ ] Histórico persistente de conversas
- [ ] Export de conversas (TXT, JSON)
- [ ] Configuração de atalhos de teclado
- [ ] Tema escuro/claro

### Versão 2.0 (Futuro)

- [ ] Integração com APIs externas (clima, notícias)
- [ ] Reconhecimento de comandos customizados
- [ ] Plugin system
- [ ] Web interface (Flask/FastAPI)
- [ ] Mobile app (Kivy)

## 🤝 Contribuindo

Contribuições são bem-vindas! Siga os passos:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### Diretrizes

- Siga PEP 8 para estilo de código
- Adicione docstrings nas funções
- Teste suas mudanças antes de submeter
- Atualize a documentação se necessário

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- **Groq** pela API rápida e gratuita de IA
- **Microsoft** pelo edge-tts de código aberto
- **OpenAI** pela inspiração do ChatGPT
- Comunidade Python open-source

## 📞 Contato & Suporte

- 🐛 **Issues**: [GitHub Issues](https://github.com/seu-usuario/victoria/issues)
- 💬 **Discussões**: [GitHub Discussions](https://github.com/seu-usuario/victoria/discussions)
- 📧 **Email**: seu-email@exemplo.com

## ⭐ Apoie o Projeto

Se o VictorIA foi útil para você, considere:

- ⭐ Dar uma estrela no GitHub
- 🐛 Reportar bugs
- 💡 Sugerir melhorias
- 🤝 Contribuir com código
- 📢 Compartilhar com amigos

---

<div align="center">

**Desenvolvido com ❤️ em Python**

[⬆ Voltar ao topo](#️-victoria---assistente-de-voz-inteligente)

</div>
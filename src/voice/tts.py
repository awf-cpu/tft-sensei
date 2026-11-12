"""TTS (texto -> fala) — camada de VOZ. STUB da Fase 2.

Plano: converter a resposta do coach em áudio para você OUVIR a orientação
sem tirar os olhos do jogo.

Opções para a Fase 2:
    - pyttsx3: offline, simples, voz robótica (bom p/ começar)
    - TTS de API (ex. ElevenLabs/OpenAI): voz natural, custo por uso
"""
from __future__ import annotations


def speak(text: str) -> None:
    """Fala o texto em voz alta. (Não implementado — Fase 2)"""
    raise NotImplementedError(
        "TTS chega na Fase 2. Veja os comentários em src/voice/tts.py."
    )

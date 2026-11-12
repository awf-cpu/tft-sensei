"""STT (fala -> texto) — camada de VOZ. STUB da Fase 2.

Plano: usar Whisper LOCAL (grátis, offline, baixa latência) para transcrever
o que o usuário fala ("vale a pena forçar essa comp?").

Para implementar na Fase 2:
    pip install openai-whisper sounddevice
    - captura ~alguns segundos do microfone com sounddevice
    - transcreve com whisper ("small" ou "base" já servem p/ PT-BR)
"""
from __future__ import annotations


def listen(seconds: int = 5) -> str:
    """Grava do microfone e devolve o texto transcrito. (Não implementado)"""
    raise NotImplementedError(
        "STT chega na Fase 2. Veja os comentários em src/voice/stt.py."
    )

"""Captura de tela — camada de PERCEPÇÃO (visão).

Seguro contra anti-cheat: apenas lê os pixels da tela (como um print),
sem injetar nada no processo do jogo nem ler memória.

Fase 1: captura a tela inteira (ou o monitor indicado) e salva um PNG.
Fase 3 (futuro): recortar só a janela do TFT e disparar por gatilhos.
"""
from __future__ import annotations

import io
from datetime import datetime
from pathlib import Path

import mss
from PIL import Image

CAPTURES_DIR = Path("captures")


def capture_screen(monitor: int = 1, save: bool = True) -> Image.Image:
    """Captura um monitor e devolve uma imagem PIL.

    Args:
        monitor: índice do monitor (1 = principal).
        save: se True, salva um PNG em captures/ para histórico.
    """
    with mss.mss() as sct:
        shot = sct.grab(sct.monitors[monitor])
        img = Image.frombytes("RGB", shot.size, shot.rgb)

    if save:
        CAPTURES_DIR.mkdir(exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        img.save(CAPTURES_DIR / f"capture_{ts}.png")

    return img


def image_to_png_bytes(img: Image.Image, max_width: int = 1280) -> bytes:
    """Serializa uma imagem PIL em PNG (para enviar ao LLM).

    Reduz a largura para no máx. `max_width` px: menos dados -> menos
    latência e custo, sem perder a legibilidade da tela do TFT.
    """
    if img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((max_width, int(img.height * ratio)))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def load_image(path: str) -> Image.Image:
    """Carrega uma imagem de um arquivo já existente."""
    return Image.open(path).convert("RGB")

"""TFT Coach — ponto de entrada (Fase 1).

Fluxo: captura/carrega um print -> CÉREBRO analisa -> imprime a orientação.

Exemplos:
    python -m src.main --image print.png
    python -m src.main --capture
    python -m src.main --capture --pergunta "forço reroll de custo 1?"
"""
from __future__ import annotations

import argparse
import sys

from .brain.analyzer import analyze
from .perception.capture import (
    capture_screen,
    image_to_png_bytes,
    load_image,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="TFT Coach — analisa um print do TFT e te orienta."
    )
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--image", help="caminho de um print já existente (.png/.jpg)")
    src.add_argument(
        "--capture", action="store_true", help="captura a tela agora e analisa"
    )
    parser.add_argument(
        "--monitor", type=int, default=1, help="índice do monitor (padrão: 1)"
    )
    parser.add_argument(
        "--pergunta", default=None, help="pergunta específica sobre a tela"
    )
    parser.add_argument(
        "--explica",
        action="store_true",
        help="modo aula detalhada (mais lento); padrão é resposta curta ao vivo",
    )
    args = parser.parse_args(argv)

    # 1. PERCEPÇÃO
    if args.capture:
        print("📸 Capturando a tela...", file=sys.stderr)
        img = capture_screen(monitor=args.monitor)
    else:
        img = load_image(args.image)

    png = image_to_png_bytes(img)

    # 2. CÉREBRO
    print("🧠 Analisando com a IA...", file=sys.stderr)
    try:
        resposta = analyze(
            png, pergunta=args.pergunta, mode="deep" if args.explica else "live"
        )
    except RuntimeError as e:
        print(f"\n❌ {e}", file=sys.stderr)
        return 1

    # 3. SAÍDA (Fase 2: voz.tts.speak(resposta))
    print("\n" + "=" * 60)
    print(resposta)
    print("=" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

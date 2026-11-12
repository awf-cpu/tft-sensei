"""Análise multimodal — camada de CÉREBRO.

Dois modos, pensados para um coach AO VIVO:

- "live"  -> resposta CURTA e RÁPIDA (1-2 frases): modelo veloz (Haiku),
             esforço baixo, poucos tokens. É o padrão durante a partida.
- "deep"  -> a aula detalhada do "professor" (3 blocos), só quando o
             usuário pede ("por quê?", "explica"). Usa modelo mais capaz.
"""
from __future__ import annotations

import base64

from ..config import config
from .knowledge import load_meta, meta_as_context

# AO VIVO: curto, direto, falável em poucos segundos.
LIVE_PROMPT = """Você é um coach de Teamfight Tactics (TFT) falando AO VIVO no ouvido
do jogador durante a partida. Olhe o print e diga a jogada AGORA.

REGRAS DE OURO:
- Responda em NO MÁXIMO 2 frases curtas. Nada de listas, títulos ou blocos.
- Vá direto à ação (comprar, rolar, subir nível, segurar ouro, posicionar) + um
  motivo de 3-4 palavras.
- Se faltar info crítica na tela, diga em meia frase o que não dá pra ver.
- Tom de quem fala rápido, como um treinador no banco. Idioma: {lang}."""

# EXPLICA (sob demanda): a aula completa.
DEEP_PROMPT = """Você é um treinador especialista em TFT atuando como PROFESSOR.
Analise o print e ensine o jogador, explicando o PORQUÊ de cada escolha.
Estruture em 3 partes curtas:
1. 📋 Leitura do cenário
2. ✅ Recomendação
3. 💡 Por quê (a lição)
Idioma: {lang}."""


def analyze(image_png: bytes, pergunta: str | None = None, mode: str = "live") -> str:
    """Analisa o print e devolve a orientação do coach.

    mode="live" (padrão): curto e rápido. mode="deep": aula detalhada.
    """
    config.validate()
    is_live = mode != "deep"

    system = (LIVE_PROMPT if is_live else DEEP_PROMPT).format(lang=config.lang)
    model = config.live_model if is_live else config.llm_model
    max_tokens = 120 if is_live else 700

    # RAG: no modo live mandamos pouco contexto (latência); no deep, mais.
    meta_ctx = meta_as_context(load_meta(), max_comps=3 if is_live else 5)
    user_text = f"Print da minha partida de TFT.\n\nMeta de referência:\n{meta_ctx}\n"
    if pergunta:
        user_text += f"\nPergunta: {pergunta}\n"

    b64 = base64.b64encode(image_png).decode("ascii")

    if config.llm_provider == "openai":
        return _analyze_openai(system, user_text, b64, model, max_tokens)
    return _analyze_anthropic(system, user_text, b64, model, max_tokens, is_live)


def _analyze_openai(
    system: str, user_text: str, b64: str, model: str, max_tokens: int
) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=config.openai_api_key)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_text},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{b64}"},
                    },
                ],
            },
        ],
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content or "(sem resposta)"


def _analyze_anthropic(
    system: str, user_text: str, b64: str, model: str, max_tokens: int, is_live: bool
) -> str:
    import anthropic

    # Sem chave -> usa o login da CLI (`ant auth login`).
    client = (
        anthropic.Anthropic(api_key=config.anthropic_api_key)
        if config.anthropic_api_key
        else anthropic.Anthropic()
    )

    kwargs = dict(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_text},
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": b64,
                        },
                    },
                ],
            }
        ],
    )
    # Ao vivo: esforço baixo = menos "pensamento" = resposta mais rápida.
    if is_live:
        kwargs["output_config"] = {"effort": "low"}

    resp = client.messages.create(**kwargs)
    return "".join(b.text for b in resp.content if b.type == "text") or "(sem resposta)"

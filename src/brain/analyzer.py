"""Análise multimodal — camada de CÉREBRO.

Recebe a imagem do tabuleiro + a base de meta + a pergunta do usuário,
e devolve a orientação do "professor". Suporta OpenAI e Anthropic.
"""
from __future__ import annotations

import base64

from ..config import config
from .knowledge import load_meta, meta_as_context

# Persona do coach: é aqui que mora o "professor".
# Conhecimento ESTÁVEL (como raciocinar/ensinar) vai no prompt;
# conhecimento VOLÁTIL (meta do patch) vem do RAG (knowledge.py).
SYSTEM_PROMPT = """Você é um treinador (coach) especialista em Teamfight Tactics (TFT),
atuando como PROFESSOR ao vivo durante a partida do usuário.

Seu jeito de ensinar:
- Analise o print do tabuleiro: unidades no campo e no bench, itens, nível,
  ouro, estágio/rodada, vida e augments visíveis.
- Dê uma recomendação CLARA e priorizada (o que fazer AGORA).
- Explique sempre o PORQUÊ, de forma didática, para o usuário aprender — não
  apenas o comando. Ex.: "rola aqui porque você está em 50 de ouro e perdendo
  streak; estabilize antes de cair demais de vida".
- Seja objetivo: a pessoa está no meio de uma partida com tempo curto.
- Se a imagem estiver ambígua ou faltar informação, diga o que não dá pra ver
  e dê a melhor recomendação possível mesmo assim.

Responda SEMPRE no idioma: {lang}.
Estruture a resposta em 3 partes curtas:
1. 📋 Leitura do cenário (o que você vê)
2. ✅ Recomendação (o que fazer agora)
3. 💡 Por quê (a lição)
"""


def _build_user_text(pergunta: str | None) -> str:
    meta_ctx = meta_as_context(load_meta())
    base = (
        "Aqui está um print da minha partida de TFT. "
        "Analise e me oriente.\n\n"
        f"=== Base de meta atual (referência) ===\n{meta_ctx}\n"
    )
    if pergunta:
        base += f"\n=== Minha pergunta específica ===\n{pergunta}\n"
    return base


def analyze(image_png: bytes, pergunta: str | None = None) -> str:
    """Analisa o print e devolve a orientação do coach (texto)."""
    config.validate()
    system = SYSTEM_PROMPT.format(lang=config.lang)
    user_text = _build_user_text(pergunta)
    b64 = base64.b64encode(image_png).decode("ascii")

    if config.llm_provider == "openai":
        return _analyze_openai(system, user_text, b64)
    return _analyze_anthropic(system, user_text, b64)


def _analyze_openai(system: str, user_text: str, b64: str) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=config.openai_api_key)
    resp = client.chat.completions.create(
        model=config.llm_model,
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
        max_tokens=700,
    )
    return resp.choices[0].message.content or "(sem resposta)"


def _analyze_anthropic(system: str, user_text: str, b64: str) -> str:
    import anthropic

    client = anthropic.Anthropic(api_key=config.anthropic_api_key)
    resp = client.messages.create(
        model=config.llm_model,
        max_tokens=700,
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
    # Concatena blocos de texto da resposta
    return "".join(b.text for b in resp.content if b.type == "text") or "(sem resposta)"

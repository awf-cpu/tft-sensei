"""Base de conhecimento (RAG) — camada de CÉREBRO.

Aqui mora o conhecimento que MUDA a cada patch: comps, prioridade de itens,
augments fortes do set atual. A ideia é você atualizar só este arquivo/base
a cada patch — sem retreinar nenhum modelo.

Fase 1: carrega um JSON simples e injeta no prompt.
Fase 4 (futuro): virar um índice vetorial (embeddings) que busca só as
comps relevantes ao estado atual, economizando tokens.
"""
from __future__ import annotations

import json
from pathlib import Path

# Resolved from the file location so it works from any working directory.
META_DIR = Path(__file__).resolve().parents[2] / "data" / "meta"


def load_meta() -> dict:
    """Carrega a base de meta. Usa comps.json se existir, senão o exemplo."""
    path = META_DIR / "comps.json"
    if not path.exists():
        path = META_DIR / "comps.example.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def meta_as_context(meta: dict, max_comps: int = 5) -> str:
    """Formata a base de meta como texto para injetar no prompt.

    Fase 4: aqui entraria a busca vetorial para mandar só o que importa.
    Por ora mandamos as top comps (limitado por max_comps).
    """
    if not meta:
        return "(Sem base de meta carregada. Aconselhe pelo conhecimento geral de TFT.)"

    patch = meta.get("patch", "desconhecido")
    comps = meta.get("comps", [])[:max_comps]

    linhas = [f"Patch/Set de referência: {patch}", "", "Comps de referência:"]
    for c in comps:
        nome = c.get("nome", "?")
        nivel = c.get("nivel", "?")
        unidades = ", ".join(c.get("unidades_chave", []))
        itens = ", ".join(c.get("itens_prioritarios", []))
        linhas.append(f"- {nome} (tier {nivel}) — chave: {unidades}; itens: {itens}")

    return "\n".join(linhas)

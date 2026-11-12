"""Carrega configuração a partir do arquivo .env."""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    llm_provider: str = os.getenv("LLM_PROVIDER", "anthropic").lower()
    # Modo AO VIVO: modelo rápido e barato (prioriza latência).
    live_model: str = os.getenv("LLM_LIVE_MODEL", "claude-haiku-5-5")
    # Modo EXPLICA (sob demanda): modelo mais capaz p/ a aula detalhada.
    llm_model: str = os.getenv("LLM_MODEL", "claude-sonnet-5-5")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    riot_api_key: str = os.getenv("RIOT_API_KEY", "")
    riot_region: str = os.getenv("RIOT_REGION", "americas")
    lang: str = os.getenv("COACH_LANG", "pt-BR")

    def validate(self) -> None:
        """Garante que há credencial para o provedor escolhido."""
        if self.llm_provider == "openai" and not self.openai_api_key:
            raise RuntimeError(
                "OPENAI_API_KEY não definida. Edite o arquivo .env "
                "(copie de .env.example)."
            )
        # Anthropic: a chave é OPCIONAL. Se ANTHROPIC_API_KEY estiver vazia,
        # o SDK usa o login da CLI (`ant auth login`) automaticamente — é o
        # caminho "Seu próprio computador", sem chave pra gerenciar.
        if self.llm_provider not in ("openai", "anthropic"):
            raise RuntimeError(
                f"LLM_PROVIDER inválido: {self.llm_provider!r}. "
                "Use 'openai' ou 'anthropic'."
            )


config = Config()

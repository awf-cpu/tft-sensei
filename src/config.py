"""Carrega configuração a partir do arquivo .env."""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai").lower()
    llm_model: str = os.getenv("LLM_MODEL", "gpt-4o")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    riot_api_key: str = os.getenv("RIOT_API_KEY", "")
    riot_region: str = os.getenv("RIOT_REGION", "americas")
    lang: str = os.getenv("COACH_LANG", "pt-BR")

    def validate(self) -> None:
        """Garante que a chave do provedor escolhido está presente."""
        if self.llm_provider == "openai" and not self.openai_api_key:
            raise RuntimeError(
                "OPENAI_API_KEY não definida. Edite o arquivo .env "
                "(copie de .env.example)."
            )
        if self.llm_provider == "anthropic" and not self.anthropic_api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY não definida. Edite o arquivo .env "
                "(copie de .env.example)."
            )
        if self.llm_provider not in ("openai", "anthropic"):
            raise RuntimeError(
                f"LLM_PROVIDER inválido: {self.llm_provider!r}. "
                "Use 'openai' ou 'anthropic'."
            )


config = Config()

import json
import os
from pathlib import Path

os.environ.setdefault("LLM_PROVIDER", "anthropic")

from src.brain import analyzer, knowledge  # noqa: E402


def test_meta_loads_from_any_working_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    meta = knowledge.load_meta()
    assert meta.get("comps"), "example meta should load regardless of cwd"


def test_meta_context_limits_comps():
    meta = {"patch": "X", "comps": [{"nome": f"c{i}", "nivel": "S"} for i in range(10)]}
    text = knowledge.meta_as_context(meta, max_comps=3)
    assert text.count("- c") == 3 and "Patch/Set de referência: X" in text


def test_empty_meta_falls_back_to_general_knowledge():
    assert "Sem base de meta" in knowledge.meta_as_context({})


def test_live_mode_uses_fast_model_and_short_budget(monkeypatch):
    seen = {}

    def fake(system, user_text, b64, model, max_tokens, is_live):
        seen.update(model=model, max_tokens=max_tokens, is_live=is_live, b64=b64)
        return "ok"

    monkeypatch.setattr(analyzer, "_analyze_anthropic", fake)
    assert analyzer.analyze(b"\x89PNG", "e agora?", mode="live") == "ok"
    assert seen["is_live"] and seen["max_tokens"] == 120
    deep = {}
    monkeypatch.setattr(analyzer, "_analyze_anthropic", lambda *a: deep.update(t=a[4]) or "ok")
    analyzer.analyze(b"\x89PNG", mode="deep")
    assert deep["t"] == 700


def test_invalid_provider_rejected():
    from src.config import Config

    try:
        Config(llm_provider="nope").validate()
    except RuntimeError as e:
        assert "inválido" in str(e)
    else:
        raise AssertionError("expected RuntimeError")

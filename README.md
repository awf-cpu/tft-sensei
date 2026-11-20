# tft-sensei

![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)
![Status: MVP](https://img.shields.io/badge/status-MVP-orange)

An **AI coach for Teamfight Tactics (TFT)** that "looks" at your game screen with a multimodal LLM and explains what to do next (rolls, items, augments, positioning) and *why*. It has a fast **live mode** (one or two short sentences) and a detailed **teaching mode**. Voice interaction (speech-to-text and text-to-speech) is designed and stubbed, and is on the roadmap.

> Portfolio project for multimodal LLM pipelines: screen perception, prompt design for latency-sensitive answers, and a patch-proof knowledge layer. Not affiliated with Riot Games.

## The business problem it explores

Domain knowledge that changes often (here, the game meta every ~2 weeks) ages badly when baked into model weights. The design choice that matters: **volatile knowledge lives in an updatable knowledge base (RAG-style), not in the model**, so nothing goes stale and nothing needs retraining. The same reasoning applies to price lists, regulations, internal policies and product catalogs.

## Try it

```bash
pip install -r requirements.txt && cp .env.example .env   # add your LLM API key
python -m src.main --image path/to/screenshot.png          # analyze a screenshot
python -m src.main --capture --pergunta "should I force a cost-1 reroll?"   # capture the screen and ask
python -m src.main --capture --explica                     # teaching mode (slower, detailed)
```

The LLM provider is configurable (`LLM_PROVIDER=anthropic|openai`, `LLM_MODEL`) in `.env`.

## Architecture

```
PERCEPTION  ->  reads the game state
  - screen capture (pixels only) + multimodal LLM: board, shop, augments, bench
  - optional live-data source for exact HP, gold and stage

BRAIN       ->  decides and teaches
  - vision LLM with a coach persona (live mode: short and fast, deep mode: 3-part lesson)
  - updatable meta knowledge base (comps / items / augments for the current set)

VOICE       ->  planned: local Whisper STT + TTS (stubs in src/voice/)

MEMORY      ->  planned: log interactions into your own dataset, distill to a local model later
```

Why not train a local model first? The meta changes too fast for weights, retrieval is cheaper and always current, and the sensible path is **cloud model plus knowledge base now, collect your own usage data, distill to local later**.

## Roadmap

- [x] Phase 1: screenshot to analysis to text answer (this MVP), including live and teaching modes
- [ ] Phase 2: voice (STT with Whisper, TTS)
- [ ] Phase 3: real-time triggers and on-screen overlay
- [ ] Phase 4: robust per-patch meta knowledge base

## Compliance

Screen capture only (reads pixels) and official APIs. It never reads game memory, which would violate the game's terms. Respect API rate limits and never commit API keys.

## How this becomes a solution for your company

The pattern here (perceive a screen or document with a multimodal model, answer with a persona, keep changing knowledge outside the model) is the same one used for assistants that read forms, dashboards, scanned documents or on-screen workflows and guide a user step by step. If you need something like that, see **Work with me** below.

## Work with me

I am André Feix, founder of **Pindorama Tecnologia** (Florianópolis, Brazil). We build custom AI systems for companies and law firms: WhatsApp agents with compliance guardrails (LGPD, bar-association rules), RAG over documents, document and deadline automation, LLM routing with cost control, and local AI with data kept in Brazil.

- LinkedIn: https://www.linkedin.com/in/andrefeix
- Email: andrefeix777@gmail.com
- More: https://github.com/awf-cpu

## Em português (resumo)

Assistente de IA para Teamfight Tactics que analisa o print da tela com um modelo multimodal e orienta a jogada explicando o porquê. Modo ao vivo (resposta curta) e modo aula (`--explica`). Voz (Whisper + TTS) está planejada, ainda como stub. O conhecimento que muda a cada patch fica numa base atualizável, não nos pesos do modelo. Para rodar: `pip install -r requirements.txt`, copie `.env.example` para `.env` e use `python -m src.main --image print.png`.

## License

MIT © 2026 awf-cpu

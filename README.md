# TFT Coach 🧠🎙️

Um assistente de IA, por voz e em tempo real, que atua como **professor ao vivo** de
Teamfight Tactics (TFT): ele "enxerga" o seu tabuleiro, analisa o cenário e te orienta
nas escolhas — rolls, itens, augments, posicionamento — explicando o *porquê* de cada
recomendação.

> Estilo Blitz/Mobalytics, mas com coaching por IA e interação por voz.

---

## Filosofia de arquitetura

O sistema é dividido em 4 camadas independentes. A decisão mais importante do projeto:
**conhecimento que muda a cada patch NÃO fica treinado no modelo — fica numa base
atualizável (RAG).** Assim nada fica desatualizado e você não precisa retreinar nada.

```
PERCEPÇÃO  →  capta o estado do jogo
  ├── Visão (screenshot + modelo multimodal)  → lê tabuleiro, loja, augments, bench
  └── Live/Overwolf (opcional)                → vida, ouro e estágio exatos

CÉREBRO    →  decide e ensina
  ├── LLM com visão (nuvem no MVP)            → raciocínio + persona de "professor"
  └── RAG (base de meta atualizável)          → comps/itens/augments do set atual

VOZ        →  conversa em tempo real
  ├── STT (Whisper, local)                    → você fala a pergunta
  └── TTS                                      → ele responde falando

MEMÓRIA    →  grava interações → vira dataset próprio → destilação local no futuro
```

### Por que não treinar um modelo local desde o início?
- O meta do TFT muda a cada ~2 semanas; conhecimento nos pesos envelhece quase na hora.
- RAG é mais barato, sempre atual e não exige GPU de treino.
- O caminho certo é: **nuvem + RAG agora → coletar seus dados usando → destilar p/ local depois.**

---

## Roadmap por fases

- [x] **Fase 1 — Cérebro de texto:** screenshot → IA analisa → responde em texto *(este MVP)*
- [ ] **Fase 2 — Voz:** fala a pergunta (STT) + ouve a resposta (TTS)
- [ ] **Fase 3 — Tempo real:** captura automática nos gatilhos + overlay na tela
- [ ] **Fase 4 — RAG de meta robusto:** base de comps/itens atualizada por patch

---

## Como rodar a Fase 1

Pré-requisitos: Python 3.10+ e uma API key de um modelo **com visão** (multimodal).

```bash
cd tft-coach
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # edite e coloque sua API key
```

Analisar um print que você já tirou:

```bash
python -m src.main --image caminho/para/print.png
```

Capturar a tela atual e analisar (precisa estar com o TFT visível):

```bash
python -m src.main --capture
```

Fazer uma pergunta específica sobre a tela:

```bash
python -m src.main --capture --pergunta "vale a pena forçar reroll de custo 1?"
```

---

## Estrutura

```
src/
  main.py              # ponto de entrada: orquestra captura → análise → resposta
  config.py            # carrega .env e configurações
  perception/
    capture.py         # captura de tela (seguro: só lê pixels, não toca no jogo)
  brain/
    analyzer.py        # envia imagem + contexto ao LLM multimodal
    knowledge.py       # RAG: carrega a base de meta (comps/itens) do set atual
  voice/
    stt.py             # STUB Fase 2 — reconhecimento de fala (Whisper)
    tts.py             # STUB Fase 2 — síntese de voz
data/
  meta/
    comps.example.json # exemplo da base de conhecimento (você atualiza por patch)
```

---

## ⚠️ Compliance (importante)

- **Só captura de tela** (lê pixels) e APIs oficiais. **Nunca** leitura de memória do jogo
  — isso viola os termos da Riot e dá ban.
- A captura de tela é *anti-cheat safe* porque não injeta nada no processo do jogo.
- Para a Riot API oficial, respeite os rate limits e nunca versione sua API key.

Este projeto não é afiliado à Riot Games.

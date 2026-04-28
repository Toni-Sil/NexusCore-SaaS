# 🧠 NexusCore AI Engine

Microserviço Python (FastAPI) responsável por toda a inteligência adaptativa do NexusCore SaaS.

## Setup

```bash
cd ai-engine
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

## Variáveis de ambiente

```env
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
NEXUSCORE_BACKEND_URL=http://localhost:3000
REDIS_URL=redis://localhost:6379
SECRET_KEY=...
```

## Estrutura

```
ai-engine/
├── main.py                  # Entrypoint FastAPI
├── requirements.txt
├── agents/
│   ├── niche_analyzer.py    # Analisa o nicho e gera NicheProfile
│   ├── theme_generator.py   # Gera ThemeConfig baseado no nicho
│   ├── workflow_generator.py # Gera steps de workflow
│   ├── field_generator.py   # Gera campos dinâmicos
│   └── orchestrator.py      # Orquestrador central (full-setup)
├── templates/
│   ├── pet_shop.json        # Template estático de fallback
│   ├── oficina.json
│   ├── barbearia.json
│   ├── fabrica.json
│   ├── varejo.json
│   └── clinica.json
├── prompts/
│   ├── niche_analysis.txt   # Prompt de análise de nicho
│   ├── theme_generation.txt # Prompt de geração de tema
│   └── workflow_gen.txt     # Prompt de geração de workflow
└── utils/
    ├── cache.py             # Redis cache
    ├── llm.py               # Abstração do LLM (OpenAI / Gemini)
    └── validator.py         # Valida JSON gerado pela IA
```

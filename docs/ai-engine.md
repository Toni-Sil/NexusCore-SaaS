# 🧠 NexusCore AI Engine — Motor de IA Adaptativa

## Visão Geral

O **NexusCore AI Engine** é o cérebro do sistema. Ele é um serviço Python independente (microserviço) que conversa com o backend principal via API interna e é responsável por fazer o sistema "se ajustar" automaticamente ao nicho de cada tenant.

Ele **não** é um chatbot. É um agente de configuração que age silenciosamente no backend, tomando decisões sobre como o sistema deve se apresentar e se comportar para um determinado nicho.

---

## 🎯 O que o AI Engine faz

### 1. Análise de Nicho (Niche Analyzer)
Recebe o nicho informado no onboarding (ou inferido por descrição livre) e produz um `NicheProfile` completo:

```json
{
  "niche": "pet_shop",
  "display_name": "Pet Shop",
  "entity_labels": {
    "service_order": "Atendimento",
    "customer": "Tutor",
    "product": "Produto Pet",
    "schedule": "Agendamento",
    "inventory": "Estoque"
  },
  "active_modules": ["scheduling", "service_orders", "inventory", "financial", "crm", "reports"],
  "workflow_template": "pet_shop_default",
  "theme_profile": "warm_nature",
  "dashboard_metrics": ["atendimentos_hoje", "pets_cadastrados", "receita_mensal", "agendamentos_proximos"],
  "tone": "friendly_casual"
}
```

### 2. Geração de Tema Visual (Theme Generator)
Com base no nicho e no `theme_profile`, o AI Engine gera um `ThemeConfig` completo:

```json
{
  "primary_color": "#2E7D32",
  "secondary_color": "#81C784",
  "accent_color": "#FF8F00",
  "font_display": "Cabinet Grotesk",
  "font_body": "Satoshi",
  "border_radius": "lg",
  "icon_style": "rounded",
  "logo_concept": "pata + símbolo clean",
  "illustration_style": "flat_friendly"
}
```

### 3. Geração de Fluxos (Workflow Generator)
Produz os steps de cada processo do nicho:

```json
{
  "workflow": "atendimento_pet",
  "steps": [
    { "id": 1, "label": "Check-in do pet", "color": "blue" },
    { "id": 2, "label": "Em banho e tosa", "color": "yellow" },
    { "id": 3, "label": "Aguardando retirada", "color": "orange" },
    { "id": 4, "label": "Finalizado", "color": "green" }
  ]
}
```

### 4. Geração de Campos Dinâmicos (Field Generator)
Gera os campos extras de formulário por entidade, específicos do nicho:

```json
{
  "entity": "customer",
  "extra_fields": [
    { "name": "pet_name", "label": "Nome do pet", "type": "text", "required": true },
    { "name": "pet_species", "label": "Espécie", "type": "select", "options": ["Cão", "Gato", "Pássaro", "Outro"] },
    { "name": "pet_breed", "label": "Raça", "type": "text" },
    { "name": "veterinarian", "label": "Veterinário responsável", "type": "text" }
  ]
}
```

### 5. Análise Contínua (Continuous Adapter)
O AI Engine monitora o uso e pode sugerir ajustes:
- "Seus clientes mais usam agendamento — destacar no dashboard?"
- "Você tem X produtos sem movimentação — ativar alerta de estoque parado?"
- "Seu fluxo de OS tem 3 etapas não utilizadas — simplificar?"

---

## 🏗️ Arquitetura do AI Engine

```
┌─────────────────────────────────────────────────────┐
│                  NexusCore AI Engine                 │
│                  (Python FastAPI)                    │
│                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐  │
│  │ Niche        │  │ Theme        │  │ Workflow  │  │
│  │ Analyzer     │  │ Generator    │  │ Generator │  │
│  └──────┬───────┘  └──────┬───────┘  └─────┬─────┘  │
│         │                │                 │        │
│  ┌──────▼─────────────────▼─────────────────▼─────┐  │
│  │              Orchestrator Agent                │  │
│  │   (LangChain / LlamaIndex / Custom Agent)      │  │
│  └──────────────────────┬─────────────────────────┘  │
│                         │                            │
│  ┌──────────────────────▼─────────────────────────┐  │
│  │              LLM Layer                         │  │
│  │   OpenAI GPT-4o / Gemini Pro / NVIDIA NIM      │  │
│  └──────────────────────┬─────────────────────────┘  │
│                         │                            │
│  ┌──────────────────────▼─────────────────────────┐  │
│  │           Niche Knowledge Base                  │  │
│  │   (JSON templates por nicho + RAG opcional)    │  │
│  └────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
         │
         ▼  (API interna REST/gRPC)
┌────────────────┐
│ Backend NestJS │  ← aplica as configs geradas no tenant
└────────────────┘
```

---

## 🔄 Fluxo de Onboarding com IA

```
[Usuário] → Preenche onboarding
    ↓
"Qual o seu negócio?"  →  "Sou dono de uma barbearia"
    ↓
[AI Engine: Niche Analyzer]
    → Identifica nicho: "barbearia"
    → Gera NicheProfile completo
    ↓
[AI Engine: Theme Generator]
    → Gera ThemeConfig (escuro, masculino, tipografia forte)
    ↓
[AI Engine: Workflow Generator]
    → Gera steps: Agendado → Em atendimento → Concluído → Pago
    ↓
[AI Engine: Field Generator]
    → Campos extras: serviço escolhido, barbeiro, observações
    ↓
[Backend NestJS]
    → Salva TenantConfig no banco
    → Ativa módulos corretos
    ↓
[Frontend Next.js]
    → Carrega CSS variables do tema
    → Renderiza sistema com a cara da barbearia
```

---

## 📡 Endpoints do AI Engine (FastAPI)

| Método | Rota | Descrição |
|---|---|---|
| POST | `/ai/analyze-niche` | Recebe descrição e retorna NicheProfile |
| POST | `/ai/generate-theme` | Recebe NicheProfile e retorna ThemeConfig |
| POST | `/ai/generate-workflow` | Gera steps de workflow por processo |
| POST | `/ai/generate-fields` | Gera campos dinâmicos por entidade |
| POST | `/ai/generate-dashboard` | Gera layout e métricas do dashboard |
| POST | `/ai/suggest-improvements` | Analisa uso e sugere melhorias |
| POST | `/ai/full-setup` | Endpoint unificado: faz tudo de uma vez |

---

## 🗃️ Tabelas de suporte no banco

```sql
-- Profile de nicho gerado pela IA
CREATE TABLE tenant_niche_profiles (
  id UUID PRIMARY KEY,
  tenant_id UUID REFERENCES tenants(id),
  niche_key VARCHAR(100),
  niche_label VARCHAR(200),
  profile_json JSONB,        -- NicheProfile completo
  generated_by VARCHAR(50),  -- 'ai_engine' | 'manual'
  created_at TIMESTAMP DEFAULT NOW()
);

-- Tema gerado pela IA
CREATE TABLE tenant_themes (
  id UUID PRIMARY KEY,
  tenant_id UUID REFERENCES tenants(id),
  theme_json JSONB,          -- ThemeConfig completo
  is_active BOOLEAN DEFAULT TRUE,
  generated_by VARCHAR(50),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Workflows gerados pela IA
CREATE TABLE workflow_templates (
  id UUID PRIMARY KEY,
  tenant_id UUID REFERENCES tenants(id),
  process_name VARCHAR(100),
  steps_json JSONB,
  generated_by VARCHAR(50),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Campos dinâmicos gerados pela IA
CREATE TABLE dynamic_fields (
  id UUID PRIMARY KEY,
  tenant_id UUID REFERENCES tenants(id),
  entity VARCHAR(100),
  fields_json JSONB,
  generated_by VARCHAR(50),
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔑 Segurança e Limites

- O AI Engine só é chamado por serviços internos (não exposto publicamente)
- Rate limiting por tenant no onboarding (max 3 gerações/hora)
- Cache Redis de 24h para perfis de nicho semelhantes
- Fallback para templates estáticos se a IA falhar
- Logs de tudo que a IA gera (auditoria)

# 🏗️ Arquitetura Geral — NexusCore SaaS

## Visão de Alto Nível

```
┌──────────────────────────────────────────────────────────────────┐
│                        NexusCore SaaS                            │
│                                                                  │
│  ┌─────────────────┐   ┌────────────────────────────────────┐   │
│  │  Frontend        │   │         Backend Principal           │   │
│  │  Next.js 15     │◄──►│         NestJS (TypeScript)         │   │
│  │  + CSS Vars     │   │         REST API + WebSocket        │   │
│  │  (tema dinâmico)│   └──────────────┬─────────────────────┘   │
│  └─────────────────┘                  │                          │
│                         ┌─────────────▼──────────────┐          │
│                         │     NexusCore AI Engine      │         │
│                         │     Python FastAPI           │         │
│                         │     LLM + Agentes            │         │
│                         └─────────────┬────────────────┘         │
│                                       │                          │
│              ┌────────────────────────┼───────────────┐          │
│              ▼                        ▼               ▼          │
│         PostgreSQL               Redis Cache       Storage        │
│         (multi-tenant)           (sessões, IA)    (arquivos)     │
└──────────────────────────────────────────────────────────────────┘
```

## Princípio de Multi-Tenant

Todo dado no banco carrega `tenant_id`. O backend injeta automaticamente o filtro de tenant em cada query via middleware, garantindo isolamento total.

## Camadas do Sistema

| Camada | Responsabilidade |
|---|---|
| **Core** | Auth, tenants, usuários, permissões, billing, auditoria |
| **Operacional** | Clientes, produtos, estoque, ordens, financeiro, agenda |
| **Adaptativa** | Temas, labels, módulos, workflows, campos dinâmicos |
| **IA Engine** | Geração de configs, análise de nicho, sugestões |
| **Integrações** | WhatsApp, e-mail, pagamentos, NFe, calendário |

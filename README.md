# 🚀 NexusCore SaaS

**Sistema SaaS Superadaptativo Multi-Nicho com IA no Backend**

Plataforma que se transforma visualmente e operacionalmente para qualquer nicho de pequena e média empresa, guiada por um motor de inteligência artificial que analisa o nicho e reconfigura o sistema automaticamente.

> Baseado em: [sistema-de-ordem-de-servico](https://github.com/Toni-Sil/sistema-de-ordem-de-servi-o) + [systema-de-gerenciamento-S.F.C.P.C](https://github.com/Toni-Sil/systema-de-gerenciamento-S.F.C.P.C)

---

## 🧠 Conceito Central

Um SaaS com uma **IA adaptativa no backend** — o **NexusCore AI Engine** — que ao receber o nicho (via onboarding ou por inferência), gera automaticamente:

- A identidade visual do sistema (paleta, tipografia, ícones, tom)
- Os módulos ativos e desativados
- Os fluxos de trabalho específicos
- A nomenclatura de entidades (OS, comanda, pedido, atendimento)
- Os campos e formulários dinâmicos
- As métricas do dashboard

---

## 📂 Estrutura do Projeto

Veja a documentação completa em `/docs/`:

- [`/docs/architecture.md`](./docs/architecture.md) — Arquitetura geral do sistema
- [`/docs/ai-engine.md`](./docs/ai-engine.md) — Motor de IA Adaptativa
- [`/docs/multi-tenant.md`](./docs/multi-tenant.md) — Sistema Multi-Tenant
- [`/docs/theme-engine.md`](./docs/theme-engine.md) — Engine de Temas
- [`/docs/modules.md`](./docs/modules.md) — Módulos do sistema
- [`/docs/roadmap.md`](./docs/roadmap.md) — Roadmap de desenvolvimento
- [`/docs/database-schema.md`](./docs/database-schema.md) — Schema do banco de dados

---

## ⚡ Stack

| Camada | Tecnologia |
|---|---|
| Frontend | Next.js 15 + TypeScript + Tailwind CSS |
| Backend API | NestJS + TypeScript |
| AI Engine | Python (FastAPI) + LLM (OpenAI/Gemini) |
| Banco de dados | PostgreSQL + Prisma ORM |
| Cache | Redis |
| Containers | Docker + Dokploy |
| Auth | JWT + RBAC por tenant |

---

## 🎯 Nichos Alvo (MVP)

- 🐾 Pet Shop
- 🔧 Assistência Técnica / Oficina
- 🛋️ Produção / Fábrica (ex: sofá-camas)
- 🏪 Varejo / Loja
- 💈 Barbearia / Salão
- 🏥 Clínica / Consultório pequeno

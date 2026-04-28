# 📦 Módulos do Sistema

## Módulos do Core (sempre ativos)

- `auth` — Autenticação e sessões
- `tenants` — Gestão de tenants
- `users` — Usuários e permissões RBAC
- `billing` — Planos e assinaturas
- `audit` — Logs e auditoria
- `notifications` — Notificações internas

## Módulos Operacionais (ativados por nicho/plano)

| Módulo | Descrição | Nichos principais |
|---|---|---|
| `crm` | Cadastro de clientes | Todos |
| `service_orders` | Ordens de serviço / OS | Oficina, assistência técnica, pet shop |
| `scheduling` | Agendamento | Pet shop, salão, clínica, barbearia |
| `inventory` | Estoque e produtos | Todos |
| `financial` | Contas, caixa, DRE | Todos |
| `production` | Ordens de produção | Fábrica, produção |
| `pos` | Ponto de venda | Varejo, loja |
| `delivery` | Entregas e rotas | Varejo, produção |
| `reports` | Relatórios e BI | Todos |
| `integrations` | WhatsApp, NF-e, etc. | Todos |

## Ativação por Nicho (gerada pela IA)

```json
{
  "pet_shop":       ["crm", "scheduling", "service_orders", "inventory", "financial", "reports"],
  "oficina":        ["crm", "service_orders", "inventory", "financial", "reports"],
  "barbearia":      ["crm", "scheduling", "financial", "reports"],
  "fabrica":        ["crm", "production", "inventory", "financial", "reports"],
  "varejo":         ["crm", "pos", "inventory", "financial", "delivery", "reports"],
  "clinica":        ["crm", "scheduling", "financial", "reports"]
}
```

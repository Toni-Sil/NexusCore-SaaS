# 🗃️ Schema do Banco de Dados

## Tabelas Core

```sql
-- Tenants (empresas)
CREATE TABLE tenants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug VARCHAR(100) UNIQUE NOT NULL,
  name VARCHAR(200) NOT NULL,
  niche_key VARCHAR(100),
  plan VARCHAR(50) DEFAULT 'starter',
  status VARCHAR(50) DEFAULT 'active',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Usuários
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255),
  role VARCHAR(50) DEFAULT 'user', -- owner | admin | user | viewer
  created_at TIMESTAMP DEFAULT NOW()
);

-- Configuração do Tenant (gerada pela IA)
CREATE TABLE tenant_configs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID UNIQUE REFERENCES tenants(id),
  niche_profile JSONB,     -- NicheProfile gerado pela IA
  theme JSONB,             -- ThemeConfig gerado pela IA
  active_modules JSONB,    -- ["crm", "inventory", ...]
  entity_labels JSONB,     -- { "service_order": "Atendimento", ... }
  generated_by VARCHAR(50) DEFAULT 'ai_engine',
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Módulos disponíveis
CREATE TABLE modules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  key VARCHAR(100) UNIQUE NOT NULL,
  display_name VARCHAR(200),
  description TEXT,
  min_plan VARCHAR(50) DEFAULT 'starter'
);
```

## Tabelas Operacionais (todas com tenant_id)

```sql
-- Clientes / CRM
CREATE TABLE customers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  name VARCHAR(200) NOT NULL,
  phone VARCHAR(20),
  email VARCHAR(255),
  extra_data JSONB,  -- campos dinâmicos gerados pela IA
  created_at TIMESTAMP DEFAULT NOW()
);

-- Produtos / Estoque
CREATE TABLE products (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  name VARCHAR(200) NOT NULL,
  sku VARCHAR(100),
  category VARCHAR(100),
  unit_price DECIMAL(10,2),
  stock_qty INT DEFAULT 0,
  extra_data JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Ordens de Serviço
CREATE TABLE service_orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  customer_id UUID REFERENCES customers(id),
  status VARCHAR(100) NOT NULL,   -- etapas definidas pelo workflow da IA
  total DECIMAL(10,2),
  extra_data JSONB,               -- campos dinâmicos por nicho
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Agendamentos
CREATE TABLE schedules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  customer_id UUID REFERENCES customers(id),
  service_order_id UUID REFERENCES service_orders(id),
  scheduled_at TIMESTAMP NOT NULL,
  status VARCHAR(50) DEFAULT 'pending',
  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Financeiro
CREATE TABLE financial_entries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  type VARCHAR(20) NOT NULL,   -- 'income' | 'expense'
  amount DECIMAL(10,2) NOT NULL,
  description TEXT,
  category VARCHAR(100),
  reference_id UUID,           -- service_order_id ou null
  entry_date DATE DEFAULT CURRENT_DATE,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## Tabelas do AI Engine

```sql
-- Histórico de chamadas à IA
CREATE TABLE ai_engine_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID REFERENCES tenants(id),
  action VARCHAR(100),          -- 'analyze_niche' | 'generate_theme' etc
  input_data JSONB,
  output_data JSONB,
  model_used VARCHAR(100),
  tokens_used INT,
  duration_ms INT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Workflows gerados
CREATE TABLE workflow_templates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID REFERENCES tenants(id),
  process_name VARCHAR(100),
  steps JSONB,
  generated_by VARCHAR(50) DEFAULT 'ai_engine',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Campos dinâmicos por entidade
CREATE TABLE dynamic_fields (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID REFERENCES tenants(id),
  entity VARCHAR(100),
  fields JSONB,
  generated_by VARCHAR(50) DEFAULT 'ai_engine',
  created_at TIMESTAMP DEFAULT NOW()
);
```

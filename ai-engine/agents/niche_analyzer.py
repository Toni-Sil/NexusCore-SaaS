from utils.llm import LLMClient
from utils.cache import CacheService
import json

NICHE_ANALYSIS_PROMPT = """
Você é um especialista em SaaS para pequenas e médias empresas.

Analize a seguinte descrição de negócio e retorne um JSON com:
- niche_key: identificador do nicho em snake_case (ex: pet_shop, oficina, barbearia)
- niche_label: nome amigável do nicho
- entity_labels: dicionário traduzindo entidades padrão para o vocabulário do nicho
  (chaves: service_order, customer, product, schedule, inventory, employee)
- active_modules: lista de módulos a ativar
  (opções: crm, service_orders, scheduling, inventory, financial, production, pos, delivery, reports)
- tone: tom de comunicação do sistema (friendly_casual, professional, technical, premium)
- dashboard_metrics: 4 métricas mais relevantes para o nicho

Descrição do negócio: {description}

Retorne APENAS o JSON, sem explicações.
"""


class NicheAnalyzer:
    def __init__(self):
        self.llm = LLMClient()
        self.cache = CacheService()

    async def analyze(self, description: str) -> dict:
        cache_key = f"niche_analysis:{hash(description)}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        prompt = NICHE_ANALYSIS_PROMPT.format(description=description)
        response = await self.llm.complete(prompt)

        try:
            result = json.loads(response)
        except json.JSONDecodeError:
            result = self._fallback_profile(description)

        await self.cache.set(cache_key, result, ttl=3600)
        return result

    def _fallback_profile(self, description: str) -> dict:
        """Fallback estático caso a IA falhe."""
        return {
            "niche_key": "generic_business",
            "niche_label": "Negócio",
            "entity_labels": {
                "service_order": "Ordem de Serviço",
                "customer": "Cliente",
                "product": "Produto",
                "schedule": "Agendamento",
                "inventory": "Estoque",
                "employee": "Colaborador"
            },
            "active_modules": ["crm", "service_orders", "inventory", "financial", "reports"],
            "tone": "professional",
            "dashboard_metrics": ["ordens_hoje", "clientes_cadastrados", "receita_mensal", "estoque_baixo"]
        }

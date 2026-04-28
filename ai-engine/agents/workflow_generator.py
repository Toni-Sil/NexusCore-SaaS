from utils.llm import LLMClient
from utils.cache import CacheService
import json

WORKFLOW_PROMPT = """
Você é especialista em processos operacionais de pequenos negócios.

Crie os status/etapas do fluxo de trabalho de "{process_name}" para um negócio do tipo "{niche_key}".

Retorne um JSON com:
- workflow_name: nome do fluxo
- steps: lista de objetos com:
  - id: número sequencial
  - key: chave em snake_case
  - label: nome da etapa no vocabulário do nicho
  - color: cor associada (blue | yellow | orange | purple | green | red)
  - is_terminal: true se for etapa final

Nicho: {niche_key}
Processo: {process_name}

Retorne APENAS o JSON.
"""


class WorkflowGenerator:
    def __init__(self):
        self.llm = LLMClient()
        self.cache = CacheService()

    async def generate(self, niche_key: str, process_name: str) -> dict:
        cache_key = f"workflow:{niche_key}:{process_name}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        prompt = WORKFLOW_PROMPT.format(
            niche_key=niche_key,
            process_name=process_name
        )
        response = await self.llm.complete(prompt)

        try:
            result = json.loads(response)
        except json.JSONDecodeError:
            result = self._fallback_workflow(niche_key)

        await self.cache.set(cache_key, result, ttl=86400)
        return result

    def _fallback_workflow(self, niche_key: str) -> dict:
        return {
            "workflow_name": "Fluxo padrão",
            "steps": [
                {"id": 1, "key": "open", "label": "Aberto", "color": "blue", "is_terminal": False},
                {"id": 2, "key": "in_progress", "label": "Em andamento", "color": "yellow", "is_terminal": False},
                {"id": 3, "key": "waiting", "label": "Aguardando", "color": "orange", "is_terminal": False},
                {"id": 4, "key": "done", "label": "Concluído", "color": "green", "is_terminal": True}
            ]
        }

from utils.llm import LLMClient
from utils.cache import CacheService
import json

FIELD_PROMPT = """
Você é especialista em formulários de sistemas de gestão para pequenos negócios.

Crie campos extras de formulário para a entidade "{entity}" de um negócio do tipo "{niche_key}".

Retorne um JSON com:
- entity: nome da entidade
- extra_fields: lista de objetos com:
  - name: chave em snake_case
  - label: nome amigável do campo no vocabulário do nicho
  - type: tipo do campo (text | number | select | date | textarea | boolean)
  - required: true ou false
  - options: lista de opções (apenas para type=select)
  - placeholder: exemplo de preenchimento

Apenas campos ESPECÍFICOS do nicho, não campos genéricos (nome, telefone, etc já existem).

Nicho: {niche_key}
Entidade: {entity}

Retorne APENAS o JSON.
"""


class FieldGenerator:
    def __init__(self):
        self.llm = LLMClient()
        self.cache = CacheService()

    async def generate(self, niche_key: str, entity: str) -> dict:
        cache_key = f"fields:{niche_key}:{entity}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        prompt = FIELD_PROMPT.format(niche_key=niche_key, entity=entity)
        response = await self.llm.complete(prompt)

        try:
            result = json.loads(response)
        except json.JSONDecodeError:
            result = {"entity": entity, "extra_fields": []}

        await self.cache.set(cache_key, result, ttl=86400)
        return result

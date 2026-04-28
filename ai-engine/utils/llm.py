import os
from openai import AsyncOpenAI


class LLMClient:
    """
    Abstração do cliente LLM.
    Suporta OpenAI (padrão) com fallback para Gemini.
    """

    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")

    async def complete(self, prompt: str) -> str:
        try:
            response = await self.openai_client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,  # baixo para respostas mais determinísticas
                response_format={"type": "json_object"},
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"LLM call failed: {str(e)}")

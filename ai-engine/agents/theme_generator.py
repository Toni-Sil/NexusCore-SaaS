from utils.llm import LLMClient
from utils.cache import CacheService
import json

THEME_GENERATION_PROMPT = """
Você é um designer de UI especializado em SaaS para negócios.

Crie um tema visual profissional para um sistema de gestão de {niche_label}.

Retorne um JSON com:
- primary_color: cor principal em hex (considere a identidade do nicho)
- secondary_color: cor secundária em hex
- accent_color: cor de destaque em hex
- bg_color: cor de fundo principal
- surface_color: cor de cards/superfícies
- font_display: fonte para títulos (usar fontes do Google Fonts ou Fontshare)
- font_body: fonte para corpo de texto
- border_radius: tamanho do arredondamento (sm | md | lg | xl)
- sidebar_style: estilo da sidebar (light | dark)
- icon_style: estilo dos ícones (outline | filled | rounded)
- logo_concept: descrição de um conceito de logo simples para o nicho
- illustration_style: estilo de ilustrações (flat | 3d | minimal | none)

Nicho: {niche_key}
Nome do nicho: {niche_label}

Considere as convenções visuais do setor. Retorne APENAS o JSON.
"""


class ThemeGenerator:
    def __init__(self):
        self.llm = LLMClient()
        self.cache = CacheService()

    async def generate(self, niche_key: str, niche_label: str) -> dict:
        cache_key = f"theme:{niche_key}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        prompt = THEME_GENERATION_PROMPT.format(
            niche_key=niche_key,
            niche_label=niche_label
        )
        response = await self.llm.complete(prompt)

        try:
            result = json.loads(response)
        except json.JSONDecodeError:
            result = self._fallback_theme(niche_key)

        await self.cache.set(cache_key, result, ttl=86400)  # 24h
        return result

    def _fallback_theme(self, niche_key: str) -> dict:
        themes = {
            "pet_shop": {"primary_color": "#2E7D32", "secondary_color": "#81C784", "accent_color": "#FF8F00"},
            "oficina": {"primary_color": "#1565C0", "secondary_color": "#42A5F5", "accent_color": "#FF6D00"},
            "barbearia": {"primary_color": "#212121", "secondary_color": "#424242", "accent_color": "#CFB53B"},
            "fabrica": {"primary_color": "#37474F", "secondary_color": "#78909C", "accent_color": "#66BB6A"},
            "varejo": {"primary_color": "#E65100", "secondary_color": "#FFA726", "accent_color": "#1565C0"},
            "clinica": {"primary_color": "#0277BD", "secondary_color": "#4FC3F7", "accent_color": "#00897B"},
        }
        base = themes.get(niche_key, {"primary_color": "#01696f", "secondary_color": "#4f98a3", "accent_color": "#da7101"})
        return {
            **base,
            "bg_color": "#F8F9FA",
            "surface_color": "#FFFFFF",
            "font_display": "Cabinet Grotesk",
            "font_body": "Satoshi",
            "border_radius": "md",
            "sidebar_style": "dark",
            "icon_style": "outline",
            "logo_concept": f"símbolo minimalista relacionado a {niche_key}",
            "illustration_style": "flat"
        }

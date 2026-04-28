from agents.niche_analyzer import NicheAnalyzer
from agents.theme_generator import ThemeGenerator
from agents.workflow_generator import WorkflowGenerator
from agents.field_generator import FieldGenerator
import asyncio


class NexusCoreOrchestrator:
    """
    Orquestrador central do AI Engine.
    Coordena todos os agentes para fazer o full-setup de um tenant.
    """

    def __init__(self):
        self.niche_analyzer = NicheAnalyzer()
        self.theme_generator = ThemeGenerator()
        self.workflow_generator = WorkflowGenerator()
        self.field_generator = FieldGenerator()

    async def full_setup(self, description: str, tenant_id: str) -> dict:
        """
        1. Analisa o nicho
        2. Em paralelo: gera tema, workflows e campos
        3. Retorna tudo em um único objeto TenantSetup
        """

        # Passo 1: análise do nicho (sequencial — os outros dependem disso)
        niche_profile = await self.niche_analyzer.analyze(description)
        niche_key = niche_profile["niche_key"]
        niche_label = niche_profile["niche_label"]

        # Passo 2: gera tema, workflows e campos EM PARALELO
        theme_task = self.theme_generator.generate(niche_key, niche_label)
        workflow_task = self.workflow_generator.generate(niche_key, "service_order")
        customer_fields_task = self.field_generator.generate(niche_key, "customer")
        order_fields_task = self.field_generator.generate(niche_key, "service_order")

        theme, workflow, customer_fields, order_fields = await asyncio.gather(
            theme_task,
            workflow_task,
            customer_fields_task,
            order_fields_task
        )

        return {
            "tenant_id": tenant_id,
            "niche_profile": niche_profile,
            "theme": theme,
            "workflows": {
                "service_order": workflow
            },
            "dynamic_fields": {
                "customer": customer_fields,
                "service_order": order_fields
            },
            "active_modules": niche_profile.get("active_modules", []),
            "entity_labels": niche_profile.get("entity_labels", {}),
        }

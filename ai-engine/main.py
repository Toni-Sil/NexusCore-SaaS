from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os

from agents.orchestrator import NexusCoreOrchestrator
from agents.niche_analyzer import NicheAnalyzer
from agents.theme_generator import ThemeGenerator
from agents.workflow_generator import WorkflowGenerator
from agents.field_generator import FieldGenerator
from utils.cache import CacheService

app = FastAPI(
    title="NexusCore AI Engine",
    description="Motor de IA adaptativa para o NexusCore SaaS",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("NEXUSCORE_BACKEND_URL", "http://localhost:3000")],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Schemas ---

class NicheInput(BaseModel):
    description: str          # "sou dono de uma barbearia no centro"
    tenant_id: Optional[str] = None

class NicheProfileInput(BaseModel):
    niche_key: str
    niche_label: str
    tenant_id: Optional[str] = None

class WorkflowInput(BaseModel):
    niche_key: str
    process_name: str
    tenant_id: Optional[str] = None

class FieldInput(BaseModel):
    niche_key: str
    entity: str               # 'customer' | 'service_order' | 'product'
    tenant_id: Optional[str] = None

class FullSetupInput(BaseModel):
    description: str
    tenant_id: str

# --- Endpoints ---

@app.get("/health")
async def health():
    return {"status": "ok", "service": "NexusCore AI Engine"}


@app.post("/ai/analyze-niche")
async def analyze_niche(data: NicheInput):
    """
    Recebe uma descrição livre do negócio e retorna um NicheProfile completo.
    Ex: input: "oficina mecânica focada em carros importados"
    """
    analyzer = NicheAnalyzer()
    result = await analyzer.analyze(data.description)
    return result


@app.post("/ai/generate-theme")
async def generate_theme(data: NicheProfileInput):
    """
    Recebe o nicho e retorna um ThemeConfig com paleta, fontes e estilo.
    """
    generator = ThemeGenerator()
    result = await generator.generate(data.niche_key, data.niche_label)
    return result


@app.post("/ai/generate-workflow")
async def generate_workflow(data: WorkflowInput):
    """
    Gera os steps de um workflow específico para o nicho.
    """
    generator = WorkflowGenerator()
    result = await generator.generate(data.niche_key, data.process_name)
    return result


@app.post("/ai/generate-fields")
async def generate_fields(data: FieldInput):
    """
    Gera campos dinâmicos de formulário para uma entidade específica.
    """
    generator = FieldGenerator()
    result = await generator.generate(data.niche_key, data.entity)
    return result


@app.post("/ai/full-setup")
async def full_setup(data: FullSetupInput):
    """
    Endpoint principal do onboarding.
    Recebe a descrição do negócio e gera TUDO de uma vez:
    NicheProfile + ThemeConfig + Workflows + Fields + Dashboard config.
    """
    orchestrator = NexusCoreOrchestrator()
    result = await orchestrator.full_setup(
        description=data.description,
        tenant_id=data.tenant_id
    )
    return result

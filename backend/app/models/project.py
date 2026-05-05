from pydantic import BaseModel
from typing import Optional

class ProjectInput(BaseModel):
    """
    Modèle unifié pour les nouveaux projets Mawaba.
    """
    titre: str
    description: str
    contexte: str
    echeancier: str
    budget_max: str

class GenerationResponse(BaseModel):
    project_id: str
    status: str
    links: dict[str, str]
    message: str
import os
import uuid
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from fastapi.concurrency import run_in_threadpool
from app.models.project import ProjectInput, GenerationResponse
from app.services.generator import generate_all_deliverables

router = APIRouter()

# Stockage en mémoire
projects_data = {}

@router.post("/generate", response_model=GenerationResponse)
async def generate_documents(project: ProjectInput):
    """
    Génère l'ensemble des livrables (Word, Excel, HTML) via le moteur unifié.
    """
    project_id = uuid.uuid4().hex[:8]
    project_info = project.dict()
    
    try:
        # Exécution du moteur de génération (bloquant -> threadpool)
        results = await run_in_threadpool(generate_all_deliverables, project_info)
        
        projects_data[project_id] = {
            "deliverables": results,
            "info": project_info
        }
        
        # Préparation des liens publics
        links = {
            key: f"/api/download/{project_id}/{key}"
            for key in results.keys()
        }
        
        return GenerationResponse(
            project_id=project_id,
            status="success",
            links=links,
            message="Tous les livrables ont été générés avec succès."
        )
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{project_id}/{key}")
async def download_file(project_id: str, key: str):
    """
    Télécharge un livrable spécifique.
    """
    if project_id not in projects_data:
        raise HTTPException(status_code=404, detail="Projet introuvable")
        
    deliverables = projects_data[project_id]["deliverables"]
    if key not in deliverables:
        raise HTTPException(status_code=404, detail="Livrable introuvable")
        
    filepath = deliverables[key]
    
    if not os.path.exists(filepath):
        # Tentative avec chemin absolu si nécessaire
        abs_path = os.path.abspath(filepath)
        if not os.path.exists(abs_path):
             raise HTTPException(status_code=404, detail=f"Fichier introuvable sur le disque : {filepath}")
        filepath = abs_path

    filename = os.path.basename(filepath)
    
    media_type = "application/octet-stream"
    if filepath.endswith(".docx"):
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    elif filepath.endswith(".xlsx"):
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    elif filepath.endswith(".html"):
        media_type = "text/html"
        
    return FileResponse(
        path=filepath,
        filename=filename,
        media_type=media_type
    )

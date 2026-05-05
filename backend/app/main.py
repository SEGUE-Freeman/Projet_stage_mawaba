import os
import uuid
import json
from typing import Optional
from fastapi import FastAPI, APIRouter, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq

from app.services.generator import generate_all_deliverables

load_dotenv()

# --- MODÈLES ---
class ProjectInput(BaseModel):
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

# --- APP SETUP ---
app = FastAPI(title="Mawaba Unified")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store for generated file paths
projects_data = {}

@app.post("/api/generate", response_model=GenerationResponse)
async def generate_all(project: ProjectInput):
    p_id = uuid.uuid4().hex[:8]
    p_info = project.dict()
    
    try:
        # Utilisation du service centralisé pour générer les 5 livrables
        results = generate_all_deliverables(p_info)
        
        # Sauvegarde des chemins pour le téléchargement
        projects_data[p_id] = results
        
        # Construction des liens de téléchargement
        links = {k: f"/api/download/{p_id}/{k}" for k in results.keys()}
        
        return GenerationResponse(
            project_id=p_id, 
            status="success", 
            links=links, 
            message="Tous les documents ont été générés avec succès."
        )
        
    except Exception as e:
        print(f"CRITICAL ERROR during generation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération: {str(e)}")

@app.get("/api/download/{p_id}/{key}")
async def download(p_id: str, key: str):
    if p_id not in projects_data or key not in projects_data[p_id]:
        raise HTTPException(status_code=404, detail="Fichier non trouvé ou lien expiré.")
    
    file_path = projects_data[p_id][key]
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Le fichier physique est introuvable sur le serveur.")
        
    # On extrait le nom du fichier pour forcer le téléchargement (Content-Disposition: attachment)
    filename = os.path.basename(file_path)
    return FileResponse(file_path, filename=filename)

# --- STATIC FILES ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FRONTEND_PATH = os.path.join(BASE_DIR, "frontend")
if os.path.exists(FRONTEND_PATH):
    app.mount("/", StaticFiles(directory=FRONTEND_PATH, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    print(f"Lancement Mawaba Unified sur http://127.0.0.1:8080")
    uvicorn.run(app, host="0.0.0.0", port=8080)
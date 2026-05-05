import os
import sys

# Ajout du chemin racine pour l'import des modules locaux
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.generator import generate_all_deliverables

def run_diagnostic():
    print("--- DÉBUT DE L'AUDIT LOGIQUE ---")
    
    project_info = {
        "titre": "PROJET TEST AUDIT",
        "description": "Un projet de test pour vérifier que la génération fonctionne sans erreurs de type ou de quota.",
        "contexte": "Audit technique du système de génération Mawaba.",
        "echeancier": "Dès que possible",
        "budget_max": "1000 EUR"
    }
    
    try:
        print("1. Tentative de génération des 5 livrables...")
        results = generate_all_deliverables(project_info)
        
        print("\n2. Vérification de l'existence physique des fichiers :")
        for key, path in results.items():
            if os.path.exists(path):
                size = os.path.getsize(path)
                print(f"   [OK] {key}: {path} ({size} octets)")
                if size < 100:
                    print(f"   [ATTENTION] Le fichier {key} semble anormalement petit.")
            else:
                print(f"   [ERREUR] {key}: Le fichier n'existe pas !")
        
        print("\n--- AUDIT TERMINÉ AVEC SUCCÈS ---")
        
    except Exception as e:
        print(f"\n[ERREUR CRITIQUE] L'audit a échoué : {str(e)}")

if __name__ == "__main__":
    run_diagnostic()

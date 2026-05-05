import sys
import os

# Ajouter le chemin du backend pour l'import
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.services.docx_gen import create_word_document

def test_table_parsing():
    content = """
# Test Table
Voici un tableau avec des bordures :
| Colonne 1 | Colonne 2 | Colonne 3 |
|-----------|-----------|-----------|
| Valeur 1  | Valeur 2  | Valeur 3  |
| A         | B         | C         |

Un autre paragraphe.
"""
    print("Génération du document de test...")
    filepath = create_word_document(content, "Test Table Correction", "Test")
    print(f"Document généré : {filepath}")
    
    if os.path.exists(filepath):
        print("SUCCÈS : Le fichier a été créé.")
        # On pourrait ici utiliser python-docx pour vérifier le nombre de colonnes dans le XML
    else:
        print("ÉCHEC : Le fichier n'a pas été créé.")

if __name__ == "__main__":
    test_table_parsing()

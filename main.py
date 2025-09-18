from services.auth_service import AuthService
from services.projet_service import ProjetService
from services.storage_service import StorageService
from models.projet import ProjetIA

def demo_complete():
    """Démonstration complète des fonctionnalités"""
    
    print("🚀 === DEMO SUPABASE + PYTHON === 🚀\n")
    
    # 1. Authentification
    print("1️⃣ === AUTHENTIFICATION ===")
    
    # Inscription (ou connexion si existe)
    auth_result = AuthService.connecter_utilisateur(
        "demo@example.com", 
        "motdepasse123"
    )
    
    if not auth_result["success"]:
        print("Création du compte de démo...")
        auth_result = AuthService.inscrire_utilisateur(
            "demo@example.com", 
            "motdepasse123"
        )
    
    if auth_result["success"]:
        user_id = auth_result["user"].id
        print(f"✅ Utilisateur connecté: {auth_result['user'].email}")
    else:
        print(f"❌ Erreur auth: {auth_result['message']}")
        return
    
    # 2. CRUD Projets
    print("\n2️⃣ === CRUD PROJETS ===")
    
    # Création
    nouveau_projet = ProjetIA(
        nom="Classification d'Images",
        description="Modèle CNN pour classifier des images de chats et chiens",
        type_modele="Computer Vision"
    )
    
    try:
        projet_cree = ProjetService.creer_projet(nouveau_projet, user_id)
        print(f"✅ Projet créé: {projet_cree.nom} (ID: {projet_cree.id})")
        
        # Lecture
        projets = ProjetService.lister_projets(user_id)
        print(f"📋 Nombre de projets: {len(projets)}")
        
        # Mise à jour
        ProjetService.mettre_a_jour_projet(
            projet_cree.id,
            {"statut": "termine", "description": "Modèle CNN entraîné avec succès"},
            user_id
        )
        print("✅ Projet mis à jour")
        
        # Recherche
        resultats = ProjetService.rechercher_projets(user_id, "CNN")
        print(f"🔍 Projets trouvés avec 'CNN': {len(resultats)}")
        
    except Exception as e:
        print(f"❌ Erreur CRUD: {str(e)}")
    
    # 3. Storage (simulation)
    print("\n3️⃣ === STORAGE ===")
    try:
        fichiers = StorageService.lister_fichiers()
        print(f"📁 Fichiers dans le storage: {len(fichiers)}")
    except Exception as e:
        print(f"❌ Erreur storage: {str(e)}")

    
    # 4. Gestion des Datasets
print("\n4️⃣ === GESTION DATASETS ===")

if projet_cree:
    try:
        # Simulation d'un dataset
        nouveau_dataset = Dataset(
            nom="Images d'entraînement",
            projet_id=projet_cree.id,
            format_fichier="CSV",
            taille_mb=Decimal("45.7")
        )
        
        dataset_cree = DatasetService.creer_dataset(nouveau_dataset)
        print(f"✅ Dataset créé: {dataset_cree.nom}")
        print(f"   Taille: {dataset_cree.get_taille_formatee()}")
        
        # Lister les datasets du projet
        datasets = DatasetService.lister_datasets_projet(projet_cree.id)
        print(f"📋 Datasets du projet: {len(datasets)}")
        
        # Statistiques
        stats = DatasetService.statistiques_datasets(projet_cree.id)
        print(f"📊 Statistiques:")
        print(f"   - Nombre total: {stats['nombre_datasets']}")
        print(f"   - Taille totale: {stats['taille_totale_formatee']}")
        print(f"   - Formats: {stats['formats']}")
        
    except Exception as e:
        print(f"❌ Erreur datasets: {str(e)}")
    
    print("\n🎉 === DEMO TERMINÉE === 🎉")

if __name__ == "__main__":
    demo_complete()
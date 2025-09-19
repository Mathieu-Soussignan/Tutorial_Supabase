# main.py
from services.auth_service import AuthService
from services.projet_service import ProjetService
from services.storage_service import StorageService
from services.dataset_service import DatasetService
from models.projet import ProjetIA
from models.dataset import Dataset
from decimal import Decimal
import uuid


def demo_complete():
    """Démonstration complète avec authentification"""
    
    print("🚀 === DEMO SUPABASE + PYTHON === 🚀\n")
    
    # Variables pour stocker les résultats
    user_id = None
    projet_cree = None
    
    # 1. Authentification RÉELLE
    print("1️⃣ === AUTHENTIFICATION ===")
    
    try:
        # Créer un utilisateur de démo réel
        demo_email = "demo-tuto@supabase.demo"
        demo_password = "DemoSupabase2025!"
        
        print("📧 Tentative de connexion utilisateur démo...")
        
        # D'abord essayer de se connecter (au cas où il existe déjà)
        auth_result = AuthService.connecter_utilisateur(demo_email, demo_password)
        
        if not auth_result["success"]:
            print("🆕 Création d'un nouvel utilisateur démo...")
            auth_result = AuthService.inscrire_utilisateur(demo_email, demo_password)
            
            if auth_result["success"]:
                print("✅ Utilisateur créé avec succès")
            else:
                print(f"⚠️ Inscription échouée: {auth_result.get('message', 'Erreur inconnue')}")
                # Réessayer la connexion au cas où l'utilisateur existe déjà
                auth_result = AuthService.connecter_utilisateur(demo_email, demo_password)
        
        if auth_result["success"]:
            user_id = auth_result["user"].id
            print(f"✅ Utilisateur authentifié: {demo_email}")
            print(f"   ID: {user_id[:8]}...")
        else:
            raise Exception(f"Impossible d'authentifier: {auth_result.get('message', 'Erreur inconnue')}")
            
    except Exception as e:
        print(f"❌ Erreur authentification: {str(e)}")
        print("🔄 Solution de fallback...")
        
        try:
            # Fallback 1 : Essayer l'auth anonyme
            print("   Tentative auth anonyme...")
            auth_result = AuthService.connexion_anonyme()
            
            if auth_result["success"]:
                user_id = auth_result["user"].id
                print(f"✅ Utilisateur anonyme connecté: {user_id[:8]}...")
            else:
                raise Exception("Auth anonyme échouée")
                
        except Exception as e2:
            # Fallback 2 : Mode démo avec user_id = None
            print(f"   Auth anonyme échouée: {str(e2)}")
            print("🎭 Mode démo sans authentification")
            user_id = None
            print("✅ Démonstration en mode standalone")
    
    # 2. CRUD Projets
    print("\n2️⃣ === CRUD PROJETS ===")
    
    # Création d'un projet avec des hyperparamètres réalistes
    nouveau_projet = ProjetIA(
        nom="Classification d'Images - Chats vs Chiens",
        description="Modèle CNN pour classifier des images de chats et chiens avec transfer learning",
        type_modele="Computer Vision",
        hyperparametres={
            "architecture": "ResNet50",
            "pretrained": True,
            "epochs": 25,
            "batch_size": 32,
            "learning_rate": 0.001,
            "optimizer": "Adam",
            "loss_function": "categorical_crossentropy",
            "metrics": ["accuracy", "precision", "recall"],
            "early_stopping": True,
            "patience": 5
        }
    )
    
    try:
        # Passer user_id même s'il est None - le service doit gérer ça
        projet_cree = ProjetService.creer_projet_ia(nouveau_projet, user_id)
        print(f"✅ Projet créé: {projet_cree.nom}")
        print(f"   ID: {projet_cree.id}")
        print(f"   Type: {projet_cree.type_modele}")
        print(f"   Statut: {projet_cree.statut}")
        
        # Lecture - adapter selon si on a un user_id ou pas
        if user_id:
            projets = ProjetService.lister_projets(user_id)
            print(f"📋 Nombre de projets pour cet utilisateur: {len(projets)}")
        else:
            print("📋 Mode démo : impossible de lister les projets par utilisateur")
        
        # Mise à jour avec des infos réalistes
        updates = {
            "statut": "en_cours", 
            "description": "Modèle CNN avec transfer learning - Phase d'entraînement"
        }
        
        if user_id:
            projet_mis_a_jour = ProjetService.mettre_a_jour_projet(
                projet_cree.id,
                updates,
                user_id
            )
            print("✅ Projet mis à jour")
        else:
            print("⚠️ Mise à jour sautée (mode démo sans user_id)")
        
        # Recherche intelligente
        if user_id:
            termes_recherche = ["CNN", "Computer Vision", "ResNet"]
            for terme in termes_recherche[:1]:  # Juste un exemple
                resultats = ProjetService.rechercher_projets(user_id, terme)
                print(f"🔍 Recherche '{terme}': {len(resultats)} résultat(s)")
        
        # Statistiques
        if user_id:
            stats = ProjetService.statistiques_projets(user_id)
            print(f"📊 Statistiques projets:")
            print(f"   - Total: {stats['total']}")
            print(f"   - Par type: {stats['par_type']}")
            print(f"   - Type favori: {stats.get('type_favori', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Erreur CRUD: {str(e)}")
        print("💡 Vérifiez :")
        print("   - Que les tables sont créées dans Supabase")
        print("   - Que RLS est configuré correctement")
        print("   - Que les contraintes FK sont adaptées")
    
    # 3. Storage (simulation)
    print("\n3️⃣ === STORAGE ===")
    try:
        fichiers = StorageService.lister_fichiers()
        print(f"📁 Fichiers dans le storage: {len(fichiers)}")
        
        if len(fichiers) == 0:
            print("   💡 Aucun fichier trouvé - c'est normal pour une première démo")
        else:
            print(f"   📄 Exemples de fichiers:")
            for fichier in fichiers[:3]:  # Montrer max 3 fichiers
                print(f"      • {fichier.get('name', 'fichier inconnu')}")
                
    except Exception as e:
        print(f"❌ Erreur storage: {str(e)}")
        print("💡 Créez le bucket 'datasets' dans Supabase Storage")
    
    # 4. Gestion des Datasets
    print("\n4️⃣ === GESTION DATASETS ===")
    
    if projet_cree:
        try:
            # Dataset 1 : Images d'entraînement
            dataset_train = Dataset(
                nom="Images d'entraînement - Chats/Chiens",
                projet_id=projet_cree.id,
                format_fichier="ZIP",
                taille_mb=Decimal("157.3"),
                nb_lignes=8000
            )
            
            dataset_cree = DatasetService.creer_dataset(dataset_train)
            print(f"✅ Dataset créé: {dataset_cree.nom}")
            print(f"   Taille: {dataset_cree.get_taille_formatee()}")
            print(f"   Format: {dataset_cree.format_fichier}")
            
            # Dataset 2 : Images de validation
            dataset_val = Dataset(
                nom="Images de validation",
                projet_id=projet_cree.id,
                format_fichier="ZIP",
                taille_mb=Decimal("34.2"),
                nb_lignes=2000
            )
            
            dataset_cree2 = DatasetService.creer_dataset(dataset_val)
            print(f"✅ Dataset 2 créé: {dataset_cree2.nom}")
            print(f"   Taille: {dataset_cree2.get_taille_formatee()}")
            
            # Dataset 3 : Métadonnées
            dataset_meta = Dataset(
                nom="Métadonnées et annotations",
                projet_id=projet_cree.id,
                format_fichier="JSON",
                taille_mb=Decimal("2.7"),
                nb_lignes=10000
            )
            
            dataset_cree3 = DatasetService.creer_dataset(dataset_meta)
            print(f"✅ Dataset 3 créé: {dataset_cree3.nom}")
            
            # Statistiques des datasets
            datasets = DatasetService.lister_datasets_projet(projet_cree.id)
            print(f"\n📋 Total datasets du projet: {len(datasets)}")
            
            stats = DatasetService.statistiques_datasets(projet_cree.id)
            print(f"📊 Statistiques datasets:")
            print(f"   - Nombre total: {stats['nombre_datasets']}")
            print(f"   - Taille totale: {stats['taille_totale_formatee']}")
            print(f"   - Formats: {stats['formats']}")
            
            if stats['dataset_plus_gros']:
                print(f"   - Plus volumineux: {stats['dataset_plus_gros']['nom']}")
                print(f"     ({stats['dataset_plus_gros']['taille']})")
            
        except Exception as e:
            print(f"❌ Erreur datasets: {str(e)}")
    else:
        print("⚠️ Aucun projet créé, impossible de créer des datasets")
    
    # 5. Hyperparamètres détaillés
    print("\n5️⃣ === HYPERPARAMÈTRES ===")
    if projet_cree and projet_cree.hyperparametres:
        print("🔧 Configuration du modèle:")
        for param, valeur in projet_cree.hyperparametres.items():
            # Formatting spécial pour certains paramètres
            if isinstance(valeur, float):
                print(f"   • {param}: {valeur:.4f}")
            elif isinstance(valeur, bool):
                print(f"   • {param}: {'✅ Oui' if valeur else '❌ Non'}")
            elif isinstance(valeur, list):
                print(f"   • {param}: {', '.join(map(str, valeur))}")
            else:
                print(f"   • {param}: {valeur}")
    
    # 6. Récapitulatif final
    print("\n6️⃣ === RÉCAPITULATIF ===")
    if user_id:
        print(f"👤 Utilisateur: {user_id[:8]}... (authentifié)")
    else:
        print(f"👤 Mode: Démo standalone")
        
    if projet_cree:
        print(f"📋 Projet principal: {projet_cree.nom}")
        print(f"🏷️ Type: {projet_cree.type_modele}")
        print(f"📊 Hyperparamètres: {len(projet_cree.hyperparametres or {})} configurés")
        
        try:
            datasets_count = len(DatasetService.lister_datasets_projet(projet_cree.id))
            print(f"📁 Datasets: {datasets_count} créés")
        except:
            print(f"📁 Datasets: Information non disponible")
    else:
        print("📋 Aucun projet créé")
    
    print("\n🎉 === DEMO TERMINÉE === 🎉")
    print("🚀 Supabase + Python = GOAT Stack pour l'IA ! 🐐")


if __name__ == "__main__":
    demo_complete()
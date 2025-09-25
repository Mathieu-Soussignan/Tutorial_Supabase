# services/dataset_service.py - VERSION DÉMO COMPATIBLE
from typing import List, Optional, Dict
from config.database import supabase
import os
from datetime import datetime
from decimal import Decimal


class DatasetService:
    
    @staticmethod
    def creer_dataset_simple(nom: str, projet_id: str, taille_mb: float, format_fichier: str, nb_lignes: int = None) -> Dict:
        """Version simplifiée pour créer un dataset (démo)"""
        try:
            data = {
                "nom": nom,
                "projet_id": projet_id,
                "taille_mb": taille_mb,
                "format_fichier": format_fichier,
                "nb_lignes": nb_lignes,
                "fichier_url": f"demo://datasets/{nom.lower().replace(' ', '_')}.{format_fichier.lower()}"
            }
            
            response = supabase.table('datasets').insert(data).execute()
            return response.data[0] if response.data else None
                
        except Exception as e:
            raise Exception(f"Erreur service dataset: {str(e)}")
    
    @staticmethod
    def creer_dataset(dataset) -> Dict:
        """Créer un nouveau dataset - VERSION COMPATIBLE"""
        try:
            # Si c'est un objet Dataset, convertir en dict
            if hasattr(dataset, 'to_dict'):
                data = dataset.to_dict()
            else:
                data = dataset
            
            response = supabase.table('datasets').insert(data).execute()
            
            if response.data:
                return response.data[0]
            else:
                raise Exception("Erreur lors de la création du dataset")
                
        except Exception as e:
            raise Exception(f"Erreur service dataset: {str(e)}")
    
    @staticmethod
    def lister_datasets_projet(projet_id: str) -> List[Dict]:
        """Lister tous les datasets d'un projet - VERSION SIMPLIFIÉE"""
        try:
            response = supabase.table('datasets')\
                .select('*')\
                .eq('projet_id', projet_id)\
                .order('created_at', desc=True)\
                .execute()
            
            return response.data or []
            
        except Exception as e:
            print(f"Erreur récupération datasets: {str(e)}")
            return []
    
    @staticmethod 
    def lister_tous_datasets() -> List[Dict]:
        """Lister TOUS les datasets (pour démo)"""
        try:
            response = supabase.table('datasets')\
                .select('*')\
                .order('created_at', desc=True)\
                .limit(50)\
                .execute()
            
            return response.data or []
            
        except Exception as e:
            print(f"Erreur récupération datasets: {str(e)}")
            return []
    
    @staticmethod
    def uploader_et_creer_dataset(
        fichier_path: str, 
        nom_dataset: str, 
        projet_id: str,
        format_fichier: str
    ) -> Dict:
        """Upload un fichier et crée le dataset correspondant - VERSION DÉMO"""
        try:
            # Mode démo : simuler l'upload
            if not os.path.exists(fichier_path):
                # Simuler une taille réaliste
                taille_mb = 45.7  # Exemple
            else:
                # Calculer la vraie taille
                taille_bytes = os.path.getsize(fichier_path)
                taille_mb = round(taille_bytes / (1024 * 1024), 2)
            
            # Simuler l'URL de fichier
            timestamp = int(datetime.now().timestamp())
            fichier_url = f"demo://storage/{projet_id}/{timestamp}_{os.path.basename(fichier_path)}"
            
            # Créer l'entrée dataset
            data = {
                "nom": nom_dataset,
                "projet_id": projet_id,
                "fichier_url": fichier_url,
                "taille_mb": taille_mb,
                "format_fichier": format_fichier,
                "nb_lignes": 10000 if format_fichier.upper() in ['CSV', 'JSON'] else None
            }
            
            return DatasetService.creer_dataset(data)
            
        except Exception as e:
            raise Exception(f"Erreur upload dataset: {str(e)}")
    
    @staticmethod
    def supprimer_dataset(dataset_id: str, supprimer_fichier: bool = True) -> bool:
        """Supprimer un dataset - VERSION SIMPLIFIÉE"""
        try:
            response = supabase.table('datasets')\
                .delete()\
                .eq('id', dataset_id)\
                .execute()
            
            return len(response.data or []) > 0
            
        except Exception as e:
            print(f"Erreur suppression dataset: {str(e)}")
            return False
    
    @staticmethod
    def statistiques_datasets(projet_id: str = None) -> Dict:
        """Récupère les statistiques des datasets"""
        try:
            if projet_id:
                datasets = DatasetService.lister_datasets_projet(projet_id)
            else:
                datasets = DatasetService.lister_tous_datasets()
            
            if not datasets:
                return {
                    "nombre_datasets": 0,
                    "taille_totale_mb": 0,
                    "taille_totale_formatee": "0 MB",
                    "formats": {},
                    "dataset_plus_gros": None
                }
            
            # Calculs statistiques
            taille_totale = sum(float(d.get('taille_mb', 0) or 0) for d in datasets)
            formats = {}
            dataset_plus_gros = None
            
            # Trouver le plus gros dataset
            if datasets:
                dataset_plus_gros = max(datasets, key=lambda d: float(d.get('taille_mb', 0) or 0))
            
            # Comptage des formats
            for dataset in datasets:
                format_fichier = dataset.get('format_fichier', 'inconnu') or "inconnu"
                formats[format_fichier] = formats.get(format_fichier, 0) + 1
            
            # Formatage de la taille
            if taille_totale >= 1024:
                taille_formatee = f"{taille_totale/1024:.1f} GB"
            else:
                taille_formatee = f"{taille_totale:.1f} MB"
            
            return {
                "nombre_datasets": len(datasets),
                "taille_totale_mb": round(taille_totale, 2),
                "taille_totale_formatee": taille_formatee,
                "formats": formats,
                "dataset_plus_gros": {
                    "nom": dataset_plus_gros.get('nom', 'Inconnu'),
                    "taille": f"{dataset_plus_gros.get('taille_mb', 0):.1f} MB"
                } if dataset_plus_gros and dataset_plus_gros.get('taille_mb') else None
            }
            
        except Exception as e:
            print(f"Erreur calcul statistiques: {str(e)}")
            return {
                "nombre_datasets": 0,
                "taille_totale_mb": 0,
                "taille_totale_formatee": "0 MB", 
                "formats": {},
                "dataset_plus_gros": None
            }
    
    @staticmethod
    def rechercher_datasets(terme: str, projet_id: str = None) -> List[Dict]:
        """Recherche des datasets par nom"""
        try:
            query = supabase.table('datasets')\
                .select('*')\
                .ilike('nom', f'%{terme}%')
            
            if projet_id:
                query = query.eq('projet_id', projet_id)
            
            response = query.execute()
            return response.data or []
            
        except Exception as e:
            print(f"Erreur recherche datasets: {str(e)}")
            return []
    
    @staticmethod
    def mettre_a_jour_dataset(dataset_id: str, updates: Dict) -> Dict:
        """Mettre à jour un dataset"""
        try:
            response = supabase.table('datasets')\
                .update(updates)\
                .eq('id', dataset_id)\
                .execute()
            
            if response.data:
                return response.data[0]
            else:
                raise Exception("Dataset non trouvé")
                
        except Exception as e:
            raise Exception(f"Erreur mise à jour dataset: {str(e)}")

# FONCTIONS UTILITAIRES POUR LA DÉMO
def creer_datasets_demo(projet_id: str) -> List[Dict]:
    """Créer des datasets de démonstration"""
    datasets_demo = [
        {
            "nom": "Images d'entraînement - Chats/Chiens", 
            "taille_mb": 157.3,
            "format_fichier": "ZIP",
            "nb_lignes": None
        },
        {
            "nom": "Images de validation",
            "taille_mb": 34.2, 
            "format_fichier": "ZIP",
            "nb_lignes": None
        },
        {
            "nom": "Métadonnées et annotations",
            "taille_mb": 2.7,
            "format_fichier": "JSON", 
            "nb_lignes": 8574
        }
    ]
    
    datasets_crees = []
    for dataset_info in datasets_demo:
        try:
            dataset = DatasetService.creer_dataset_simple(
                nom=dataset_info["nom"],
                projet_id=projet_id,
                taille_mb=dataset_info["taille_mb"],
                format_fichier=dataset_info["format_fichier"],
                nb_lignes=dataset_info["nb_lignes"]
            )
            if dataset:
                datasets_crees.append(dataset)
        except Exception as e:
            print(f"Erreur création dataset démo: {e}")
    
    return datasets_crees
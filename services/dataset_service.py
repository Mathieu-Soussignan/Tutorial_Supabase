from typing import List, Optional, Dict
from config.database import supabase
from models.dataset import Dataset
import os

class DatasetService:
    
    @staticmethod
    def creer_dataset(dataset: Dataset) -> Dataset:
        """Créer un nouveau dataset"""
        try:
            data = dataset.to_dict()
            
            response = supabase.table('datasets').insert(data).execute()
            
            if response.data:
                return Dataset.from_dict(response.data[0])
            else:
                raise Exception("Erreur lors de la création du dataset")
                
        except Exception as e:
            raise Exception(f"Erreur service dataset: {str(e)}")
    
    @staticmethod
    def lister_datasets_projet(projet_id: str) -> List[Dataset]:
        """Lister tous les datasets d'un projet"""
        try:
            response = supabase.table('datasets')\
                .select('*')\
                .eq('projet_id', projet_id)\
                .order('created_at', desc=True)\
                .execute()
            
            return [Dataset.from_dict(item) for item in response.data]
            
        except Exception as e:
            raise Exception(f"Erreur récupération datasets: {str(e)}")
    
    @staticmethod
    def uploader_et_creer_dataset(
        fichier_path: str, 
        nom_dataset: str, 
        projet_id: str,
        format_fichier: str
    ) -> Dataset:
        """Upload un fichier et crée le dataset correspondant"""
        try:
            # 1. Calculer la taille du fichier
            taille_bytes = os.path.getsize(fichier_path)
            taille_mb = round(taille_bytes / (1024 * 1024), 2)
            
            # 2. Générer un nom unique pour le fichier
            timestamp = int(datetime.now().timestamp())
            nom_fichier = f"{projet_id}/{timestamp}_{os.path.basename(fichier_path)}"
            
            # 3. Upload vers Supabase Storage
            from services.storage_service import StorageService
            fichier_url = StorageService.uploader_dataset(fichier_path, nom_fichier)
            
            if not fichier_url:
                raise Exception("Erreur lors de l'upload du fichier")
            
            # 4. Créer l'entrée dataset
            dataset = Dataset(
                nom=nom_dataset,
                projet_id=projet_id,
                fichier_url=fichier_url,
                taille_mb=taille_mb,
                format_fichier=format_fichier
            )
            
            return DatasetService.creer_dataset(dataset)
            
        except Exception as e:
            raise Exception(f"Erreur upload dataset: {str(e)}")
    
    @staticmethod
    def supprimer_dataset(dataset_id: str, supprimer_fichier: bool = True) -> bool:
        """Supprimer un dataset et optionnellement son fichier"""
        try:
            # 1. Récupérer les infos du dataset avant suppression
            dataset_info = supabase.table('datasets')\
                .select('fichier_url')\
                .eq('id', dataset_id)\
                .single()\
                .execute()
            
            # 2. Supprimer l'entrée en base
            response = supabase.table('datasets')\
                .delete()\
                .eq('id', dataset_id)\
                .execute()
            
            # 3. Supprimer le fichier si demandé
            if supprimer_fichier and dataset_info.data and dataset_info.data.get('fichier_url'):
                try:
                    # Extraire le nom du fichier de l'URL
                    fichier_url = dataset_info.data['fichier_url']
                    nom_fichier = fichier_url.split('/')[-1]
                    
                    from services.storage_service import StorageService
                    StorageService.supprimer_fichier(nom_fichier)
                except Exception as e:
                    print(f"Attention: Erreur suppression fichier: {str(e)}")
            
            return len(response.data) > 0
            
        except Exception as e:
            raise Exception(f"Erreur suppression dataset: {str(e)}")
    
    @staticmethod
    def statistiques_datasets(projet_id: str) -> Dict:
        """Récupère les statistiques des datasets d'un projet"""
        try:
            datasets = DatasetService.lister_datasets_projet(projet_id)
            
            if not datasets:
                return {
                    "nombre_datasets": 0,
                    "taille_totale_mb": 0,
                    "formats": {},
                    "dataset_plus_gros": None
                }
            
            # Calculs statistiques
            taille_totale = sum(d.taille_mb or 0 for d in datasets)
            formats = {}
            dataset_plus_gros = max(datasets, key=lambda d: d.taille_mb or 0)
            
            # Comptage des formats
            for dataset in datasets:
                format_fichier = dataset.format_fichier or "inconnu"
                formats[format_fichier] = formats.get(format_fichier, 0) + 1
            
            return {
                "nombre_datasets": len(datasets),
                "taille_totale_mb": round(taille_totale, 2),
                "taille_totale_formatee": f"{taille_totale/1024:.1f} GB" if taille_totale >= 1024 else f"{taille_totale:.1f} MB",
                "formats": formats,
                "dataset_plus_gros": {
                    "nom": dataset_plus_gros.nom,
                    "taille": dataset_plus_gros.get_taille_formatee()
                } if dataset_plus_gros.taille_mb else None
            }
            
        except Exception as e:
            raise Exception(f"Erreur calcul statistiques: {str(e)}")
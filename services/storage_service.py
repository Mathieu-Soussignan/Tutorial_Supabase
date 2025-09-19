import os
from typing import Optional, List
from config.database import supabase

class StorageService:
    
    @staticmethod
    def uploader_dataset(fichier_path: str, nom_fichier: str, bucket: str = "datasets") -> Optional[str]:
        """Upload d'un dataset"""
        try:
            with open(fichier_path, 'rb') as f:
                response = supabase.storage.from_(bucket).upload(nom_fichier, f)
            
            if response:
                # Récupérer l'URL publique
                url = supabase.storage.from_(bucket).get_public_url(nom_fichier)
                return url
            
        except Exception as e:
            raise Exception(f"Erreur upload: {str(e)}")
        
        return None
    
    @staticmethod
    def lister_fichiers(bucket: str = "datasets") -> List[dict]:
        """Lister les fichiers d'un bucket"""
        try:
            response = supabase.storage.from_(bucket).list()
            return response
            
        except Exception as e:
            raise Exception(f"Erreur listage: {str(e)}")
    
    @staticmethod
    def supprimer_fichier(nom_fichier: str, bucket: str = "datasets") -> bool:
        """Supprimer un fichier"""
        try:
            response = supabase.storage.from_(bucket).remove([nom_fichier])
            return len(response) > 0
            
        except Exception as e:
            raise Exception(f"Erreur suppression: {str(e)}")
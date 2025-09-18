from typing import List, Optional
from config.database import supabase
from models.projet import ProjetIA

class ProjetService:
    
    @staticmethod
    def creer_projet(projet: ProjetIA, user_id: str) -> ProjetIA:
        """Créer un nouveau projet IA"""
        try:
            data = projet.to_dict()
            data['created_by'] = user_id
            
            response = supabase.table('projets_ia').insert(data).execute()
            
            if response.data:
                return ProjetIA.from_dict(response.data[0])
            else:
                raise Exception("Erreur lors de la création du projet")
                
        except Exception as e:
            raise Exception(f"Erreur service: {str(e)}")
    
    @staticmethod
    def lister_projets(user_id: str) -> List[ProjetIA]:
        """Lister tous les projets d'un utilisateur"""
        try:
            response = supabase.table('projets_ia')\
                .select('*')\
                .eq('created_by', user_id)\
                .order('created_at', desc=True)\
                .execute()
            
            return [ProjetIA.from_dict(item) for item in response.data]
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération: {str(e)}")
    
    @staticmethod
    def mettre_a_jour_projet(projet_id: str, updates: dict, user_id: str) -> ProjetIA:
        """Mettre à jour un projet"""
        try:
            updates['updated_at'] = 'now()'
            
            response = supabase.table('projets_ia')\
                .update(updates)\
                .eq('id', projet_id)\
                .eq('created_by', user_id)\
                .execute()
            
            if response.data:
                return ProjetIA.from_dict(response.data[0])
            else:
                raise Exception("Projet non trouvé ou accès refusé")
                
        except Exception as e:
            raise Exception(f"Erreur mise à jour: {str(e)}")
    
    @staticmethod
    def supprimer_projet(projet_id: str, user_id: str) -> bool:
        """Supprimer un projet"""
        try:
            response = supabase.table('projets_ia')\
                .delete()\
                .eq('id', projet_id)\
                .eq('created_by', user_id)\
                .execute()
            
            return len(response.data) > 0
            
        except Exception as e:
            raise Exception(f"Erreur suppression: {str(e)}")
    
    @staticmethod
    def rechercher_projets(user_id: str, terme: str) -> List[ProjetIA]:
        """Recherche full-text dans les projets"""
        try:
            response = supabase.table('projets_ia')\
                .select('*')\
                .eq('created_by', user_id)\
                .or_(f'nom.ilike.%{terme}%,description.ilike.%{terme}%')\
                .execute()
            
            return [ProjetIA.from_dict(item) for item in response.data]
            
        except Exception as e:
            raise Exception(f"Erreur recherche: {str(e)}")
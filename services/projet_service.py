from typing import List, Optional
from config.database import supabase
from models.projet import ProjetIA

class ProjetService:

    @staticmethod
    def creer_projet_ia(projet: ProjetIA, user_id: str) -> ProjetIA:
        """Création avec validation métier"""
        try:
            # Validation business
            if not projet.nom.strip():
                raise ValueError("Le nom du projet est obligatoire")
            
            if projet.type_modele not in ['NLP', 'Computer Vision', 'ML', 'Deep Learning']:
                raise ValueError("Type de modèle non supporté")
            
            # Validation des hyperparamètres
            if projet.hyperparametres:
                if not isinstance(projet.hyperparametres, dict):
                    raise ValueError("Les hyperparamètres doivent être un dictionnaire")
            
            data = projet.to_dict()
            data['created_by'] = user_id
            
            response = supabase.table('projets_ia').insert(data).execute()
            
            if response.data:
                return ProjetIA.from_dict(response.data[0])
            else:
                raise Exception("Erreur lors de la création")
                
        except Exception as e:
            raise Exception(f"Erreur service création: {str(e)}")

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

    @staticmethod
    def statistiques_projets(user_id: str) -> dict:
        """Analytics en temps réel des projets"""
        try:
            # Requête pour récupérer tous les projets de l'utilisateur
            if user_id:
                response = supabase.table('projets_ia')\
                    .select('type_modele, statut')\
                    .eq('created_by', user_id)\
                    .execute()
            else:
                response = supabase.table('projets_ia')\
                    .select('type_modele, statut')\
                    .order('created_at', desc=True)\
                    .limit(10)\
                    .execute()
            
            if not response.data:
                return {"total": 0, "par_type": {}, "par_statut": {}, "type_favori": None}
            
            # Calculs des statistiques
            par_type = {}
            par_statut = {}
            
            for projet in response.data:
                type_modele = projet['type_modele']
                statut = projet['statut']
                
                # Compter par type
                par_type[type_modele] = par_type.get(type_modele, 0) + 1
                
                # Compter par statut
                par_statut[statut] = par_statut.get(statut, 0) + 1
            
            # Trouver le type favori
            type_favori = None
            if par_type:
                type_favori = max(par_type.items(), key=lambda x: x[1])[0]
            
            return {
                "total": len(response.data),
                "par_type": par_type,
                "par_statut": par_statut,
                "type_favori": type_favori
            }
            
        except Exception as e:
            raise Exception(f"Erreur calcul statistiques: {str(e)}")
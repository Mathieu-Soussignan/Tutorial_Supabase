# services/projet_service.py - VERSION DÉMO
from typing import List, Optional, Dict
from config.database import supabase

def creer_projet(user_id: str, nom: str, description: str, type_modele: str, hyperparametres: dict):
    """Créer un nouveau projet IA - VERSION DÉMO"""
    try:
        data = {
            "nom": nom,
            "description": description,
            "type_modele": type_modele,
            "hyperparametres": hyperparametres
        }
        
        # Ajouter created_by seulement si c'est un UUID valide
        if user_id and is_valid_uuid(user_id):
            data["created_by"] = user_id
        else:
            # Mode démo : utiliser NULL
            data["created_by"] = None
        
        response = supabase.table('projets_ia').insert(data).execute()
        return response
        
    except Exception as e:
        raise Exception(f"Erreur création projet: {str(e)}")

def is_valid_uuid(uuid_string):
    """Vérifier si c'est un UUID valide"""
    try:
        import uuid
        uuid.UUID(uuid_string)
        return True
    except (ValueError, TypeError):
        return False

def lister_projets(user_id: str = None):
    """Lister les projets - VERSION DÉMO"""
    try:
        # Mode démo : lister TOUS les projets récents
        query = supabase.table('projets_ia').select('*').order('created_at', desc=True).limit(20)
        
        response = query.execute()
        return response
        
    except Exception as e:
        raise Exception(f"Erreur listage projets: {str(e)}")
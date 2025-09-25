# config/database.py - VERSION COMPLÈTE CORRIGÉE
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class SupabaseConfig:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.anon_key = os.getenv("SUPABASE_KEY")
        self.service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if not self.url:
            raise ValueError("SUPABASE_URL est obligatoire")
            
        # POUR LA DÉMO : Utiliser service_role qui bypass RLS
        if self.service_key:
            self.client: Client = create_client(self.url, self.service_key)
            print("🔧 Mode admin: RLS bypassé pour la démo")
        elif self.anon_key:
            self.client: Client = create_client(self.url, self.anon_key)
            print("🔐 Mode normal: RLS activé")
        else:
            raise ValueError("Aucune clé API disponible")
    
    def get_client(self) -> Client:
        return self.client

# Instance globale
supabase_config = SupabaseConfig()

# FONCTION MANQUANTE : get_supabase_client
def get_supabase_client() -> Client:
    """Récupère le client Supabase global"""
    return supabase_config.get_client()

# Pour compatibilité avec d'anciens imports
supabase = get_supabase_client()
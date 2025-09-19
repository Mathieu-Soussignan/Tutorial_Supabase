# config/database.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class SupabaseConfig:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.anon_key = os.getenv("SUPABASE_KEY")
        self.service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if not self.url or not self.anon_key:
            raise ValueError("SUPABASE_URL et SUPABASE_KEY sont obligatoires")
            
        # Client normal (avec RLS)
        self.client: Client = create_client(self.url, self.anon_key)
        
        # Client admin (bypass RLS)
        if self.service_key:
            self.admin_client: Client = create_client(self.url, self.service_key)
        else:
            self.admin_client = self.client  # Fallback
    
    def get_client(self, admin_mode=False) -> Client:
        """
        Récupère le client Supabase
        admin_mode: True pour bypass RLS (démo uniquement)
        """
        if admin_mode and hasattr(self, 'admin_client'):
            return self.admin_client
        return self.client

# Instance globale
supabase_config = SupabaseConfig()
# Pour la démo, on utilise le mode admin
supabase = supabase_config.get_client(admin_mode=True)
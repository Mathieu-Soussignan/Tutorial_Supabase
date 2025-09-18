import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class SupabaseConfig:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL et SUPABASE_KEY doivent être définis")
            
        self.client: Client = create_client(self.url, self.key)
    
    def get_client(self) -> Client:
        return self.client

# Instance globale
supabase_config = SupabaseConfig()
supabase = supabase_config.get_client()
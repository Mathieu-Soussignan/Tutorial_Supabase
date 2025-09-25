# services/auth_service.py
from config.database import get_supabase_client

supabase = get_supabase_client()

def sign_up_email(email: str, password: str):
    resp = supabase.auth.sign_up({"email": email, "password": password})
    return resp

def sign_in_email(email: str, password: str):
    resp = supabase.auth.sign_in_with_password({"email": email, "password": password})
    return resp

def sign_out():
    supabase.auth.sign_out()
    return {"ok": True}

def get_user():
    # renvoie l'utilisateur courant si une session est persistée côté client
    return supabase.auth.get_user()
from config.database import get_supabase_client

supabase = get_supabase_client()
res = supabase.auth.sign_in_with_oauth({"provider": "github"})
print("Objet retourné :", res)
print("URL :", res.url)
# services/storage_service.py
from config.database import get_supabase_client
import uuid

supabase = get_supabase_client()
BUCKET = "datasets"

def upload_file(file_stream, filename: str, content_type: str = None):
    key = f"{uuid.uuid4()}_{filename}"
    res = supabase.storage.from_(BUCKET).upload(key, file_stream, {"content-type": content_type} if content_type else None)
    if res.get("error"):
        raise Exception(res["error"])
    public_url = supabase.storage.from_(BUCKET).get_public_url(key)
    return {"key": key, "public_url": public_url}
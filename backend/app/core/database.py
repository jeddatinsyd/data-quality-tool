import os
from supabase import create_client, Client

# These should be in .env
url: str = os.environ.get("SUPABASE_URL", "")
key: str = os.environ.get("SUPABASE_KEY", "")

supabase: Client = None

if url and key:
    supabase = create_client(url, key)
else:
    print("Warning: Supabase credentials not found. Persistence will be disabled.")

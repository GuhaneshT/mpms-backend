from supabase import create_client, Client
from backend.core.config import settings

# Initialize Supabase client (communicates over HTTPS, port 443)
supabase_client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


def get_supabase() -> Client:
    """FastAPI dependency that provides the Supabase client."""
    return supabase_client
